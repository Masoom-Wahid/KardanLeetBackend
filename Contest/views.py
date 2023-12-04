from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import (ContestantsSerializer,
                          ContestSerializer,
                          ContestGroupSerializer,
                          ContestQuestionSerializer)
from rest_framework.permissions import IsAdminUser , IsAuthenticated,AllowAny
from rest_framework import status
from Questions.serializers import SampleSerializer
from .models import Contests,Contest_Groups,Contestants,Contest_Question
from rest_framework.decorators import action
from .utils import create_folder_for_contest,delete_folder_for_contest
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
from .testers.execute import RunCode
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class CompetetionViewSet(ModelViewSet):
    queryset = Contests.objects.filter(starred=True)
    serializer_class = ContestSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def list(self,request):
        #TODO : Make this with caching
        try:
            instance = Contests.objects.get(starred=True)
        except Contests.DoesNotExist:
            return Response(
                {"detail":"An Starred Contest Does Not Exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        questions = Contest_Question.objects.filter(contest=instance)
        serializer = ContestQuestionSerializer(questions,many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
    
    def retrieve(self,request,pk):
        try:
            instance = Contests.objects.get(starred=True)
        except Contests.DoesNotExist:
            return Response(
                {"detail":"An Starred Contest Does Not Exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            question = instance.contest_question_set.all().get(id=pk)
        except:
            return Response(
                {"detail":"Invalid Question ID"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ContestQuestionSerializer(question,many=False)
        sample_test_cases = question.sample_test_cases_set.all()
        sample_serilizer = SampleSerializer(sample_test_cases,many=True)
        return Response(
            {
                "question":serializer.data,
                "test_cases":sample_serilizer.data
            },
            status=status.HTTP_200_OK
        )
    def get_suffix(self,lang):
        suffixes = {
            "python":".py",
            "java":".java",
            "c":".cpp"
        }
        return suffixes[lang]
    
    def create(self,request):
        lang = request.data.get("lang",None)
        typeof = request.data.get("type",None)
        code = request.FILES.get("code",None)
        question_name = request.data.get("question_name",None)
        #FIXME : question name is only given in id so think about if this is correct
        contest_name = request.data.get("contest_name",None)
        if lang and code and typeof:
            suffix = self.get_suffix(lang)
            if typeof == "run":
                run = RunCode(question_name,
                                    contest_name,
                                    lang,
                                    suffix,
                                    code
                                    )
                result = run.run()
                if result[0]:
                    return Response(
                        status=status.HTTP_200_OK
                    )
                else:
                    if result[1] == "timeout":
                        return Response(
                            {"detail":"timeout , Infinite Loop",
                                "num_of_solved":result[2]},
                                status=status.HTTP_400_BAD_REQUEST
                            
                        )

                    else:
                        return Response(
                            {"detail":"Invalid Answer",
                                "num_of_solved":result[1]
                                },
                                status=status.HTTP_400_BAD_REQUEST
                        )

            elif typeof == "submit":
                pass
            else:
                return Response(
                    {"detail":"Invalid Type"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        else:
            return Response(
                {"detail":"lang and code and typeof required"},
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self,request,pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def destroy(self,request,pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

class ContestViewSet(ModelViewSet):
    queryset = Contests.objects.all()
    serializer_class = ContestSerializer

    def get_permissions(self):
        if self.action in ["create","list","retreive","destroy"]:
            permission_classes = [IsAdminUser]
        elif self.action in ["sample"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]

        return (permission() for permission in permission_classes)


    def create(self,request,*args,**kwargs):
        request.data["name"] = request.data["name"].replace(" ","_")
        serializer = ContestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        create_folder_for_contest(instance.name)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
    def destroy(self,request,pk=None):
        instance = self.get_object()
        delete_folder_for_contest(instance.name)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False,methods=["POST"])
    def star_contest(self,request):
        contest_name = request.data.get("name",None)
        typeof = request.data.get("type",None)
        if contest_name and typeof:
            try:
                contest = Contests.objects.get(name=contest_name)
            except Contests.DoesNotExist:
                return Response(
                    {"detail":"Invalid Contest Name"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if typeof == "star":
                if Contests.objects.filter(starred=True).exists():
                    return Response(
                        {"detail":"an starred contest already exists"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    contest.starred = True
                    contest.save()
                    return Response(
                    status=status.HTTP_204_NO_CONTENT
                    )
            elif typeof == "unstar":
                contest.starred = False
                contest.save()
                return Response(
                    status=status.HTTP_204_NO_CONTENT
                )
            else:
                return Response(
                    {"detail":"Invalid Type"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            pass
    
    @action(detail=False,methods=["POST"])
    def groups(self,request):
        contest_name = request.data.get("name",None)
        if contest_name:
            try:
                contest = Contests.objects.get(name=contest_name)
            except:
                return Response(
                    {"detail":"Invalid Contest Name"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            instance = Contest_Groups.objects.filter(contest=contest)
            serializer = ContestGroupSerializer(instance,many=True)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        else:
            return Response(
                {"detail":"id param required"},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False,methods=["POST"])
    def start_contest(self,request):
        name = request.data.get("name",None)
        if name:
            #TODO : Add a worker here 
            instance = Contests.objects.get("name",None)

        else:
            pass

    # @action(detail=False,methods=["POST"],parser_classes=[MultiPartParser,FormParser])
    # def sample(self,request):
    #     sample = request.FILES.get("sample")
    #     num_of_test_cases = request.data.get("num_of_test_cases")
    #     contest_name = request.data.get("contest_name")
    #     question_name = request.data.get("question_name")
    #     check = run(int(num_of_test_cases),contest_name,question_name,sample)
    #     print(check)
    #     return Response(
    #         status=status.HTTP_204_NO_CONTENT
    #     )
    @action(detail=False,methods=["GET","POST","DELETE"])
    def contestants(self,request):
        method = request.method
        if method == "GET":
            group_id = request.GET.get("group_id",None)
            if group_id:
                try:
                    group = Contest_Groups.objects.get(id=group_id)
                except Contest_Groups.DoesNotExist:
                    return Response(
                        {"detail":"Invalid ID"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                instance = Contestants.objects.filter(group=group)
                serializer = ContestantsSerializer(instance,many=True)
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
            else:
                pass
        if method == "POST":
            group_id = request.data.get("group_id",None)
            name = request.data.get("name",None)
            if not group_id or not name:
                return Response(
                        {"detail":"Group_id and name required"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                try:
                    instance = Contest_Groups.objects.get(id=group_id)
                except Contest_Groups.DoesNotExist:
                    return Response(
                        {"detail":"Invalid ID"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                contest_instance = Contestants.objects.create(
                    group = instance,
                    name=name
                )
                serializer = ContestantsSerializer(contest_instance,many=False)
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
        if method == "DELETE":
            conetsant_id = request.data.get("id",None)
            if conetsant_id != None:
                try:
                    instance = Contestants.objects.get(id=conetsant_id)
                except Contestants.DoesNotExist:
                    return Response(
                        {"detail":"Invalid ID"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                instance.delete()
                return Response(
                    {"detail":"ok"},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"detail":"id required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

    

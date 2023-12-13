from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import (ContestantsSerializer,
                          ContestSerializer,
                          ContestGroupSerializer,
                          ContestQuestionSerializer,
                          ContestSubmissionSerializer)
from rest_framework.permissions import IsAdminUser , IsAuthenticated,AllowAny
from rest_framework import status
from Questions.serializers import SampleSerializer
from .models import Contests,Contest_Groups,Contestants,Contest_Question,Contest_submissiosn
from rest_framework.decorators import action
from .utils import create_folder_for_contest,delete_folder_for_contest
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
from .testers.execute import RunCode
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .tasks import scheduler


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
        show_submissions = request.GET.get("submissions",False)
        show_code = request.GET.get("show_code",False)
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
        if show_submissions:
            group = get_object_or_404(Contest_Groups,user=request.user)
            print(group.calculateTime())
            submissions = Contest_submissiosn.objects.filter(group=group,question=question)
            serializer = ContestSubmissionSerializer(submissions,many=True,context={
                "showCode":show_code
            })
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        else:
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

    
    def create(self,request):
        lang = request.data.get("lang",None)
        typeof = request.data.get("type",None)
        code = request.FILES.get("code",None)

        question = get_object_or_404(Contest_Question, pk=request.data.get("id",None))
        group = get_object_or_404(Contest_Groups,user=request.user)
        contest = get_object_or_404(Contests,starred=True,started=True)
        # if Contest_submissiosn.objects.filter(group=group,question=question,solved=True).exists():
        #     return Response(
        #         {"detail":"You Have Already Solved This Question"},
        #         status=status.HTTP_403_FORBIDDEN
        #     )
        if lang and code and typeof:
            run = RunCode(
                        typeof
                        ,group
                        ,question
                        ,contest
                        ,lang
                        ,code
                        )
            result,detail = run.run()
            if result:
                return Response(
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"detail":detail},
                    status=status.HTTP_406_NOT_ACCEPTABLE
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
    def FinishContest(self):
        starred_contest = Contests.objects.get(starred=True,started=True)
        starred_contest.finished = True

    @action(detail=False,methods=["POST"])
    def actions(self,request):
        action_data = request.data.get("action",None)
        action , typeof = action_data.split("_")
        contest_name = request.data.get("name",None)
        if contest_name and action:
            contest_instance = get_object_or_404(Contests,name=contest_name)
            """Change The Contest Based On The Request"""
            if action == "start":
                if action == "do" and contest_instance.started != True:
                    contest_instance.started = True
                    contest_instance.started_at = timezone.now()
                    run_at = timezone.now() + contest_instance.duration
                    scheduler.add_job(self.FinishContest, 'date', run_date=run_at,id="Contest_Listener")
                else:
                    return Response(
                        {"detail":"The Contest Has Already Started"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                if action == "undo" : contest_instance.started = False ; scheduler.pause_job("Contest_Listener")
                if action == "resume" : contest_instance.starred = True ; scheduler.resume_job("Contest_Listener")
            if action == "reset":
                if action == "do" : contest_instance.starred = False ; scheduler.remove_job("Contest_Listener")
            elif action == "star":
                if Contests.objects.filter(starred=True).exists():
                    return Response(
                        {"detail":"Starred Contest Already Exists"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                contest_instance.starred = True if typeof == "do" else False
            elif action == "finished":
                contest_instance.finished = True if typeof == "do" else False
            
            contest_instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({
                "detail":"name and action required"},
                status=status.HTTP_400_BAD_REQUEST
                )
    
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

    

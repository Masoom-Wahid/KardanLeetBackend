from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import (ContestantsSerializer,
                          ContestSerializer,
                          ContestGroupSerializer,
                          ContestQuestionSerializer,
                          ContestSubmissionSerializer)
from rest_framework.permissions import IsAdminUser , IsAuthenticated,AllowAny
from rest_framework import status
from Questions.serializers import SampleTestCaseSerializer
from .models import Contests,Contest_Groups,Contestants,Contest_Question,Contest_submissiosn
from rest_framework.decorators import action
from .utils import create_folder_for_contest,delete_folder_for_contest
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
from .testers.Run import Run
from .testers.ManualRun import ManualRun
from .testers.SubmitRun import SubmitRun
from rest_framework.permissions import IsAuthenticated
from Auth.permissions import IsSuperUserOrIsStaffUser
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
        instance = get_object_or_404(Contests,starred=True)
        questions = Contest_Question.objects.filter(contest=instance)
        serializer = ContestQuestionSerializer(questions,many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
    
    def retrieve(self,request,pk):
        show_submissions = request.GET.get("submissions",False)
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
            submission_id = request.GET.get("id",None)
            if submission_id:
                submission_instance = get_object_or_404(Contest_submissiosn,id=submission_id)
                serializer = ContestSubmissionSerializer(submission_instance,many=False,context={
                    "showCode":True
                })
            else:
                group = get_object_or_404(Contest_Groups,user=request.user)
                submissions = Contest_submissiosn.objects.filter(group=group,question=question)
                serializer = ContestSubmissionSerializer(submissions,many=True,context={
                    "showCode":False
                })
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        else:
            serializer = ContestQuestionSerializer(question,many=False)
            sample_test_cases = question.sample_test_cases_set.all()
            sample_serilizer = SampleTestCaseSerializer(sample_test_cases,many=True)
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
        if Contest_submissiosn.objects.filter(group=group,question=question,solved=True).exists():
            return Response(
                {"detail":"You Have Already Solved This Question"},
                status=status.HTTP_403_FORBIDDEN
            )
        if lang and code and typeof:
            if typeof == "run":
                run = Run(
                            group
                            ,question
                            ,contest
                            ,lang
                            ,code
                            )
            elif typeof=="submit":
                run = SubmitRun(
                            group
                            ,question
                            ,contest
                            ,lang
                            ,code
                            )
            else:
                manual_data = request.data.get("manual_testcase",None)
                run = ManualRun(
                            group
                            ,question
                            ,contest
                            ,lang
                            ,code
                            ,manual_data
                            )
        

            result,detail = run.run()
            if result:
                return Response(
                    {"detail":detail},
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
    permission_classes = [IsSuperUserOrIsStaffUser]


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
        starred_contest.save()


    def update(self,request,pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    @action(detail=False,methods=["POST"])
    def actions(self,request):
        action_data = request.data.get("action",None)
        action , typeof = action_data.split("_")
        contest_name = request.data.get("name",None)
        if contest_name and action:
            contest_instance = get_object_or_404(Contests,name=contest_name)
            """Change The Contest Based On The Request"""
            if typeof == "start":
                if action == "do":
                    if contest_instance.started == True and contest_instance.starred != False:
                        contest_instance.started = True
                        contest_instance.started_at = timezone.now()
                        run_at = timezone.now() + contest_instance.duration
                        scheduler.add_job(self.FinishContest, 'date', run_date=run_at,id="Contest_Listener")
                    else:
                        return Response(
                            {"detail":"The Contest Has Already Started or You Need To Star The Contest"},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                elif action == "undo" : contest_instance.started = False ; scheduler.pause_job("Contest_Listener")
                elif action == "resume" : contest_instance.starred = True ; scheduler.resume_job("Contest_Listener")
            if typeof == "reset":
                if action == "do" : 
                    contest_instance.starred = False 
                    try:
                        scheduler.remove_job("Contest_Listener")
                    except:
                        pass
            elif typeof == "star":
                if action == "do":
                    if Contests.objects.filter(starred=True).exists():
                        return Response(
                            {"detail":"Starred Contest Already Exists"},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    contest_instance.starred = True 
                else:
                    contest_instance.starred = False
            elif typeof == "finish":
                contest_instance.finished = True if action == "do" else False
            
            contest_instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({
                "detail":"name and action required"},
                status=status.HTTP_400_BAD_REQUEST
                )
    
    @action(detail=False,methods=["POST"])
    def groups(self,request):
        contest = get_object_or_404(Contests,name=request.data.get("name",None))
        instance = Contest_Groups.objects.filter(contest=contest)
        serializer = ContestGroupSerializer(instance,many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
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
            print("here")
            group = get_object_or_404(Contest_Groups,id=request.GET.get("id",None))
            instance = Contestants.objects.filter(group=group)
            serializer = ContestantsSerializer(instance,many=True)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        if method == "POST":
            name = request.data.get("name",None)
            if not name:
                return Response(
                        {"detail":"name required"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                group = get_object_or_404(Contest_Groups,id=request.data.get("id",None))
                contest_instance = Contestants.objects.create(
                    group = group,
                    name=name
                )
                serializer = ContestantsSerializer(contest_instance,many=False)
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
        if method == "DELETE":
            instance = get_object_or_404(Contestants,id=request.GET.get("id",None))
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    

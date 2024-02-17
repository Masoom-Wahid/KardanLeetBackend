from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import (
                          ContestSerializer,
                          ContestGroupSerializer,
                          ContestQuestionSerializer,
                          ContestSubmissionSerializer,
                          CompetitionQuestionSerializer,
                          RetreiveQuestionSerializer)
from rest_framework.permissions import  IsAuthenticated
from rest_framework import status
from Questions.serializers import (SampleTestCasesExampleSerializer
                                ,ConstraintsSerializer
                                ,ShowSampleTestCasesExampleSerializer)
from .models import Contests,Contest_Groups,Contest_Question,Contest_submissiosn
from rest_framework.decorators import action
from .utils import (create_folder_for_contest
                    ,delete_folder_for_contest
                    ,change_contest_name
                    ,sortLeaderBoarddata,
                    getLeaderBoardData,
                    check_question_files
                    )
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
from .testers.Run import Run
from .testers.ManualRun import ManualRun
from .testers.SubmitRun import SubmitRun
from .testers.__Del__ import deleteFiles
from rest_framework.permissions import IsAuthenticated
from Auth.permissions import IsSuperUserOrIsStaffUser
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .tasks import scheduler
from django.conf import settings
from cryptography.fernet import Fernet
from math import ceil
from django.db.models import Q
from django.db.models import Count, Sum, Case, When
from django.core.cache import cache
import datetime


class CompetetionViewSet(ModelViewSet):
    queryset = Contests.objects.filter(starred=True)
    serializer_class = ContestSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]


    def list(self,request):
        try:
            instance = Contests.objects.get(started=True,finished=False)
        except :
            return Response(
                status=status.HTTP_423_LOCKED
            )
        questions = Contest_Question.objects.filter(contest=instance).order_by("point")
        serializer = CompetitionQuestionSerializer(questions,many=True,context={
            "user":request.user
            })
        return Response(
            {
            "name":instance.name,
            "data":serializer.data,
            },
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
                submissions = Contest_submissiosn.objects.filter(
                    group=group,
                    question=question).order_by("-solved","-submit_time")
                serializer = ContestSubmissionSerializer(submissions,many=True,context={
                    "showCode":False
                })
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        else:
            serializer = RetreiveQuestionSerializer(question,many=False,context={
            "user":request.user
            })
            sample_test_cases = question.sampletestcasesexample_set.all()

            try: consts = question.constraints 
            except : consts = None

            sample_serilizer = ShowSampleTestCasesExampleSerializer(sample_test_cases,many=True)
            if consts : constraints_serializer = ConstraintsSerializer(consts,many=False)
            return Response(
                {
                    "question":serializer.data,
                    "test_cases":sample_serilizer.data,
                    "consts":constraints_serializer.data if consts else {"consts":""}
                },
                status=status.HTTP_200_OK
            )

    
    @action(detail=False,methods=["GET"])
    def submissions(self,request):
        sub_id = request.GET.get("id",None)
        instance = get_object_or_404(Contest_submissiosn,id=sub_id)
        if instance.group.user != request.user and  not request.user.is_superuser:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
                )
        serializer = ContestSubmissionSerializer(instance,many=False,context={
            "showCode":True
        })
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
    
    @action(detail=False,methods=["POST"],parser_classes=[JSONParser])
    def setTabSwitch(self,request):
        group_instance = get_object_or_404(Contest_Groups,user__id=request.data.get("id",None))
        group_instance.tabswitch = request.data.get("tabswitch",1) ; group_instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

    
    def create(self,request):
        lang = request.data.get("lang",None)
        typeof = request.data.get("type",None)
        code = request.FILES.get("code",None)
        question = get_object_or_404(Contest_Question, pk=request.data.get("id",None))
        group = get_object_or_404(Contest_Groups,user=request.user)

        """
        If The Contest has not started or there is not starred contest or it is finished
        then the API should response with 423.
        
        """
        try:
            contest = Contests.objects.get(starred=True,started=True,finished=False)
        except Contests.DoesNotExist:
            return Response(
                status=status.HTTP_423_LOCKED
                )

        """
        Since It Is Annoying to only have one chance when developing this would be off for developing
         and will only work for production
        """
        if not settings.DEBUG:
            if Contest_submissiosn.objects.filter(group=group,question=question,solved=True).exists():
                return Response(
                    {"detail":"You Have Already Solved This Question"},
                    status=status.HTTP_412_PRECONDITION_FAILED
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

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self,request,pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

class ContestViewSet(ModelViewSet):
    queryset = Contests.objects.all()
    serializer_class = ContestSerializer
    permission_classes = [IsSuperUserOrIsStaffUser]


    def update(self,request,pk=None):
        instance = get_object_or_404(Contests,pk=pk)
        #TODO: Update The credentials.txt file here 
        serializer = ContestSerializer(instance=instance,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
    
    def retrieve(self, request,pk=None):
        instance = get_object_or_404(Contests,id=pk)
        clean_cache = request.GET.get("clean_cache",False)
        show_results = request.GET.get("results",False)
        show_groups = request.GET.get("groups",False)
        show_langs = request.GET.get("lang",False)

        if clean_cache:
            try:
                cache.delete("leaderboard")
            except:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            return Response(
                status=status.HTTP_200_OK
            )
        
        if show_results:
            if show_langs:
                results = instance.contest_groups_set.aggregate(
                    python=Count('contest_submissiosn', filter=Q(contest_submissiosn__lang='python')),
                    java=Count('contest_submissiosn', filter=Q(contest_submissiosn__lang='java')),
                    cpp=Count('contest_submissiosn', filter=Q(contest_submissiosn__lang='cpp')),
                    php=Count('contest_submissiosn', filter=Q(contest_submissiosn__lang='php')),
                    rust=Count('contest_submissiosn', filter=Q(contest_submissiosn__lang='rust')),
                    js=Count('contest_submissiosn', filter=Q(contest_submissiosn__lang='js')),
                    ts=Count('contest_submissiosn', filter=Q(contest_submissiosn__lang='ts')),
                    csharp=Count('contest_submissiosn', filter=Q(contest_submissiosn__lang='csharp')),
                    c=Count('contest_submissiosn', filter=Q(contest_submissiosn__lang='c')),
                )
            """We only want the cache for current starred and started contest not for every one of them"""
            if instance.starred and instance.started and not instance.finished:
                cacheExists = cache.get("leaderboard")
                if cacheExists:
                    sorted_data = sortLeaderBoarddata(cacheExists)
                else:
                    data = getLeaderBoardData(instance)
                    sorted_data = sortLeaderBoarddata(data)
                    cache.set("leaderboard",data,14400)
                elapsed =  instance.duration - (timezone.now() - instance.started_at ) 
                return Response(
                    {
                        "time":int(elapsed.total_seconds()),
                        "data":sorted_data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                data = getLeaderBoardData(instance)
                sorted_data = sortLeaderBoarddata(data)
                return Response(
                    {
                        "time":"",
                        "lang_stats":results if show_langs else "",
                        "data":sorted_data
                    },
                    status=status.HTTP_200_OK
            )

        elif show_groups:
            groups = instance.contest_groups_set.all()
            serializer = ContestGroupSerializer(groups,many=True)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        else:
            serializer = ContestSerializer(instance,many=False)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
                )

    def create(self,request,*args,**kwargs):
        serializer = ContestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        instance.key = str(Fernet.generate_key())[2:-1]
        instance.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
    

    def destroy(self,request,pk=None):
        instance = self.get_object()
        for group in Contest_Groups.objects.filter(contest=instance):
            group.user.delete()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

    def finishContest(self):
        starred_contest = Contests.objects.get(starred=True,started=True)
        starred_contest.finished = True
        starred_contest.starred=False
        deleteFiles()
        starred_contest.save()



    @action(detail=False,methods=["GET"])
    def getLastContest(self,request):
        """Used For Admin Page"""
        contests = Contests.objects.all().order_by("-created_at")[:3]
        serializer = ContestSerializer(contests,many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @action(detail=False,methods=["POST"])
    def setQuestions(self,request):
        contest_name = request.data.get("name",None)
        questions_ids = request.data.get("ids",None)
        conetst_instance = get_object_or_404(Contests,name=contest_name)
        if not questions_ids:
            conetst_instance.contest_question_set.set = set()
            conetst_instance.save()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )
        ids = questions_ids.split(",")
        questions = Contest_Question.objects.filter(id__in=ids)
        if any(question is None for question in questions):
            return Response(
                {"detail":"Invalid ID"},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            conetst_instance.contest_question_set.set(ids)
            conetst_instance.save()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )

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
                    if contest_instance.started == False and contest_instance.starred == True:
                        # Check Wheter the user has upload all the testcases or not
                        if not check_question_files(contest_instance):
                            return Response(
                                {"detail":"Make Sure You Uploaded All The Testcases for every question"},
                                status=status.HTTP_400_BAD_REQUEST
                            )
                        contest_instance.started = True
                        contest_instance.started_at = timezone.now()
                        deleteFiles()
                        run_at = timezone.now() + contest_instance.duration
                        scheduler.add_job(self.finishContest, 'date', run_date=run_at,id="Contest_Listener")
                    else:
                        return Response(
                            {"detail":"The Contest Has Already Started or You Need To Star The Contest"},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                # Just Leaving these there as they will not be used in production since using them is really unstable
                # and we are relying more on manual finishing of the contest
                elif action == "undo" : contest_instance.started = False ; scheduler.pause_job("Contest_Listener")
                elif action == "resume" : contest_instance.starred = True ; scheduler.resume_job("Contest_Listener")
            
            # Sometimes the admin does not want to Delete The Given Contest but rather restart it
            # this just removes the listener and undo star , start and finish
            if typeof == "reset":
                if action == "do" : 
                    contest_instance.started = False
                    contest_instance.finished = False
                    contest_instance.starred = False
                    for group in Contest_Groups.objects.filter(contest=contest_instance):
                        group.user.delete()
                        group.delete()
                    try:
                        scheduler.remove_job("Contest_Listener")
                    except:
                        pass

            # This is For Starring and Unstarring the contest
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
                if action == "do":
                    contest_instance.finished = True 
                    contest_instance.starred = False
                    deleteFiles()
                else:
                    contest_instance.finished = False

            contest_instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({
                "detail":"name and action required"},
                status=status.HTTP_400_BAD_REQUEST
                )
    
    @action(detail=False,methods=["GET"])
    def stats(self,request):
        contest = request.GET.get("contest","starred")
        if contest == "starred":
            contest_instance = get_object_or_404(Contests,starred=True)
        else:
            contest_instance = get_object_or_404(Contests,name=contest)

        previous_contest_groups = Contest_Groups.objects.exclude(contest=contest_instance).values('contest__name').annotate(
    group_count=Count('id')
)

        status = Contest_Groups.objects.filter(contest=contest_instance).annotate(
            group_count=Count('id'),
            challenge_count=Count('contest__contest_question', distinct=True),
            correct_answer_count=Sum(Case(When(contest_submissiosn__solved=True, then=1), default=0)),
            incorrect_answer_count=Sum(Case(When(contest_submissiosn__solved=False, then=1), default=0))
        ).values('group_count', 'challenge_count', 'correct_answer_count', 'incorrect_answer_count').first()

        group_count = status['group_count']
        challenge_count = status["challenge_count"]
        correct_answer_count = status['correct_answer_count']
        incorrect_answer_count = status['incorrect_answer_count']

        return Response(
            {
                "previous_contest_groups":previous_contest_groups,
                "current_contest" : {
                "Active Contestants":group_count,
                "Number of Challenges":challenge_count,
                "Correct Answers":correct_answer_count,
                "Incorrect Answers":incorrect_answer_count,
                }

            }
            
        )
            
    





    @action(detail=False,methods=["GET"])
    def groups(self,request):
        """
        We Have 3 Probbabilties Here
        You Want To See All Groups
        You Want To See All Submissions of a group
        You Want To See a submission detail of a submission
        
        """
        MAXIMUM_PER_PAGE_ALLOWED = 6
        page = int(request.GET.get("page",1))
        group_id = request.GET.get("id",None)
        submission_id = request.GET.get("submission_id",None)
        if submission_id:
            """
            if "id" is given , that means the user wants to see the submissions of a group,
            now if "submission_id" is not given we render all submissions else we render that
            particular submission
            """

            instance = get_object_or_404(Contest_submissiosn,id=submission_id)
            serializer = ContestSubmissionSerializer(instance,many=False,context={
                "showCode":True
            })
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        elif group_id:
                # Filters
            solved = request.GET.get("solved","")
            time = request.GET.get("time","")
            lang = request.GET.get("lang","")

            group_instance = get_object_or_404(Contest_Groups,id=group_id)

            filter_conditions = Q(group=group_instance)
            if lang:
                filter_conditions &= Q(lang=lang)
            elif solved:
                filter_conditions &= Q(solved=solved)


            if time == "earliest":
                instance = Contest_submissiosn.objects.filter(filter_conditions).order_by("-submit_time")
            else:
                instance = Contest_submissiosn.objects.filter(filter_conditions).order_by("submit_time")

            submissions_count = instance.count()
            pages_count = ceil(submissions_count/MAXIMUM_PER_PAGE_ALLOWED)
            if pages_count < page:
                return Response(
                {"detail":"Invalid Page Number"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            index = (page  - 1 )* MAXIMUM_PER_PAGE_ALLOWED
            if index + MAXIMUM_PER_PAGE_ALLOWED > submissions_count:
                last_index = submissions_count
            else:
                last_index = index + MAXIMUM_PER_PAGE_ALLOWED

            data = instance[index:last_index]
            serializer = ContestSubmissionSerializer(data,many=True)

            return Response(
                {
                    "team_name":group_instance.group_name,
                    "avaialabe_pages":pages_count,
                    "submissions_count":submissions_count,
                    "data":serializer.data
                },
                status=status.HTTP_200_OK
            )
        else:
            """
            else the user wants to see all groups
            """
            contest = get_object_or_404(Contests,name=request.GET.get("contest",None))
            instance = Contest_Groups.objects.filter(contest=contest)
            users_count = instance.count()
            pages_count = ceil(users_count / MAXIMUM_PER_PAGE_ALLOWED)
            if pages_count < page:
                return Response(
                    {"detail":"Invalid Page Number"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            index = (page  - 1 )* MAXIMUM_PER_PAGE_ALLOWED
            if index + MAXIMUM_PER_PAGE_ALLOWED > users_count:
                last_index = users_count
            else:
                last_index = index + MAXIMUM_PER_PAGE_ALLOWED

            data = instance[index:last_index]
            serializer = ContestGroupSerializer(data,many=True)

            return Response(
                {
                    "avaialabe_pages":pages_count,
                    "users_count":users_count,
                    "data":serializer.data
                },
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
    
    # @action(detail=False,methods=["GET","POST","DELETE"])
    # def contestants(self,request):
    #     method = request.method
    #     if method == "GET":
    #         group = get_object_or_404(Contest_Groups,id=request.GET.get("id",None))
    #         instance = Contestants.objects.filter(group=group)
    #         serializer = ContestantsSerializer(instance,many=True)
    #         return Response(
    #             serializer.data,
    #             status=status.HTTP_200_OK
    #         )
    #     if method == "POST":
    #         name = request.data.get("name",None)
    #         if not name:
    #             return Response(
    #                     {"detail":"name required"},
    #                     status=status.HTTP_400_BAD_REQUEST
    #                 )
    #         else:
    #             group = get_object_or_404(Contest_Groups,id=request.data.get("id",None))
    #             contest_instance = Contestants.objects.create(
    #                 group = group,
    #                 name=name
    #             )
    #             serializer = ContestantsSerializer(contest_instance,many=False)
    #             return Response(
    #                 serializer.data,
    #                 status=status.HTTP_200_OK
    #             )
    #     if method == "DELETE":
    #         instance = get_object_or_404(Contestants,id=request.GET.get("id",None))
    #         instance.delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)
    

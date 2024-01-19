from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from Contest.models import Contest_Question,Contests
from .models import sample_test_cases,sample_test_cases_file,Constraints
from rest_framework.decorators import action
from .serializers import (ContestQuestionsCreatorSerializer
                          ,ContestQuestionsSerializer
                          ,SampleTestCaseSerializer
                          ,ConstraintsSerializer
                          )
from Auth.permissions import IsSuperUserOrIsStaffUser
from rest_framework.parsers import MultiPartParser, FormParser
import os
from django.conf import settings
from .utils import (create_folder_for_questions
                    ,delete_folder_for_contest
                    ,change_question_name
                    )
from django.db.models import Q
from rest_framework.status import *
from django.shortcuts import get_object_or_404

class QuestionViewSet(ModelViewSet):
    queryset = Contest_Question.objects.all()
    serializer_class = ContestQuestionsSerializer
    permission_classes = [IsSuperUserOrIsStaffUser]
    

    def retrieve(self,request,pk=None):
        question_instance = get_object_or_404(Contest_Question,id=pk)
        avaialabe_test_cases = sample_test_cases_file.objects.filter(question=question_instance).count() // 2
        files_required = avaialabe_test_cases < question_instance.num_of_test_cases
        samples = sample_test_cases.objects.filter(question=question_instance)
        constraints = Constraints.objects.filter(question=question_instance)
        #Serializers
        question_serializer = ContestQuestionsSerializer(question_instance,many=False)
        samples_serializer = SampleTestCaseSerializer(samples,many=True)
        constraints_serializer = ConstraintsSerializer(constraints,many=True)
        return Response(
            {
            "question":question_serializer.data,
            "testcases":{
                "num_of_test_cases":question_instance.num_of_test_cases,
                "avaialabe_test_cases":avaialabe_test_cases,
                "files_required":files_required
            },
            "samples":samples_serializer.data,
            "consts":constraints_serializer.data
            },
            status=status.HTTP_200_OK
            )
    def list(self,request):
        contest_name = request.GET.get("name",None)
        if contest_name:
            contest = get_object_or_404(Contests,name=contest_name)
            instance = Contest_Question.objects.filter(contest=contest)
            serializer = ContestQuestionsSerializer(instance,many=True)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"detail":"name required"},
                status=status.HTTP_400_BAD_REQUEST
            )


    def create(self,request,*args,**kwargs):
        contest = request.data.get("name",None)
        if not contest:
            return Response(
                {"detail" :"name requried"},
                status=status.HTTP_400_BAD_REQUEST
            )
        contest_instance = get_object_or_404(Contests,name=contest)
        # if a question with the given in the same contest exists give an error
        if Contest_Question.objects.filter(contest=contest_instance,title=request.data.get("title",None)).exists():
            return Response(
                {"detail":"A Question With The Given Name In This Contest Exists"},
                status=status.HTTP_400_BAD_REQUEST
                )
        serializer = ContestQuestionsCreatorSerializer(data=request.data,context = {
            "contest":contest_instance
        })
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        create_folder_for_questions(instance.contest.name,instance.title)
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED
        )
    
    def update(self, request,pk=None):
        question = get_object_or_404(Contest_Question,id=pk)
        # Check if a question with this name alredy exists
        if Contest_Question.objects.filter(contest=contest_instance,title=request.data.get("title",None)).exists():
            return Response(
                {"detail":"A Question With The Given Name In This Contest Exists"},
                status=status.HTTP_400_BAD_REQUEST
                )
        """change the question folder name"""
        if change_question_name(question.contest.name,question.title,request.data.get("title")) == None:
            return Response(
                {"detail":"Could Change The Folder Name for the question"},
                status=status.HTTP_400_BAD_REQUEST)
        """update the database instance"""
        serializer = ContestQuestionsSerializer(instance=question,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )   

    def destroy(self, request,pk=None):
        question = get_object_or_404(Contest_Question,id=pk)
        delete_folder_for_contest(question.contest.name,question.title)
        question.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False,methods=["GET","POST","PUT"],parser_classes=[MultiPartParser,FormParser])
    def files(self,request):
        method = request.method
        if method == "POST":
            question_id = request.data.get("id",None)
            files = request.data.getlist("files",None)
            if not question_id or not files:
                return Response(
                    {"detail":"files and id required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                question_instance = get_object_or_404(Contest_Question,pk=question_id)
                num_of_test_cases = question_instance.num_of_test_cases
                avaialabe_test_cases = sample_test_cases_file.objects.filter(question=question_instance).count()
                if num_of_test_cases <= avaialabe_test_cases // 2:
                    return Response(
                        {"detail":"TestCases Has Already Been Uploaded"},
                        status=status.HTTP_400_BAD_REQUEST
                        )
                file_names = [f"input{(avaialabe_test_cases+2)//2}.txt",
                                f"output{(avaialabe_test_cases+2)//2}.txt"
                ]
                for file in files:
                    if not file.name in file_names:
                        return Response(
                            {"Detail":"Invalid Naming Convention"},
                            status=status.HTTP_400_BAD_REQUEST
                            )
                for file in files:            
                    instance  = sample_test_cases_file.objects.create(
                        question = question_instance,
                        test_case_file = file
                    )
                    os.rename(instance.test_case_file.path,
                            os.path.join(
                                settings.MEDIA_ROOT,
                                    "contest",
                                    instance.question.contest.name,
                                    instance.question.title,
                                    file.name))
                    instance.save()
                return Response(
                    status=status.HTTP_204_NO_CONTENT
                )
        elif method == "PUT":
            question_id = request.data.get("question",None)
            id = request.data.get("id",None)
            input_file = request.FILES.get("input",None)
            output_file = request.FILES.get("output",None)
            if question_id and input_file and output_file:
                question_instance = get_object_or_404(Contest_Question,pk=question_id)
                try:
                    inputfilepath = os.path.join(settings.BASE_DIR,"files","contest",question_instance.contest.name,
                                                question_instance.title,
                                                f"input{id}.txt")
                    outputfilepath = os.path.join(settings.BASE_DIR,"files","contest",question_instance.contest.name,
                                                question_instance.title,
                                                f"output{id}.txt")
                    with open(inputfilepath,"w") as past_input_file:
                        past_input_file.write(input_file.read().decode())
                    with open(outputfilepath,"w") as past_output_file:
                        past_output_file.write(output_file.read().decode())

                    return Response(
                        {"data":"ok"},
                        status=status.HTTP_200_OK
                    )
                except Exception as e:
                    return Response(
                        {"detail":str(e)},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {"detail":" question(question_id) and input_file and output_file required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        elif method == "GET":
            question_id = request.GET.get("question",None)
            id = request.GET.get("id",None)
            if question_id:
                question_instance = get_object_or_404(Contest_Question,pk=question_id)
                files_required = sample_test_cases_file.objects.filter(question=question_instance).count() < question_instance.num_of_test_cases
                if not id:
                    return Response(
                        {"testCases":question_instance.num_of_test_cases,
                        "files_required":files_required
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    try:
                        inputfilepath = os.path.join(settings.BASE_DIR,"files","contest",question_instance.contest.name,
                                                question_instance.title,
                                                f"input{id}.txt")
                        ouputfilepath = os.path.join(settings.BASE_DIR,"files","contest",question_instance.contest.name,
                                                question_instance.title,
                                                f"output{id}.txt")
                        with open(inputfilepath,"r") as file:
                            inputdata = file.read()
                        with open(ouputfilepath,"r") as file:
                            outputdata = file.read()
                        return Response(
                            {"input":inputdata,
                            "output":outputdata
                            },
                            status=status.HTTP_200_OK
                        )
                    except Exception as e:
                        return Response(
                            {"detail":str(e)},
                            status=status.HTTP_400_BAD_REQUEST
                        )
            else:
                return Response(
                    {"detail":"question(question_id)required"},
                    status=status.HTTP_400_BAD_REQUEST
                )



"""View all the constraints"""
class ConstraintViewSet(ModelViewSet):
    queryset = Constraints.objects.all()
    serializer_class = ConstraintsSerializer
    permission_classes = [IsSuperUserOrIsStaffUser]
    def list(self,request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

"""
These Are The Real Test Cases , These Are The Descriptive TestCases Which Will Be
Shown To User As An Introduction To The Problem
"""
class SampleTestCasesViewSet(ModelViewSet):
    queryset = sample_test_cases.objects.all()
    serializer_class = SampleTestCaseSerializer
    permission_classes = [IsSuperUserOrIsStaffUser]


    def list(self,request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
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
                try:
                    question_instance= Contest_Question.objects.get(id=question_id)
                except Contest_Question.DoesNotExist:
                    return Response(
                        {"Detail":"Invalid ID"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                num_of_test_cases = question_instance.num_of_test_cases
                file_names = [file.name for file in files]
                for i in range(1,num_of_test_cases+1):
                    if f"input{i}.txt" in file_names and f"output{i}.txt" in file_names:
                        continue
                    else:
                        return Response(
                            {"detail":"Make Sure You Have The Files Lined Up From input1.txt , output1.txt and in order"},
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
            contest_name = request.data.get("contest",None)
            question_id = request.data.get("question",None)
            id = request.data.get("id",None)
            file = request.FILES.get("file",None)
            if question_id and contest_name:
                contest_instance = get_object_or_404(Contests,name=contest_name)
                question_instance = get_object_or_404(Contest_Question,pk=question_id)
                try:
                    filepath = os.path.join(settings.BASE_DIR,"files","contest",contest_instance.name,
                                                question_instance.title,
                                                f"{contest_instance.name}__{question_instance.title}__{id}.txt")
                    with open(filepath,"w") as past_file:
                        past_file.write(file.read().decode())

                    data = file.read().decode()
                    return Response(
                        {"data":data},
                        status=status.HTTP_200_OK
                    )
                except Exception as e:
                    return Response(
                        {"detail":str(e)},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {"detail":"contest(contest_name) and question(question_id)required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        elif method == "GET":
            contest_name = request.GET.get("contest",None)
            question_id = request.GET.get("question",None)
            id = request.GET.get("id",None)
            if question_id and contest_name:
                contest_instance = get_object_or_404(Contests,name=contest_name)
                question_instance = get_object_or_404(Contest_Question,pk=question_id)
                if not id:
                    return Response(
                        {"testCases":question_instance.num_of_test_cases},
                        status=status.HTTP_200_OK
                    )
                else:
                    try:
                        filepath = os.path.join(settings.BASE_DIR,"files","contest",contest_instance.name,
                                                question_instance.title,
                                                f"{contest_instance.name}__{question_instance.title}__{id}.txt")
                        with open(filepath,"r") as file:
                            data = file.read()
                        return Response(
                            {"data":data},
                            status=status.HTTP_200_OK
                        )
                    except Exception as e:
                        return Response(
                            {"detail":str(e)},
                            status=status.HTTP_400_BAD_REQUEST
                        )
            else:
                return Response(
                    {"detail":"contest(contest_name) and question(question_id)required"},
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
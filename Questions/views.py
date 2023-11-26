from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from Contest.serializers import ContestantsSerializer,ContestSerializer
from rest_framework.permissions import IsAdminUser , IsAuthenticated
from rest_framework import status
# from .models import Contest,Contest_Groups,Contestants
from Contest.models import Contest_Question,Contests
from .models import sample_test_cases,sample_test_cases_file
from rest_framework.decorators import action
from .serializers import ContestQuestionsCreatorSerializer,ContestQuestionsSerializer,SampleSerializer
from rest_framework.parsers import MultiPartParser, FormParser
import uuid
from django.core.files.base import ContentFile
import os
from django.conf import settings
from .utils import create_folder_for_questions,delete_folder_for_contest
from django.db.models import Q
from rest_framework.status import *

class QuestionViewSet(ModelViewSet):
    queryset = Contest_Question.objects.all()
    serializer_class = ContestQuestionsSerializer
    def get_permissions(self):
        if self.action in ["create"]:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return (permission() for permission in permission_classes)
    
    def list(self,request):
        contest_name = request.GET.get("name",None)
        if contest_name:
            try:
                contest = Contests.objects.get(name=contest_name)
            except Contests.DoesNotExist:
                return Response(
                    {"detail":"Invalid Name"},
                    status=status.HTTP_400_BAD_REQUEST
                )
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
        try:
            contest_instance = Contests.objects.get(name=contest)
        except Contests.DoesNotExist:
            return Response(
                {"detail":"invalid Contest ID"},
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
    

    @action(detail=False,methods=["POST","DELETE"])
    def test_cases(self,request):
        method = request.method
        if method == "POST":
            question_id = request.data.get("id",None)
            sample = request.data.get("sample",None)
            answer = request.data.get("answer",None)
            if question_id and sample and answer:
                try:
                    question_instance = Contest_Question.objects.get(id=question_id)
                except Contest_Question.DoesNotExist:
                    return Response(
                        {"detail":"Invalid ID"},
                        status=status.HTTP_400_BAD_REQUEST
                    )  
                instance = sample_test_cases.objects.create(
                    question = question_instance,
                    sample = sample,
                    answer = answer
                )
                serializer = SampleSerializer(instance,many=False)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {"detail":"sample , answer , id required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
    @action(detail=False,methods=["POST","DELETE"],parser_classes=[MultiPartParser,FormParser])
    def test_cases_files(self,request):
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
                print(instance.test_case_file.path)
                real_name = f"{instance.question.contest.name}__{instance.question.title}__{file.name}"
                file.name = real_name
                os.rename(instance.test_case_file.path,
                          os.path.join(
                              settings.MEDIA_ROOT,
                                "contest",
                                instance.question.contest.name,
                                instance.question.title,
                                real_name))
                instance.save()

            return Response(
                status=status.HTTP_204_NO_CONTENT
            )









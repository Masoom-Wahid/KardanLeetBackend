from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from Contest.models import Contest_Question,Contests
from .models import (SampleTestCases
                     ,Constraints
                     ,SampleTestCasesExample
                     )
from rest_framework.decorators import action
from .serializers import (ContestQuestionsCreatorSerializer
                          ,ContestQuestionsSerializer
                          ,SampleTestCasesExampleSerializer
                          ,ConstraintsSerializer
                          ,SampleTestCaseSerializer
                          )
from .utils import deleteCachedQuestions
from Auth.permissions import IsSuperUserOrIsStaffUser
from django.db.models import Q
from rest_framework.status import *
from django.shortcuts import get_object_or_404
from math import ceil


class QuestionViewSet(ModelViewSet):
    queryset = Contest_Question.objects.all()
    serializer_class = ContestQuestionsSerializer
    permission_classes = [IsSuperUserOrIsStaffUser]
    
    

    def retrieve(self,request,pk=None):
        question_instance = get_object_or_404(Contest_Question,id=pk)
        #TODO : make this in one query
        avaialabe_test_cases = SampleTestCases.objects.filter(question=question_instance).count() // 2
        
        files_required = avaialabe_test_cases < question_instance.num_of_test_cases
        samples = SampleTestCasesExample.objects.filter(question=question_instance)
        constraints = Constraints.objects.filter(question=question_instance)
        #Serializers
        question_serializer = ContestQuestionsSerializer(question_instance,many=False)
        samples_serializer = SampleTestCasesExampleSerializer(samples,many=True)
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
        # make it filter with questions
        contest_name = request.GET.get("name",None)
        page = int(request.GET.get("page",1))
        MAXIMUM_PER_PAGE_ALLOWED = 8
        if contest_name:
            contest_instance = get_object_or_404(Contests,name=contest_name)
            instance = Contest_Question.objects.filter(contest=contest_instance).order_by("created_at")
        else:
            instance = Contest_Question.objects.all()

        questions_count = instance.count()

        if questions_count == 0:
            return Response(
                status=status.HTTP_204_NO_CONTENT
                )

        pages_count = ceil(questions_count/MAXIMUM_PER_PAGE_ALLOWED)
        if pages_count < page:
            return Response(
            {"detail":"Invalid Page Number"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        index = (page  - 1 )* MAXIMUM_PER_PAGE_ALLOWED
        if index + MAXIMUM_PER_PAGE_ALLOWED > questions_count:
            last_index = questions_count
        else:
            last_index = index + MAXIMUM_PER_PAGE_ALLOWED
        

        serializer = ContestQuestionsSerializer(instance[index:last_index],many=True)
        return Response(
            {
                "available_pages":pages_count,
                "data":serializer.data
            },
            status=status.HTTP_200_OK
        )


    def create(self,request,*args,**kwargs):
        serializer = ContestQuestionsCreatorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED
        )
    
    def update(self, request,pk=None):
        question = get_object_or_404(Contest_Question,id=pk)
        serializer = ContestQuestionsSerializer(instance=question,data=request.data)
        serializer.is_valid(raise_exception=True)
        # Just To Make Sure That Everything is Updated and cache still not holding the previous data
        deleteCachedQuestions(question.title)

        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )   

    def destroy(self, request,pk=None):
        question = get_object_or_404(Contest_Question,id=pk)
        question.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )



    @action(detail=False,methods=["GET"])
    def search(self,request):
        name = request.GET.get("name",None)
        if not name:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
                )
        title = request.GET.get("title")
        contest_instance = get_object_or_404(Contests,name=name)

        instance = Contest_Question.objects.exclude(contest__id=contest_instance.id).filter(title__icontains=title)
        serialiazer = ContestQuestionsSerializer(instance,many=True)
        return Response(
            serialiazer.data,
            status=status.HTTP_200_OK
            )


    @action(detail=False,methods=["GET","POST","PUT"])
    def testcases(self,request):
        method = request.method
        if method == "POST":
            question_id = request.data.get("id",None)
            output = request.data.get("output",None)
            input = request.data.get("input",None)

            if not input and  not output:
                return Response(
                    {"detail":"input and output required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            

            question_instance = get_object_or_404(Contest_Question,pk=question_id)
            num_of_test_cases = question_instance.num_of_test_cases
            avaialabe_test_cases = SampleTestCases.objects.filter(question=question_instance).count()
            if num_of_test_cases <= avaialabe_test_cases // 2:
                return Response(
                    {"detail":"TestCases Has Already Been Uploaded"},
                    status=status.HTTP_400_BAD_REQUEST
                    )
            testCaseNames = {f"input{(avaialabe_test_cases+2)//2}":input,
                            f"output{(avaialabe_test_cases+2)//2}":output
            }
            for testCase in testCaseNames.keys():        
                instance  = SampleTestCases.objects.create(
                    question = question_instance,
                    name=testCase,
                    testCase=testCaseNames[testCase]
                )
                instance.save()
            deleteCachedQuestions(question_instance.title)
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )
        elif method == "PUT":
            question_id = request.data.get("question",None)
            id = request.data.get("id",None)
            input = request.data.get("input",None)
            output = request.data.get("output",None)
            instance = get_object_or_404(Contest_Question,id=id)
            if question_id and input and output:
                test_case = SampleTestCases.objects.filter(
                        Q(question__pk=question_id) & (Q(name=f"input{id}") | Q(name=f"output{id}"))
                )
                for test in test_case:
                    if test.name == f"input{id}":
                        test.testCase = input
                    else:
                        test.testCase = output
                    test.save()
                deleteCachedQuestions(instance.title)
                return Response(
                    status=status.HTTP_204_NO_CONTENT
                )
            else:
                return Response(
                    {"detail":"id,question,input,output required"},
                    status=status.HTTP_200_OK
                )
        
        elif method == "GET":
            question_id = request.GET.get("question",None)
            sample_id = request.GET.get("id",None)
            if question_id:
                question_instance = get_object_or_404(Contest_Question,pk=question_id)
                files_required = SampleTestCases.objects.filter(question=question_instance).count() < question_instance.num_of_test_cases
                if not sample_id:
                    return Response(
                        {"testCases":question_instance.num_of_test_cases,
                        "files_required":files_required
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    test_case = SampleTestCases.objects.filter(
                            Q(question__pk=question_id) & (Q(name=f"input{sample_id}") | Q(name=f"output{sample_id}"))
                    )
                    if not test_case:
                        return Response(
                            {"detail":"No TestCase with the given ID"},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    else:
                        serializer = SampleTestCaseSerializer(test_case,many=True)
                        return Response(
                            serializer.data,
                            status=status.HTTP_200_OK
                        )
            else:
                return Response(
                    {"detail":"question(question_id)required"},
                    status=status.HTTP_400_BAD_REQUEST
                )



"""A ViewSet For Crud Operation For On Constraints"""
class ConstraintViewSet(ModelViewSet):
    queryset = Constraints.objects.all()
    serializer_class = ConstraintsSerializer
    permission_classes = [IsSuperUserOrIsStaffUser]
    def list(self,request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

"""
These Are Not The Real Test Cases , These Are The Descriptive TestCases Which Will Be
Shown To User As An Introduction To The Problem
"""
class SampleTestCasesExampleViewSet(ModelViewSet):
    queryset = SampleTestCasesExample.objects.all()
    serializer_class = SampleTestCasesExampleSerializer
    permission_classes = [IsSuperUserOrIsStaffUser]


    def list(self,request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
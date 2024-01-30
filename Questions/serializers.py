from rest_framework import serializers
from .models import SampleTestCasesExample,Constraints,SampleTestCases
from Contest.models import Contest_Question


class ContestQuestionsSerializer(serializers.ModelSerializer):
    contest = serializers.SerializerMethodField()
    class Meta:
        model = Contest_Question
        fields = '__all__'
    def get_contest(self,obj):
        return obj.contest.name
    

class SampleTestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleTestCases
        fields = '__all__'


class SampleTestCasesExampleSerializer(serializers.ModelSerializer):
    sample = serializers.SerializerMethodField()
    answer = serializers.SerializerMethodField()
    explanation = serializers.SerializerMethodField()
    class Meta:
        model = SampleTestCasesExample
        fields = ['question','sample','answer','explanation']

    def get_sample(self,obj):
        return obj.sample.replace("\r\n","\n")

    def get_answer(self,obj):
        return obj.answer.replace("\r\n","\n")

    def get_explanation(self,obj):
        return obj.explanation.replace("\r\n","\n")

    
class ContestQuestionsCreatorSerializer(serializers.ModelSerializer):
    contest = serializers.SerializerMethodField()
    class Meta:
        model = Contest_Question
        fields = '__all__'
        required_fields = {"contest":{"required":False}}

    def get_contest(self,obj):
        return obj.contest.name


class ConstraintsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Constraints
        fields = "__all__"
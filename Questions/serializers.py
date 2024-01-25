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
    class Meta:
        model = SampleTestCasesExample
        fields = '__all__'

    
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
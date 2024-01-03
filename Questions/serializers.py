from rest_framework import serializers
from .models import sample_test_cases,Constraints
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
        model = sample_test_cases
        fields = '__all__'
class ContestQuestionsCreatorSerializer(serializers.ModelSerializer):
    contest = serializers.SerializerMethodField()
    class Meta:
        model = Contest_Question
        fields = '__all__'
        required_fields = {"contest":{"required":False}}

    def get_contest(self,obj):
        return obj.contest.name

    def create(self,validated_data):
        contest = self.context["contest"]
        validated_data["title"] = validated_data["title"].replace(" ","_")
        instance = Contest_Question.objects.create(
            contest = contest,
            **validated_data
        )
        return instance


class ConstraintsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Constraints
        fields = "__all__"
from .models import Contestants,Contests,Contest_Groups,Contest_Question,Contest_submissiosn
from rest_framework import serializers


class ContestGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest_Groups
        fields = '__all__'

class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contests
        fields = ["id","name","duration","starred"]



class ContestSubmissionSerializer(serializers.ModelSerializer):
    code = serializers.SerializerMethodField()
    group = serializers.SerializerMethodField()
    question = serializers.SerializerMethodField()
    class Meta:
        model = Contest_submissiosn
        fields = '__all__'

    def get_code(self,obj):
        return obj.code if self.context.get("showCode",None) else ""

    def get_question(self,obj):
        return obj.question.title
    def get_group(self,obj):
        return obj.group.group_name


class ContestQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest_Question
        fields = ["id","title","lvl","description","num_of_test_cases"]

class ContestantsSerializer(serializers.ModelSerializer):
    group = serializers.SerializerMethodField()
    class Meta:
        model = Contestants
        fields = ["id","name","group"]

    def get_group(self,obj):
        return obj.group.group_name
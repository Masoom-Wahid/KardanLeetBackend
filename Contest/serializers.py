from .models import Contestants,Contests,Contest_Groups,Contest_Question,Contest_submissiosn
from rest_framework import serializers



class CompetitionQuestionSerializer(serializers.ModelSerializer):
    solved = serializers.SerializerMethodField()
    class Meta:
        model = Contest_Question
        fields = ["id","solved","title","lvl","time_limit","point","description","num_of_test_cases"]


    def get_solved(self,obj):
        user = self.context["user"]
        group = user.contest_groups_set.all()[0]
        return Contest_submissiosn.objects.filter(group=group,solved=True,question=obj).exists()
        return result


class RetreiveQuestionSerializer(serializers.ModelSerializer):
    code = serializers.SerializerMethodField()
    class Meta:
        model = Contest_Question
        fields = ["id","code","title","lvl","time_limit","point","description","num_of_test_cases"]


    def get_code(self,obj):
        user = self.context["user"]
        group = user.contest_groups_set.all()[0]
        solvedSubmission = Contest_submissiosn.objects.filter(group=group,solved=True,question=obj)
        if solvedSubmission:
            for submission in solvedSubmission:
                return submission.code
        else:
            return ""

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
        fields = ["id","title","lvl","time_limit","point","description","num_of_test_cases"]

class ContestantsSerializer(serializers.ModelSerializer):
    group = serializers.SerializerMethodField()
    class Meta:
        model = Contestants
        fields = ["id","name","group"]

    def get_group(self,obj):
        return obj.group.group_name
from .models import Contestants,Contests,Contest_Groups
from rest_framework import serializers


class ContestGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest_Groups
        fields = '__all__'

class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contests
        fields = ["id","name","duration","starred"]

class ContestantsSerializer(serializers.ModelSerializer):
    group = serializers.SerializerMethodField()
    class Meta:
        model = Contestants
        fields = ["id","name","group","starred"]

    def get_group(self,obj):
        return obj.group.group_name
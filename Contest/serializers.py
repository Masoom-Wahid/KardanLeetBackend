from .models import Contestants,Contests
from rest_framework import serializers


class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contests
        fields = ["id","name","duration"]

class ContestantsSerializer(serializers.ModelSerializer):
    group = serializers.SerializerMethodField()
    class Meta:
        model = Contestants
        fields = ["id","name","group"]

    def get_group(self,obj):
        return obj.group.group_name
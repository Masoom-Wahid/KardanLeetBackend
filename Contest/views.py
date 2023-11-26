from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import ContestantsSerializer,ContestSerializer,ContestGroupSerializer
from rest_framework.permissions import IsAdminUser , IsAuthenticated
from rest_framework import status
from .models import Contests,Contest_Groups,Contestants
from rest_framework.decorators import action
from .utils import create_folder_for_contest,delete_folder_for_contest

class ContestViewSet(ModelViewSet):
    queryset = Contests.objects.all()
    serializer_class = ContestSerializer

    def get_permissions(self):
        if self.action in ["create","list","retreive","destroy"]:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]

        return (permission() for permission in permission_classes)


    def create(self,request,*args,**kwargs):
        request.data["name"] = request.data["name"].replace(" ","_")
        serializer = ContestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        create_folder_for_contest(instance.name)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
    def destroy(self,request,pk=None):
        instance = self.get_object()
        delete_folder_for_contest(instance.name)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False,methods=["POST"])
    def star_contest(self,request):
        contest_name = request.data.get("name",None)
        typeof = request.data.get("type",None)
        if contest_name and typeof:
            try:
                contest = Contests.objects.get(name=contest_name)
            except Contests.DoesNotExist:
                return Response(
                    {"detail":"Invalid Contest Name"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if typeof == "star":
                if Contests.objects.filter(starred=True).exists():
                    return Response(
                        {"detail":"an starred contest already exists"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    contest.starred = True
                    contest.save()
                    return Response(
                    status=status.HTTP_204_NO_CONTENT
                    )
            elif typeof == "unstar":
                contest.starred = False
                contest.save()
                return Response(
                    status=status.HTTP_204_NO_CONTENT
                )
            else:
                return Response(
                    {"detail":"Invalid Type"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            pass
    
    @action(detail=False,methods=["POST"])
    def groups(self,request):
        contest_name = request.data.get("name",None)
        if contest_name:
            try:
                contest = Contests.objects.get(name=contest_name)
            except:
                return Response(
                    {"detail":"Invalid Contest Name"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            instance = Contest_Groups.objects.filter(contest=contest)
            serializer = ContestGroupSerializer(instance,many=True)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        else:
            return Response(
                {"detail":"id param required"},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False,methods=["GET","POST","DELETE"])
    def contestants(self,request):
        method = request.method
        if method == "GET":
            group_id = request.GET.get("group_id",None)
            if group_id:
                try:
                    group = Contest_Groups.objects.get(id=group_id)
                except Contest_Groups.DoesNotExist:
                    return Response(
                        {"detail":"Invalid ID"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                instance = Contestants.objects.filter(group=group)
                serializer = ContestantsSerializer(instance,many=True)
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
            else:
                pass
        if method == "POST":
            group_id = request.data.get("group_id",None)
            name = request.data.get("name",None)
            if not group_id or not name:
                return Response(
                        {"detail":"Group_id and name required"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                try:
                    instance = Contest_Groups.objects.get(id=group_id)
                except Contest_Groups.DoesNotExist:
                    return Response(
                        {"detail":"Invalid ID"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                contest_instance = Contestants.objects.create(
                    group = instance,
                    name=name
                )
                serializer = ContestantsSerializer(contest_instance,many=False)
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
        if method == "DELETE":
            conetsant_id = request.data.get("id",None)
            if conetsant_id != None:
                try:
                    instance = Contestants.objects.get(id=conetsant_id)
                except Contestants.DoesNotExist:
                    return Response(
                        {"detail":"Invalid ID"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                instance.delete()
                return Response(
                    {"detail":"ok"},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"detail":"id required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
    
    

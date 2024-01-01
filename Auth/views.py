from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from .serializers import UserSerializer
from Contest.serializers import ContestantsSerializer
from .permissions import IsSuperUserOrIsStaffUser
from rest_framework import status
from Contest.models import Contests,Contest_Groups,Contestants
from rest_framework.permissions import AllowAny
from .utils import generate_user_for_contest
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUserOrIsStaffUser]

    def create(self,request,*args,**kwargs):
        typeof = request.data.get("type",None)
        if typeof != None:
            if typeof == "contest":
                amount = int(request.data.get("amount"))
                contest_id = request.data.get("contest_id")
                contest_instance = get_object_or_404(Contests,id=contest_id)
                startFrom = contest_instance.contest_groups_set.all().count() + 1
                passwords = generate_user_for_contest(amount,startFrom,contest_instance.name,contest_instance)
                return Response(
                    passwords,
                    status=status.HTTP_201_CREATED
                )
                
            elif typeof == "normal":
                user_name = request.data.get("username",None)
                password = request.data.get("password",None)
                if user_name == None or password == None:
                    return Response(
                        {"detail":"Username and password required"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                instance = User.objects.create(
                    username = user_name,
                    email = f"{user_name}@email.com"
                )
                instance.is_superuser = True
                instance.is_staff = True
                instance.is_active = True
                instance.set_password(password)
                instance.save()
                serializer = UserSerializer(instance,many=False)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return  Response(
                    {"detail":"Invalid Type => (contest,normal)"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"detail":"type required"},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False,methods=["POST"])
    def alias(self,request):
        username = request.data.get("username",None)
        given_alias = request.data.get("alias",None)
        if username and given_alias:
            user_instance = get_object_or_404(User,username=username)
            group_instance = Contest_Groups.objects.get(user=user_instance)
            group_instance.group_name = given_alias
            group_instance.save()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )
        else:
            return Response(
                {"detail":"username and alias required"},
                status=status.HTTP_400_BAD_REQUEST
            )

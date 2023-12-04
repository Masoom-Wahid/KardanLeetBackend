from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from .serializers import UserSerializer
from Contest.serializers import ContestantsSerializer
from .permissions import IsSuperUserOrIsStaffUser
from rest_framework import status
from Contest.models import Contests,Contest_Groups,Contestants
from .utils import generate_user_for_contest
from rest_framework.decorators import action

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
                try:
                    contest_instance = Contests.objects.get(id=contest_id)
                except:
                    return Response(
                        {"detail":"Invalid Contest ID"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                passwords = generate_user_for_contest(amount,contest_instance.name,contest_instance)
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



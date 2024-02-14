from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from .serializers import UserSerializer,MyTokenObtainPairSerializer
from Contest.serializers import ContestantsSerializer
from .permissions import IsSuperUserOrIsStaffUser
from rest_framework import status
from Contest.models import Contests,Contest_Groups,Contestants
from rest_framework.permissions import AllowAny
from .utils import generate_user_for_contest,read_file
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenViewBase
from math import ceil


class TokenObtainPairView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """

    serializer_class = MyTokenObtainPairSerializer

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
                passwords = generate_user_for_contest(amount,
                                                      startFrom,
                                                      contest_instance.name,
                                                      contest_instance,
                                                      )
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

    @action(detail=False,methods=["GET"])
    def getcredentials(self,request):
        """
        requires contest and page
        returns the username and password from the credentials.txt file
        """
        MAXIMUM_PER_PAGE_ALLOWED = 5
        contest_name = request.GET.get("contest",None)
        page = int(request.GET.get("page",1))
        if contest_name and page:
            contest_instance = get_object_or_404(Contests,name=contest_name)
            users_count = Contest_Groups.objects.filter(contest=contest_instance).count()
            pages_count = ceil(users_count/MAXIMUM_PER_PAGE_ALLOWED)
            if page > pages_count:
                return Response(
                    {"detail":f"Invalid Page,Avaiable Pages {pages_count}"}
                ) 
            result = read_file(contest_instance.key,contest_instance.name,page-1,users_count,MAXIMUM_PER_PAGE_ALLOWED)
            return Response(
                {
                    "avaialable_pages":f"{pages_count}",
                    "current_page":page,
                    "result":result
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"detail":"contest required"},
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

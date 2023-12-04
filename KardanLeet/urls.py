from django.contrib import admin
from django.urls import path,include

from rest_framework import routers

from Auth.views import UserViewSet
from Contest.views import ContestViewSet,CompetetionViewSet
from Questions.views import QuestionViewSet

router = routers.DefaultRouter()

router.register(r"auth/users", UserViewSet)
router.register(r"contest", ContestViewSet)
router.register(r"questions", QuestionViewSet)
router.register(r"competition",CompetetionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/auth/",include("Auth.urls")),
    path("api/",include(router.urls)),
    # path("api/competition/",include("Contest.urls"))
]

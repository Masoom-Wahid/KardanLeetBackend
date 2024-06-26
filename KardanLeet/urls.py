from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from rest_framework import routers

from Auth.views import UserViewSet
from Contest.views import ContestViewSet,CompetetionViewSet
from Questions.views import QuestionViewSet,ConstraintViewSet,SampleTestCasesExampleViewSet
router = routers.DefaultRouter()

router.register(r"auth/users", UserViewSet)
router.register(r"contest", ContestViewSet)
router.register(r"questions", QuestionViewSet)
router.register(r"competition",CompetetionViewSet)
router.register(r"constraints",ConstraintViewSet)
router.register(r"samples",SampleTestCasesExampleViewSet)


if settings.DEBUG:
    urlpatterns = [
        path('admin/', admin.site.urls),
        path("api/auth/",include("Auth.urls")),
        path("api/",include(router.urls)),
    ]
else:
    urlpatterns = [
        path("api/auth/",include("Auth.urls")),
        path("api/",include(router.urls)),
    ]    

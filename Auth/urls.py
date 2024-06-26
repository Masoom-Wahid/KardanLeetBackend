from django.urls import path
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .views import TokenObtainPairView

urlpatterns = [
    path("token/",TokenObtainPairView.as_view(),name="obtainToken"),
	path("token/refresh/",TokenRefreshView.as_view(),name="refreshToken"),
]
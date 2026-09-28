from rest_framework.routers  import DefaultRouter
from .views import UserViewSet, ProfileAPIView, ChangePasswordView
from django.urls import path, include 

router = DefaultRouter()

router.register(r"users", UserViewSet, basename='user')
urlpatterns = [
    path("", include(router.urls)),
    path("profile/", ProfileAPIView.as_view()),
    path("change/password/", ChangePasswordView.as_view()),
    
]
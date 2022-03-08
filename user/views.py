from rest_framework.generics import (
CreateAPIView,
UpdateAPIView,
DestroyAPIView,
RetrieveUpdateAPIView,
RetrieveAPIView,
RetrieveUpdateDestroyAPIView,
ListCreateAPIView,
)
from rest_framework import authentication, permissions  
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from .serializers import UserSerializer,AuthTokenSerializer



class CreateUserView(CreateAPIView):
  serializer_class=UserSerializer


class CreateAuthTokenView(ObtainAuthToken):
    serializer_class=AuthTokenSerializer
    renderer_classses = api_settings.DEFAULT_RENDERER_CLASSES


class MangeUserView(RetrieveUpdateAPIView):
  serializer_class=UserSerializer 
  authentication_classes = (authentication.TokenAuthentication,)
  permission_classes = (permissions.IsAuthenticated,)
  def get_object(self):
      return self.request.user
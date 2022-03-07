from rest_framework.generics import CreateAPIView,UpdateAPIView,DestroyAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from .serializers import UserSerializer,AuthTokenSerializer



class CreateUserView(CreateAPIView):
  serializer_class=UserSerializer


class CreateAuthTokenView(ObtainAuthToken):
    serializer_class=AuthTokenSerializer
    renderer_classses = api_settings.DEFAULT_RENDERER_CLASSES



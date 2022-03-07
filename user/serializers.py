from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate

from django.utils.translation import ugettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
  password=serializers.CharField(max_length=68,min_length=8,write_only=True)  
  class Meta :
    model = get_user_model()
    fields = ("email","name","password")
    extra_kwarg = {
      "password":{"write_only":True,"min_length":8}
    }
  def create(self, validated_data):
      user = get_user_model().objects.create_user(**validated_data)
      return user

class AuthTokenSerializer(serializers.Serializer):
  email = serializers.EmailField()
  password = serializers.CharField(min_length=8,trim_whitespace=False)
  
  def validate(self, attrs):
      email = attrs.get("email")
      password = attrs.get("password")
      user = authenticate(self.context.get("request"),username=email,password=password)
      if not user :
        error_message = _("not valid credentails")
        raise serializers.ValidationError(error_message,code='authentication')
      attrs['user']=user 
      return attrs

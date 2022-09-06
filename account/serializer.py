import re

from rest_framework import serializers, status
from rest_framework.response import Response
from django.core import exceptions
from .models import User
from .exception import CustomValidation

class RegistrationSerializer(serializers.ModelSerializer):
  password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
  class Meta:
    model = User
    fields=['email', 'first_name','last_name','user_type', 'password', 'password2', 'phoneno']
    extra_kwargs={
      'password':{'write_only':True}
    }

  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    if password != password2:
      raise CustomValidation('Password and Confirm Password fields are not matching','msg',status_code=status.HTTP_400_BAD_REQUEST)

    email = attrs.get('email')
    regex = r'\b[A-Za-z0-9._%+-]+@weagile+\.net\b'
    if not re.fullmatch(regex, email):
      raise CustomValidation("You are not authorized user,Please enter valid email id",'msg',status_code=status.HTTP_401_UNAUTHORIZED)


    pn=attrs.get('phoneno')
    if len(str(pn))!=10:
      raise CustomValidation("Mobile number should be 10 digit",'msg',status_code=status.HTTP_401_UNAUTHORIZED)
    return attrs

  def create(self, validate_data):
    return User.objects.create_user(**validate_data)


class LoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = User
    fields = ['email', 'password']
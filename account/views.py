from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core import serializers
from django.http import HttpResponse
from django.utils.encoding import force_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import authenticate
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from account.utils import Util
from .models import User
from .serializer import LoginSerializer, RegistrationSerializer


def verifymail(user,request):
  uid = urlsafe_base64_encode(force_bytes(user.id))
  token = PasswordResetTokenGenerator().make_token(user)
  current_site = get_current_site(request)
  domain=current_site.domain
  link = 'http://'+domain+'/account/validate/' + uid + '/' + token
  # Send EMail
  body = 'Click Following Link to verify your Account' + link
  data = {
    'subject': 'Validation Email ',
    'body': body,
    'to_email': user.email
  }
  Util.send_email(data)

#function to return token created using user credential
def get_tokens(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class RegistrationView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self,request,formate=None):
        serializer=RegistrationSerializer(data=request.data)
        if User.objects.filter(email=request.data['email']).exists():
            return Response({'msg': "User with this email is already exists", 'status': 'Fail','status_code': 602})

        if serializer.is_valid():
            user = serializer.save()
            # token = get_tokens(user)
            verifymail(user, request)
            return Response({ 'msg': 'Please verify your account','status':'Success','status_code':200}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([permissions.AllowAny,])
def validate(request,uid,token):
  try:
    id = smart_str(urlsafe_base64_decode(uid))
    user = User.objects.get(id=id)
    if not PasswordResetTokenGenerator().check_token(user, token):
      raise serializers.ValidationError('Token is not Valid or Expired')
    user.is_verified = True
    user.save()
    # return Response({'msg': 'Account is verified Please Login',})
    return HttpResponse('Account is verified Please Login')
  except DjangoUnicodeDecodeError as identifier:
    PasswordResetTokenGenerator().check_token(user, token)
    raise serializers.ValidationError('Token is not Valid or Expired')

class LoginView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens(user)
            if not user.is_verified:
                verifymail(user,request)
                return Response({'msg': 'Verfication is pending ,we have sent verification..','status':'Fail','status_code':199})
            name=str((User.objects.get(email=email)).first_name) + ' '+str((User.objects.get(email=email)).last_name)
            return Response({'token': token, 'name':name,'is_admin':(User.objects.get(email=email)).is_admin,'msg': 'Login Success','status_code':200}, status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'Email or Password is not Valid','status':'Fail','status_code':601})

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from rest_framework import status
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework import permissions
from . serializer import TokenSerializer, UserSerializer
from rest_framework import generics
from rest_framework.views import APIView
# Create your views here.


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class LoginView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            serializer = TokenSerializer(data={
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)



### User Profile Api
class UserProfile(APIView):
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()

    def get(self,request):
        emailId = request.GET['email']
        userList = User.objects.all()
        serializer = UserSerializer(userList,many=True)
        return Response(serializer.data)
        # return Response({"username":"vishal"})



class MyUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(label='Your name')
    city = forms.CharField(label='Your city')

    class Meta:
        model = User
        fields = ("username","name","city", "email", "password1", "password2")

def register(request):
    if request.method=="GET":
        form = MyUserForm()
        return render(request,'registration/register.html',{'form':form})
    elif request.method=="POST":
        form = MyUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')

    return render(request, 'registration/register.html', {'form':form})

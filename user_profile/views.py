from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from user_profile.serializers import (
    UserLoginSerializer,
    UserRegistrationSerializer,
    UserSerializer
)
from .models import User
from .user_service import AuthServiceV1
from .forms import UserRegisterForm, UserLoginForm
from user_profile.constants import Succes, Error

from django.views import View

class UserRegisterView(View):
    def post(self, request):
        return AuthServiceV1.register_user(request)

    def get(self, request):
        return AuthServiceV1.registeration_form(request)

class UserLoginView(View):
    def post(self, request):
        return AuthServiceV1.login_user(request)

    def get(self, request):
        return AuthServiceV1.get_login_form(request)



def register_user(request):
    if request.method == "POST":
        form = (request.POST)
        # check whether it's valid:
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                full_name=data.get("full_name"),
                email=data.get("email"),
                password=data.get("password"),
            )
            return redirect()
    else:
        return HttpResponseNotFound("Doesn't exist.")



def about(request):
    context = {
        "about":"active"
    }
    return render(
        request,
        "saved.html",
        context=context
    )


# class UserLoginView(APIView):

#     def post(self, request):
#         serializer = UserLoginSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             payload = serializer.validated_data
#             payload["user"] = UserSerializer(payload.get("user")).data
#             return Response(payload)
        
#         raise AuthenticationFailed(detail=Error.LOGIN_ERROR)


class UserRegistrationView(APIView):

    def post(self, request):
        serialzer = UserRegistrationSerializer(data=request.data)
        if serialzer.is_valid(raise_exception=True):
            serialzer.save()
            response = {
                "message": Succes.USER_REGISTER
            }
            return Response(response)
        else:
            err = {
                "message" : Error.SOMETHING_HAPPENED
            }
            return Response(err, status=400)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated,]
    
    def get(self, request):
        user = request.user
        print(user)
        serializer = UserSerializer(user).data

        return Response(serializer)



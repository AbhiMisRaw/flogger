from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from user_profile.serializers import (
    UserLoginSerializer,
    UserRegistrationSerializer,
    UserSerializer
)
from user_profile.constants import Succes, Error


def about(request):
    context = {
        "about":"active"
    }
    return render(
        request,
        "saved.html",
        context=context
    )


class UserLoginView(APIView):

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            payload = serializer.validated_data
            payload["user"] = UserSerializer(payload.get("user")).data
            return Response(payload)
        
        raise AuthenticationFailed(detail=Error.LOGIN_ERROR)


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



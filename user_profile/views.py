from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth import logout
# from user_profile.serializers import (
#     UserLoginSerializer,
#     UserRegistrationSerializer,
#     UserSerializer
# )
from .models import User
from .user_service import AuthServiceV1, AuthServiceV2


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


class UserProfileTemplateView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return AuthServiceV1.get_profile(request)
        else:
            redirect("")


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
        "user_profile/about.html",
        context=context
    )


class UserLogoutView(View):
    
    def get(self, request):
        logout(request)
        return redirect('blog:home_page')

@method_decorator(csrf_exempt, name='dispatch')
class UserRegistrationAPIView(View):

    def post(self, request):
        return AuthServiceV2().register(request)

@method_decorator(csrf_exempt, name='dispatch')
class UserLoginAPIView(View):
    
    def post(self, request):
        return AuthServiceV2().login(request)


class UserProfileAPIView(View):
    
    def get(self, request):
        print(request.user)
        print(request.user.is_authenticated)
        if request.user.is_authenticated:
            user = request.user
            data = {
                "id":user.id,
                "full_name":user.full_name,
                "email":user.email
            }
        else:
            data ={
                "message":"Please login first."
            }
        return JsonResponse(data)
    



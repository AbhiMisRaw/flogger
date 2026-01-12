import json
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, get_user_model
from django import forms

from .forms import UserLoginForm, UserRegisterForm
from .constants import URL, Error

from utils import (
    JWTService,
    Error as ErrorResponse,
    Succes as SuccesResponse
)

User = get_user_model()


class AuthCoreService():

    @staticmethod
    def create_user(full_name: str, email: str, password: str):
        user = User.objects.create_user(
            full_name=full_name,
            email=email,
            password=password,
        )
        print(f"{user} is created...")
        return user
        # TODO logging


class AuthServiceV1():

    def get_login_form(request):
        form = UserLoginForm()
        context = {
            "form":form,
            "action":"login"
        }
        return render(request, "user_profile/auth-form.html", context=context)


    @staticmethod
    def registeration_form(request):
        if request.method == "GET":
            context = {
                "form" : UserRegisterForm(),
                "action": "register",
            }
            return render(request, "user_profile/auth-form.html", context=context)
    

    @staticmethod
    def validate_form(data: dict, form_class: forms.Form):
        form = form_class(data)
        if form.is_valid():
            return form, True
        
        return form, False


    @staticmethod
    def register_user(request):
        context = {
            "action": "register",
        }
        _body = request.POST
        print(_body)
    
        form, is_valid = AuthServiceV1.validate_form(
            _body,
            UserRegisterForm
        )
        
        if is_valid == False:
            context["form"] = form
            return render(
                request,
                "user_profile/auth-form.html",
                context
            )
        
        if User.objects.filter(email=form.cleaned_data["email"]).exists():
            form.add_error("email", )
            context["form"] = form
            return render(
                request,
                "user_profile/auth-form.html",
                context
            )
        
        data = form.cleaned_data
        User.objects.create_user(
            full_name=data.get("full_name"),
            email=data.get("email"),
            password=data.get("password"),
        )
        return redirect(to=URL.LOGIN)


    @staticmethod
    def login_user(request):
        _body = request.POST
        form, is_valid = AuthServiceV1.validate_form(_body, UserLoginForm)

        if not is_valid:
            return render(
                request,
                "user_profile/auth-form.html",
                {
                    "form": form,
                    "action": "login",
                },
            )
        
        user = authenticate(
            request,
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password"],
        )

        if user is None:
            form.add_error(None, Error.LOGIN_ERROR)
            return render(
                request,
                "user_profile/auth-form.html",
                {
                    "form": form,
                    "action": "login",
                },
            )

        login(request, user)
        return redirect("/flog/homepage")
    

class AuthServiceV2():


    def login(self, request):
        body = json.loads(request.body)

        email = body.get("email")
        password = body.get("password")

        if not email or not password:
            return ErrorResponse.send(
                Error.LOGIN_ERROR
            )
        
        user = authenticate(
            request,
            email=email,
            password=password
        )

        if user:
            data = {
                "access": str(JWTService.create_access_token(user)),
                "refresh": str(JWTService.create_refresh_token(user)),
                "user": str(user.email),
            }
            return SuccesResponse.send(data)
        else:
            return ErrorResponse.send(
                Error.LOGIN_ERROR,
                status_code=401
            )

    def register(self, request):
        body = json.loads(request.body)

        full_name = body.get("full_name")
        email = body.get("email")
        password = body.get("password")
        confirm_password = body.get("password")

        if password != confirm_password:
            return ErrorResponse.send(
                Error.PASSWORD_MATCHING_ERROR
            )
        
        _ = AuthCoreService().create_user(
            full_name,
            email,
            password
        )
        data = {
            "message":"User is successfully registered."
        }
        return SuccesResponse.send(data, 201)

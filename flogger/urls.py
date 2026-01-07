from http import HTTPStatus
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
from django.http import JsonResponse


def health_check(request):
    response = {"status":"OK"}
    return JsonResponse(response, status=HTTPStatus.OK)

def redirect_to_home(request):
    return redirect("blog:home_page")

urlpatterns = [
    path("", redirect_to_home),
    path('flog/devi/admin/', admin.site.urls),
    path("health/", health_check),
    path("about/", health_check),
    path("auth/flog/", include(("user_profile.urls", "user_profile"))),
    path("flog/", include(("blog.urls", "blog"))),
]

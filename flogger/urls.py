
from django.contrib import admin
from django.urls import path, include
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(["GET"])
def health_check(request):
    response = {"status":"OK"}
    return Response(response)

urlpatterns = [
    path('flog/devi/admin/', admin.site.urls),
    path("health/", health_check),
    path("about/", health_check),
    path("auth/flog/", include(("user_profile.urls", "user_profile"))),
    path("flog/", include(("blog.urls", "blog"))),
]

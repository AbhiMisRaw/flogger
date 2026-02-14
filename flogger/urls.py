from http import HTTPStatus
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
from django.shortcuts import render


def health_check(request):
    response = {"status":"OK"}
    return JsonResponse(response, status=HTTPStatus.OK)

def redirect_to_home(request):
    return redirect("blog:home_page")

def custom_404(request, exception):
    return render(request, "errors/404.html", status=404)

def custom_500(request):
    return render(request, "errors/500.html", status=500)

urlpatterns = [
    path("", redirect_to_home, name="home"),
    path('flog/devi/admin/', admin.site.urls),
    path("health/", health_check),
    path("about/", health_check),
    path("auth/flog/", include(("user_profile.urls", "user_profile"))),
    path("flog/", include(("blog.urls", "blog"))),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]


handler404 = "flogger.urls.custom_404"
handler500 = "flogger.urls.custom_500"
from django.urls import path
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )
from .views import (
    UserLoginView,
    UserRegisterView,
    UserProfileTemplateView,
    UserLogoutView,
    UserRegistrationAPIView,
    UserLoginAPIView,
    UserProfileAPIView,
    about,
)

url_view_patterns = [

    path(
        'login',
        UserLoginView.as_view(),
        name='login'
    ),
    path(
        'register',
        UserRegisterView.as_view(),
        name='register'
    ),
    path(
        'logout',
        UserLogoutView.as_view(),
        name='logout'
    ),
    path(
        'user/profile',
        UserProfileTemplateView.as_view(),
        name="profile"
    ),
    path(
        'about',
        about,
        name="about"
    )
]

url_api_patterns = [
    path(
        'api/v1/register',
        UserRegistrationAPIView.as_view(),
        name="register_api"
    ),
    path(
        'api/v1/login',
        UserLoginAPIView.as_view(),
        name="login_api"
    ),
]

urlpatterns = (url_view_patterns + url_api_patterns)
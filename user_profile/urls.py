from django.urls import path
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )
from .views import (
    UserLoginView,
    UserRegisterView,
    UserProfileView,
    UserLogoutView,
    about,
)

urlpatterns = [

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
        'profile',
        UserProfileView.as_view(),
        name="profile"
    ),
    path(
        'about',
        about,
        name="about"
    )
]
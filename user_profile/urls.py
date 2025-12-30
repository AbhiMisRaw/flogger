from django.urls import path
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )
from .views import (
    UserLoginView,
    UserRegistrationView,
    UserRegisterView,
    UserProfileView,
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
        'profile',
        UserProfileView.as_view(),
        name="profile"
    ),
]
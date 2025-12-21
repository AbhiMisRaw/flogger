from django.urls import path
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )
from .views import (
    UserLoginView,
    UserRegistrationView,
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
        UserRegistrationView.as_view(),
        name='token_refresh'
    ),
    path(
        'profile',
        UserProfileView.as_view(),
        name="profile"
    ),
]
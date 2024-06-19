from django.urls import path
from users.apps import UsersConfig
from users.views import UserLoginView, UserLogoutView, UserRegisterView, email_verification, UserUpdateView, \
    UserPasswordResetView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('confirm-email/<str:token>/', email_verification, name='confirm-email'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('recovery/', UserPasswordResetView.as_view(), name='recovery'),
]

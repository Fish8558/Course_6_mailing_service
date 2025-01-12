from django.urls import path
from users.apps import UsersConfig
from users.views import UserLoginView, UserLogoutView, UserRegisterView, email_verification, UserUpdateView, \
    UserPasswordResetView, UserListView, toggle_activiti

app_name = UsersConfig.name

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('confirm-email/<str:token>/', email_verification, name='confirm-email'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('recovery/', UserPasswordResetView.as_view(), name='recovery'),
    path('', UserListView.as_view(), name='user_list'),
    path('toggle_activiti/<int:pk>', toggle_activiti, name='toggle_activiti')
]

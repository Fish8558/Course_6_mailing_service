import secrets
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from config.settings import EMAIL_HOST_USER
from main.utils import make_random_password
from users.forms import LoginForm, RegisterForm, UserForm, RecoveryForm
from users.models import User


class UserLoginView(LoginView):
    """Контроллер авторизации пользователя"""
    form_class = LoginForm
    template_name = 'users/login.html'


class UserLogoutView(LogoutView):
    """Контроллер выхода пользователя"""
    pass


class UserRegisterView(CreateView):
    """Контроллер регистрации пользователя"""
    model = User
    form_class = RegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(15)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/confirm-email/{token}/'
        try:
            send_mail(
                subject="Верификация почты на сайте MailingService",
                message=f"Доброго времени суток! "
                        f"Для подтверждения регистрации на сайте MailingService перейдите по ссылки {url}",
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email]
            )
        except Exception:
            print(f"Ошибка при отправке письма верификации")
        return super().form_valid(form)


def email_verification(request, token):
    """Контроллер подтверждения регистрации пользователя"""
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class UserUpdateView(UpdateView):
    """Контроллер редактирования пользователя"""
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordResetView(PasswordResetView):
    """Контроллер смены пароля пользователя"""
    form_class = RecoveryForm
    template_name = 'users/recovery_form.html'

    def form_valid(self, form):
        if self.request.method == 'POST':
            user_email = self.request.POST['email']
            user = User.objects.filter(email=user_email).first()
            if user:
                password = make_random_password()
                user.set_password(password)
                user.save()
                try:
                    send_mail(
                        subject="Восстановление пароля на сайте MailingService",
                        message=f"Доброго времени суток! "
                                f"Ваш пароль для доступа на сайт MailingService изменен:\n"
                                f"Данные для входа:\n"
                                f"Email: {user_email}\n"
                                f"Пароль: {password}",
                        from_email=EMAIL_HOST_USER,
                        recipient_list=[user.email]
                    )
                except Exception:
                    print(f"Ошибка при отправке пароля юзеру: ({user=}), на email: {user_email}")
            return HttpResponseRedirect(reverse('users:login'))
        return super().form_valid(form)

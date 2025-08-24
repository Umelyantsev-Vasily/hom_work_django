from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegistrationForm
from .models import User


def register(request):
    if request.user.is_authenticated:
        return redirect('catalog:home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Автоматически логиним пользователя после регистрации
            login(request, user)

            # Отправка приветственного письма
            send_welcome_email(user)

            messages.success(
                request,
                _('Регистрация прошла успешно!.')
            )
            return redirect('catalog:home')
    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'form': form})


def send_welcome_email(user):
    subject = _('Добро пожаловать на наш сайт!')
    message = _(
        f'Привет {user.email}!\n\n'
        'Спасибо за регистрацию в нашем приложении. '
        'Мы рады видеть вас среди наших пользователей!\n\n'
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    try:
        send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        # Логируем ошибку, но не прерываем процесс регистрации
        print(f"Error sending welcome email: {e}")
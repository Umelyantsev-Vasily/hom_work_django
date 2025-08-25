from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import CreateView
from .forms import UserRegistrationForm
from .models import User


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = 'catalog:home'

    def form_valid(self, form):
        """Переопределяем метод form_valid для отправки приветственного письма"""
        response = super().form_valid(form)
        user = form.save()

        # Автоматически логиним пользователя после регистрации
        login(self.request, user)

        # Отправка приветственного письма
        self.send_welcome_email(user)

        messages.success(
            self.request,
            _('Registration successful! Welcome email sent.')
        )
        return response

    def send_welcome_email(self, user):
        subject = _('Welcome to our service!')
        message = _(
            f'Hello {user.email}!\n\n'
            'Thank you for registering in our service. '
            'We are glad to see you among our users!\n\n'
            'Best regards,\nYour Team'
        )
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]

        try:
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            # Логируем ошибку, но не прерываем процесс регистрации
            print(f"Error sending welcome email: {e}")


# Оставляем и функцию register для обратной совместимости
def register(request):
    if request.user.is_authenticated:
        return redirect('catalog:home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Отправка приветственного письма
            send_welcome_email(user)

            messages.success(request, _('Registration successful!'))
            return redirect('catalog:home')
    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'form': form})


def send_welcome_email(user):
    subject = _('Welcome to our service!')
    message = _(
        f'Hello {user.email}!\n\n'
        'Thank you for registering in our service. '
        'We are glad to see you among our users!\n\n'
        'Best regards,\nYour Team'
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    try:
        send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        print(f"Error sending welcome email: {e}")
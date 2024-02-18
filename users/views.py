from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.db import transaction
from django.forms import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.hashers import make_password

from users.forms import UserLoginForm, UserRegistrationForm, UserSettingsForm
from users.models import User, UserSettings
from users.utils import get_or_create_user_settings, check_password



def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            #TODO сделать проверки для тестирования
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = None
            if user:
                settings = get_or_create_user_settings(user)

                correct_password, must_update = check_password(
                    password=password,
                    encoded=user.password,
                    hasher=settings.preferred_hash_algorithm,
                )
                if must_update:
                    user.password = make_password(password=password, salt=user.email, hasher=settings.preferred_hash_algorithm)
                    user.save()

                if correct_password:
                    auth.login(request, user)
                    if request.POST.get("next", None):
                        return HttpResponseRedirect(request.POST.get("next"))
                    return HttpResponseRedirect(reverse("vault:vault"))
    else:
        form = UserLoginForm()

    context = {
        "title": "Авторизация",
        "form": form,
    }
    return render(request, "users/login.html", context)


def registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            get_or_create_user_settings(user)
            auth.login(request, user)
            messages.success(request, f"{user.username}, Вы успешно зарегистрировались")
            return HttpResponseRedirect(reverse("vault:vault"))
    else:
        form = UserRegistrationForm()
    context = {
        "title": "Регистрация",
        "form": form,
    }
    return render(request, "users/registration.html", context)


@login_required
def settings(request):
    if request.method == "POST":
        form = UserSettingsForm(data=request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = request.user
                    user.username = form.cleaned_data["username"]
                    user.email = form.cleaned_data["email"]
                    user.save()
                    settings = get_or_create_user_settings(user=user)
                    settings.preferred_hash_algorithm = form.cleaned_data[
                        "hash_algorithm"
                    ]
                    settings.save()
            except ValidationError:
                return redirect("user:settings")

    else:
        settings = get_or_create_user_settings(user=request.user)
        form = UserSettingsForm(
            initial={
                "username": request.user.username,
                "email": request.user.email,
                "settings": settings,
            }
        )

    context = {
        "title": "Профиль",
        "form": form,
    }
    return render(request, "users/settings.html", context)


@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, Вы вышли из аккаунта")
    auth.logout(request)
    return redirect(reverse("vault:vault"))


@login_required
def delete(request):
    user = User.objects.get(id=request.user.id)
    user.delete()
    return HttpResponseRedirect(reverse("vault:vault"))

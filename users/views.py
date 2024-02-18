from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.db import transaction
from django.forms import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from users.forms import UserLoginForm, UserRegistrationForm, UserSettingsForm
from users.models import User, UserSettings
from users.utils import get_or_create_user_settings


def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)
            if user:
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
                    settings.preferred_hash_algorithm=form.cleaned_data["hash_algorithm"]
                    settings.save()
            except ValidationError:
                return redirect("user:settings")

    else:
        form = UserSettingsForm(initial={
            "username": request.user.username,
            "email": request.user.email,
        })

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

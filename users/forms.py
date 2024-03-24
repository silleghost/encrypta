from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.hashers import make_password

from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email

from users.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField()

    class Meta:
        model = User
        fields = ["username", "password"]


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        # exclude = ["username", "email", "password1", "password2"]

    username = forms.CharField()
    email = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()

    def clean_username(self):
        return self.cleaned_data["username"]

    def clean_email(self):
        return self.cleaned_data["email"]

    def clean_password1(self):
        return self.cleaned_data["password1"]

    def clean_password2(self):
        return self.cleaned_data["password2"]

    def clean(self):
        cleaned_data = super().clean()
        self.errors.clear()
        return cleaned_data
    

    # def clean_username(self):
    #     username = self.cleaned_data["username"]
    #     if User.objects.filter(username__iexact=username).exists():
    #         raise forms.ValidationError(
    #             "Пользователь с таким именем уже существует", code="unique"
    #         )
    #     return username

    # def clean_email(self):
    #     email = self.cleaned_data["email"]
    #     try:
    #         validate_email(email)
    #     except:
    #         raise forms.ValidationError("Неправильный email", code="invalid")
    #     if User.objects.filter(email=email).exists():
    #         raise forms.ValidationError(
    #             "Пользователь с таким email уже существует", code="unique"
    #         )
    #     return email

    # def clean_password1(self):
    #     password1 = self.cleaned_data["password1"]
    #     try:
    #         validate_password(password1)
    #     except forms.ValidationError as error:
    #         raise forms.ValidationError(error.messages)
    #     return password1

    # def clean_password2(self):
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError("Пароли не совпадают")
    #     return password2




class UserSettingsForm(forms.Form):
    username = forms.CharField()
    email = forms.CharField()
    hash_algorithm = forms.ChoiceField(
        choices=[
            ("pbkdf2_sha256", "pbkdf2"),
            ("argon2", "argon"),
        ]
    )

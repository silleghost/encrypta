from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UserChangeForm,
)


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
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )

    username = forms.CharField()
    email = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()

#TODO удалить форму
# class UserProfileForm(UserChangeForm):
#     class Meta:
#         model = User
#         fields = (
#             "username",
#             "email",
#         )

#     username = forms.CharField()
#     email = forms.CharField()


class UserSettingsForm(forms.Form):
    username = forms.CharField()
    email = forms.CharField()
    hash_algorithm = forms.ChoiceField(
        choices=[
            ("pbkdf2_sha256", "pbkdf2"),
            ("argon2", "argon"),
        ]
    )



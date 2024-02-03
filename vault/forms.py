from unicodedata import category
from django import forms


from vault.models import Records, Categories


class NewRecordForm(forms.ModelForm):
    class Meta:
        model = Records
        fields = (
            "app_name",
            "username",
            "password",
            "url",
        )

    app_name = forms.CharField()
    username = forms.CharField(required=False)
    password = forms.CharField(required=False)
    url = forms.CharField(required=False)



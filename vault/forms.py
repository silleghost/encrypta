from unicodedata import category
from django import forms


from vault.models import Passwords, Records


class NewRecordForm(forms.ModelForm):
    class Meta:
        model = Records
        fields = (
            "app_name",
            "favicon",
            "urls",
            "records",
            "category",
            "notes",
        )

    app_name = forms.CharField()
    favicon=forms.ImageField()
    urls=forms.JSONField()
    records=forms.CharField()
    category=forms.CharField()
    notes=forms.Textarea()



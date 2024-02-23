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
    


class NewCategoryForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ("name",)

    name = forms.CharField()

    def clean_name(self):
        data= self.cleaned_data["name"]
        if Categories.objects.filter(name=data).exists():
            raise forms.ValidationError("Такая категория уже существует", code="unique")
        
        return data

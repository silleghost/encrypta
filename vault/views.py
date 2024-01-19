from django.http import HttpResponse
from django.shortcuts import render

from vault.models import Records

# Create your views here.
def vault(request):
    records = Records.objects.all()
    context = {
        "title": "Главная",
        "records": records,
    }
    return render(request, "vault/base.html", context)

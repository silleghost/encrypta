from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def vault(request):
    return render(request, "vault/base.html")

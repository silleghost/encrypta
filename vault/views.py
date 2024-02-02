from ast import Pass
from unicodedata import category
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from vault.forms import NewRecordForm

from vault.models import Categories, Records

# Create your views here.
def vault(request):
    records = Records.objects.all()
    context = {
        "title": "Главная",
        "records": records,
    }
    return render(request, "vault/vault.html", context)


def save_new_record(request):
    if request.method == "POST":
        form = NewRecordForm(data=request.POST)
        post = form.save(commit=False)
        post.category = Categories.objects.get(name=request.POST["category"])
        post.save()

        return HttpResponseRedirect(reverse("vault:vault"))


    

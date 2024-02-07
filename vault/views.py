from asyncio.windows_events import NULL
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from vault.forms import NewRecordForm
from django.contrib.auth.decorators import login_required

from vault.models import Categories, Records

# Create your views here.
@login_required
def vault(request):
    records = Records.objects.filter(user=request.user)
    context = {
        "title": "Главная",
        "records": records,
    }
    return render(request, "vault/vault.html", context)


@login_required
def save_new_record(request):
    if request.method == "POST":
        form = NewRecordForm(data=request.POST)
        post = form.save(commit=False)
        post.user = request.user
        if request.POST["category"]:
            post.category = Categories.objects.filter(user=request.user).get(name=request.POST["category"])
        post.save()

        return HttpResponseRedirect(reverse("vault:vault"))
    
@login_required
def get_record_form(request):
    record_id = request.POST.get("record_id")
    record = Records.objects.get(id=record_id)

    change_form_html = render_to_string(
        "vault/change-record-form.html", {"record" : record}, request=request
    )

    response_data = {
        "change_form_html" : change_form_html,
    }

    return JsonResponse(response_data)


    

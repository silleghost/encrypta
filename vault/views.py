from django.core.cache import cache
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse
from vault.forms import NewCategoryForm, NewRecordForm
from django.contrib.auth.decorators import login_required

from vault.models import Categories, Records

@login_required
def vault(request):
    """
    Возвращает все записи текущего пользователя
    """
    master_encryption_key = request.session.get("master-encryption-key", None)
    if master_encryption_key:
        records = Records.objects.filter(user=request.user)
        master_encryption_key = master_encryption_key.encode("utf-8")
        for record in records:
            record.decrypt_data(master_encryption_key)

    context = {
        "title": "Главная",
        "records": records,
    }
    return render(request, "vault/vault.html", context)


@login_required
def save_record(request):
    """
    Сохраняет запись в базе данных
    """
    if request.method == "POST":
        record_id = request.POST.get("id", None)
        if record_id:
            record = get_object_or_404(Records, user=request.user, id=record_id)
            form = NewRecordForm(request.POST, instance=record)
        else:
            form = NewRecordForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            if request.POST.get("category"):
                post.category = get_object_or_404(
                    Categories, user=request.user, name=request.POST["category"]
                )
            encryption_key = request.session.get("master-encryption-key")
            encryption_key = encryption_key.encode("utf-8")
            post.encrypt_data(encryption_key)
            post.save()
            return HttpResponseRedirect(reverse("vault:vault"))
    return HttpResponseRedirect(reverse("vault:vault"))


@login_required
def get_record_form(request):
    """
    Получает данные выбранной записи по id и отправляет их по AJAX
    """
    record_id = request.POST.get("record_id")
    record = Records.objects.get(id=record_id)

    encryption_key = request.session.get("master-encryption-key")
    encryption_key = encryption_key.encode("utf-8")
    record.decrypt_data(encryption_key)

    change_form_html = render_to_string(
        "vault/edit-record-form.html", {"record": record}, request=request
    )

    response_data = {
        "change_form_html": change_form_html,
    }

    return JsonResponse(response_data)


@login_required
def delete_record(request):
    """
    Удаляет запись по id
    """
    if request.method == "POST":
        record = Records.objects.filter(user=request.user).get(
            id=request.POST.get("id")
        )
        record.delete()
    return HttpResponseRedirect(reverse("vault:vault"))


@login_required
def new_category(request):
    """
    Создает новую категорию
    """
    if request.method == "POST":
        form = NewCategoryForm(data=request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            cache_key = f"category_list_{request.user.id}"
            cache.delete(cache_key)
        else:
            # TODO Здесь необходимо вернуть перерисованную форму с сообщением об ошибке
            ...

    else:
        form = NewCategoryForm()

    return HttpResponseRedirect(reverse("vault:vault"))

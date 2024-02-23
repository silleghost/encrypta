from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from vault.forms import NewCategoryForm, NewRecordForm
from django.contrib.auth.decorators import login_required

from vault.models import Categories, Records
from vault.utils import decrypt, encrypt


@login_required
def vault(request):
    """
    Возвращает все записи текущего пользователя
    """
    master_encryption_key = request.session.get("master-encryption-key", None)
    if master_encryption_key:
        master_encryption_key = master_encryption_key.encode("utf-8")
        records = Records.objects.filter(user=request.user)
        for record in records:
            record.app_name = decrypt(eval(record.app_name), master_encryption_key).decode("utf-8")
            record.username = decrypt(eval(record.username), master_encryption_key).decode("utf-8")
            record.password = decrypt(eval(record.password), master_encryption_key).decode("utf-8")
            record.url = decrypt(eval(record.url), master_encryption_key).decode("utf-8")


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
            post.app_name = encrypt(post.app_name, encryption_key)
            post.username = encrypt(post.username, encryption_key)
            post.password = encrypt(post.password, encryption_key)
            post.url = encrypt(post.url, encryption_key)
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
        else:
            # TODO Здесь необходимо вернуть перерисованную форму с сообщением об ошибке
            ...

    else:
        form = NewCategoryForm()

    return HttpResponseRedirect(reverse("vault:vault"))

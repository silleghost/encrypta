from django.contrib import admin

from vault.models import Categories, Records


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    pass


@admin.register(Records)
class RecordsAdmin(admin.ModelAdmin):
    pass

from django.contrib import admin

from users.models import User, UserSettings

# Register your models here.
admin.site.register(User)
admin.site.register(UserSettings)

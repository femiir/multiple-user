from django.contrib import admin
from .models import User, Roles, Business, Client
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Roles)
admin.site.register(Business)
admin.site.register(Client)

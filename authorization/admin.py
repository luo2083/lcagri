from django.contrib import admin
from .models import User

@admin.register(User)
class AuthorizationUserAdmin(admin.ModelAdmin):
    exclude = ['open_id']
from django.contrib import admin
from .models import Profile, WebRequest


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user']


admin.site.register(WebRequest)

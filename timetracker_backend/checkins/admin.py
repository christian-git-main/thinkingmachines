from django.contrib import admin
from .models import CheckIn
# Register your models here.
@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'hours', 'tag', 'activities', 'created_at']
    search_fields = ['user__username', 'tag', 'activities']
    list_filter = ['created_at']

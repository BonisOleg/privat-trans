from django.contrib import admin
from unfold.admin import ModelAdmin

from src.leads.models import Lead


@admin.register(Lead)
class LeadAdmin(ModelAdmin):
    list_display = ("name", "phone", "from_city", "to_city", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("name", "phone", "email")
    readonly_fields = ("created_at",)

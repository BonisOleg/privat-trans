from django.contrib import admin
from unfold.admin import ModelAdmin

from src.leads.models import Lead


@admin.register(Lead)
class LeadAdmin(ModelAdmin):
    list_display = ("name", "phone", "from_city", "from_country", "to_city", "to_country", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("name", "phone", "email", "from_city", "from_country", "to_city", "to_country")
    readonly_fields = ("created_at",)

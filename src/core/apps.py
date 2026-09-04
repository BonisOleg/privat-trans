from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.core"
    verbose_name = "Налаштування сайту"

    def ready(self):
        from django.contrib import admin

        admin.site.site_header = "ПРИВАТ-ТРАНС CMS"
        admin.site.site_title = "ПРИВАТ-ТРАНС"
        admin.site.index_title = "Контент і заявки"

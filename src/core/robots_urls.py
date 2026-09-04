from django.urls import path

from src.core.robots import robots_txt

urlpatterns = [
    path("", robots_txt, name="robots_txt"),
]

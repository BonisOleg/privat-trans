from django.urls import path

from src.faq import views

app_name = "faq"

urlpatterns = [
    path("", views.faq_list, name="list"),
]

from django.urls import path

from src.calculator import views

app_name = "calculator"

urlpatterns = [
    path("", views.calculator_page, name="page"),
]

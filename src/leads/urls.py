from django.urls import path

from src.leads import views

app_name = "leads"

urlpatterns = [
    path("create/", views.create_lead, name="create"),
]

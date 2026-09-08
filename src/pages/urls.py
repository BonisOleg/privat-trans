from django.urls import path

from src.pages import views

app_name = "pages"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("fleet/", views.fleet, name="fleet"),
    path("contacts/", views.contacts, name="contacts"),
    path("privacy/", views.privacy, name="privacy"),
]

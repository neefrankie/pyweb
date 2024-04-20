from django.urls import path

from . import views

# namespace for url in template
app_name = "main"

urlpatterns = [
    path("", views.homepage, name="home"),
]
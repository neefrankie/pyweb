from django.urls import path

from . import views

# namespace for url in template
app_name = "orm"

urlpatterns = [
    path("users/create", views.create_user, name="create_user"),
    path("books/", views.IndexView.as_view(), name="books"),
    path("books/<int:pk>/", views.DetailView.as_view(), name="book_detail"),
]

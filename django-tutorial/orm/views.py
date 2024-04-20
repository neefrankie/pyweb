from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404
from django.views import generic

from .forms import UserForm
from .models import Book

# Create your views here.


def index(request):
    latest_book_list = Book.objects.order_by("-pub_date")[:5]
    context = {
        "latest_book_list": latest_book_list,
    }
    return render(request, "orm/index.html", context)


def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, "orm/detail.html", {"book": book})


class IndexView(generic.ListView):
    template_name = "orm/index.html"
    context_object_name = "latest_book_list"

    def get_queryset(self):
        return Book.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Book
    template_name = "orm/detail.html"


def create_user(request: HttpRequest):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

    else:
        form = UserForm()

    return render(request, "orm/create_user.html", {"form": form})
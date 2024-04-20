import decimal
import random
from datetime import date
from typing import List
from faker import Faker

from django.test import TestCase
from django.contrib.auth.models import User
from .models import Author, Publisher, Book

fake = Faker()


# Create your tests here.
def create_publisher() -> Publisher:
    return Publisher(
        name="The Beatles Publishing House"
    )


def create_authors() -> List[Author]:
    return [
        Author(
            name="John"
        ),
        Author(
            name="Paul"
        ),
        Author(
            name="George"
        ),
        Author(
            name="Ringo"
        )
    ]


def create_book(p: Publisher) -> Book:
    return Book(
        name=fake.name(),
        pages=random.randint(100, 100),
        price=decimal.Decimal(random.randrange(100, 1000))/100,
        publisher=p,
        pub_date=date.today(),
    )


class BlogModelTest(TestCase):

    def test_save_publisher(self):
        p = create_publisher()
        p.save()

        p.name = "New name"

        p.save()

    def test_save_entry(self):
        p = create_publisher()
        p.save()

        # Show how to save/update ForeignKey field.
        book = create_book(p)
        book.save()

        authors = create_authors()
        for a in authors:
            a.save()

        book.authors.add(*authors)

    def test_retrieve_blog(self):
        p = create_publisher()
        p.save()

        book1 = create_book(p)
        book1.save()

        book2 = create_book(p)
        book2.save()

        all_books = Book.objects.all()
        print(all_books)


class UserAuthTest(TestCase):
    def test_create_user(self):
        User.objects.create_user("john", "lennon@thebeatlbes.com", "johnpassword")
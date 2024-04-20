from datetime import date

from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=300)
    pages = models.IntegerField()
    price = models.DecimalField(max_length=10, max_digits=5, decimal_places=2)
    rating = models.FloatField(default=0)
    cover_image = models.TextField()
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    pub_date = models.DateField()
    mod_date = models.DateField(default=date.today)

    def __str__(self):
        return self.name

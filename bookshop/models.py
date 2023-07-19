from django.db import models
from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name="Genre")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

    def __str__(self):
        return self.name

class Book (models.Model):
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=False)
    genres = models.ManyToManyField(Genre, verbose_name="Géneros", blank=False)
    author = models.CharField(max_length=100, blank=False)
    available_from = models.DateField(auto_now_add=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to="bookshop", null=False, verbose_name="Imagen")

    class Meta:
        ordering = ['name']
        verbose_name = "Book"
        verbose_name_plural = "Books"
    
    def __str__(self):
        return self.name

    @admin.display(ordering='name')
    def pelicula(self):
        return format_html(
            '<span style="color: red;">{}</span>',
            self.name,
        )
    @admin.display(ordering='description')
    def resumen(self):
        return format_html(
            self.description
        )       

class Wishlist(models.Model):
    user = models.OneToOneField(User, related_name="user_wishlist", on_delete=models.CASCADE)
    books = models.ManyToManyField(Book, related_name="books_wishlist")

    def __str__(self):
        return self.user.username

from django.contrib import admin
from .models import Genre, Book

# Register your models here.
class GenreAdmin(admin.ModelAdmin):
    readonly_fields = ['created']
    
class BooksAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'description')     
    list_filter = ('genres', 'author')
    ordering = ('name', 'author')
    
admin.site.register(Genre, GenreAdmin)    
admin.site.register(Book, BooksAdmin)    

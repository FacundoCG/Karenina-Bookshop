from django import forms
from .models import Book, Genre
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        widgets = {
            "username": forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Username', 'autocomplete':'off'}),
            "email": forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'Email', 'autocomplete':'off'}),
            "password1": forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'}),
            "password2": forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Confirm password'}),
        }

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'autocomplete':'off'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class BookForm(forms.ModelForm):    
    class Meta:
        model = Book
        fields = ['name', 'description', 'genres', 'author', 'price', 'image']

        widgets = {
            "name": forms.TextInput(attrs={'class':'form-control', 'placeholder':'Book name', 'autocomplete':'off'}),
            "description": forms.Textarea(attrs={'class':'form-control', 'placeholder':'Descripción', 'id':'txt','onkeyup':'textAreaAdjust(this)'}),
            "genres":forms.SelectMultiple(attrs={'class':'form-control', 'placeholder':'Genres'}),
            "author": forms.TextInput(attrs={'class':'form-control', 'placeholder':'Author', 'autocomplete':'off'}),
            "price": forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Price', 'step': '0.01'}),
            "image":forms.FileInput(attrs={'class':'form-control', 'placeholder':'Cover'}),
        }

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']

        widgets = {
            "name": forms.TextInput(attrs={'class':'form-control', 'placeholder':'Genre name', 'autocomplete':'off'}),
        }
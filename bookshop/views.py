from django.shortcuts import render, redirect, get_object_or_404
from django.http import request
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

from .models import Book, Wishlist, Genre
from .forms import BookForm, GenreForm, SignUpForm, LoginForm

def is_admin(user):
    return user.is_superuser  

def signup(request):
    fields = ['password1' , 'password2']

    if request.method == 'POST':
        form = SignUpForm(request.POST)

        for field in fields:
            form.fields[field].widget.attrs['class'] = 'form-control'
            form.fields[field].widget.attrs['placeholder'] = 'Password'

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()

        for field in fields:
            form.fields[field].widget.attrs['class'] = 'form-control'
            form.fields[field].widget.attrs['placeholder'] = 'Password'

    print(form.non_field_errors)

    context = {'form': form}

    return render(request, 'bookshop/sign_up.html', context)

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index') 
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'bookshop/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('index') 

def index(request):
    search_query = request.GET.get('search-area', '')
    books_searched = Book.objects.filter(name__icontains=search_query)
    context = None
    books = Book.objects.all().order_by('pk')
    
    if len(books) == 0:
        pass
    elif len(books)>3:
        last_books = books[len(books)-3:]
        context = {'books':last_books, 'books_searched':books_searched, 'search_query':search_query}
    else: 
        context = {'books':last_books, 'books_searched':books_searched, 'search_query':search_query}

    return render(request, 'bookshop/index.html', context)

def books(request):
    selected_authors = request.GET.getlist('author')
    selected_genres = request.GET.getlist('genre')
    
    all_authors = Book.objects.values_list('author', flat=True).distinct()
    all_genres = Genre.objects.values_list('name', flat=True).distinct()
    
    books = Book.objects.all().order_by('name')
    
    if selected_authors:
        books = books.filter(author__in=selected_authors)
    
    if selected_genres:
        books = books.filter(genres__name__in=selected_genres)

    context = {
        'books': books,
        'selected_authors': selected_authors,
        'selected_genres': selected_genres,
        'all_authors': all_authors,
        'all_genres': all_genres,
    }

    return render(request, 'bookshop/books.html', context)

 

@login_required
@user_passes_test(is_admin)
def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('books')  
    else:
        form = BookForm()
    
    context = {'form': form}

    return render(request, 'bookshop/create_book.html', context)

@login_required
@user_passes_test(is_admin)
def create_genre(request):
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('books') 
    else:
        form = GenreForm()
    
    context = {'form': form}
    
    return render(request, 'bookshop/create_genre.html', context)

@login_required
@user_passes_test(is_admin)
def delete_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('books') 

@login_required
@user_passes_test(is_admin)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('detail_book', book_id = book.id) 
    else:
        form = BookForm(instance=book)
    
    for field_name, field_value in book.__dict__.items():
        if field_name in form.fields:
            form.fields[field_name].widget.attrs['value'] = field_value

    context = {'form': form}

    return render(request, 'bookshop/edit_book.html', context)

def detail_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    context = None
    
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user).first()
        if wishlist:
            wishlist_ids = wishlist.books.values_list('id', flat=True)
            context = {'book': book, 'wishlist_ids': wishlist_ids}
        else:
            context = {'book': book}
    else:
        context = {'book': book}

    return render(request, 'bookshop/detail_book.html', context)

@login_required
def wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user).first()
    context = None 
    if wishlist:
        books = wishlist.books.all()
        context = {'books': books}
    else:
        books = None
        context = {'books': books}

    return render(request, 'bookshop/wishlist.html', context)

@login_required
def add_to_wishlist(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    wishlist.books.add(book)

    return redirect('wishlist')

@login_required
def wishlist_remove(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    wishlist = get_object_or_404(Wishlist, user = request.user)

    wishlist.books.remove(book)
    
    return redirect('wishlist')

def about(request):
    return render(request, 'bookshop/about.html')
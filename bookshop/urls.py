from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("create_book", views.create_book, name="create_book"),
    path("create_genre", views.create_genre, name="create_genre"),
    path("books/", views.books, name="books"),
    path("books/<int:book_id>/", views.detail_book, name="detail_book"),
    path("books/<int:book_id>/delete", views.delete_book, name="delete_book"),
    path('books/<int:book_id>/edit', views.edit_book, name="edit_book"),
    path('books/<int:book_id>/add_wishlist', views.add_to_wishlist, name="add_wishlist"),
    path('wishlist', views.wishlist, name="wishlist"),
    path('wishlist/remove/<int:book_id>', views.wishlist_remove, name="wishlist_remove"),
    path('about', views.about, name="about"),
]
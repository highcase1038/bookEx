from django.urls import path
from . import views
from .views import add_to_favorites, remove_from_favorites, view_favorites


urlpatterns = [
    path('', views.index, name='index'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('book_detail/<int:book_id>', views.book_detail, name='book_detail'),
    path('book_delete/<int:book_id>', views.book_delete, name='book_delete'),
    path('postbook', views.postbook, name='postbook'),
    path('displaybooks', views.displaybooks, name='displaybooks'),
    path('mybooks', views.mybooks, name='mybooks'),
    path('search/', views.search_books, name='search_books'),
    path('add_to_favorites/<int:book_id>/', add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/<int:book_id>/', remove_from_favorites, name='remove_from_favorites'),
    path('favorites/', view_favorites, name='view_favorites'),
    path('requestbook', views.requestbook, name='requestbook'),
    path('displayusers', views.displayusers, name='displayusers'),
    path('user_detail/<int:user_id>', views.user_detail, name='user_detail'),
    path('myprofile', views.myprofile, name='myprofile'),
]

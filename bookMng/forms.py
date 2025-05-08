from django import forms
from django.forms import ModelForm#
from .models import Book, Comment, Rating, BookRequest


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = [
            'name',
            'web',
            'price',
            'picture',
        ]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment# Path: bookEx/bookMng/forms.py
        fields = ('text',)

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']
        widgets = {
            'score': forms.NumberInput(attrs={'min': '1', 'max': '10'})
        }

class BookRequestForm(forms.ModelForm):
    class Meta:
        model = BookRequest
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Book Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Why do you want this book?', 'rows': 4}),
        }
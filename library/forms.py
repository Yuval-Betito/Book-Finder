from django import forms
from .models import Book

class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'published_year', 'language', 'cover_image_url', 'original_language', 'genres']
        widgets = {
            'genres': forms.CheckboxSelectMultiple()
        }

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'published_year', 'language', 'cover_image_url']
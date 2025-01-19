from django.contrib.auth.models import User
from django.db import models


class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'genres'  # שם הטבלה הקיימת
        managed = False  # Django לא ינסה לנהל את הטבלה

    def __str__(self):
        return self.name


class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    published_year = models.IntegerField(blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    cover_image_url = models.URLField(max_length=500, blank=True, null=True)
    original_language = models.CharField(max_length=50, blank=True, null=True)
    genres = models.ManyToManyField(Genre, related_name="books", db_table="bookgenres")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = 'books'

    def __str__(self):
        return self.title



class FavoriteBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='favorited_by')
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'books_favoritebook'  # שם הטבלה בבסיס הנתונים

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"





class Review(models.Model):
    review_id = models.AutoField(primary_key=True)  # תואם לשדה הראשי בטבלה
    book = models.ForeignKey(
        'Book',
        on_delete=models.CASCADE,
        related_name='reviews',
        db_column='book_id'  # תואם לשם השדה בבסיס הנתונים
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        db_column='user_id'  # תואם לשם השדה בבסיס הנתונים
    )
    review_text = models.TextField(null=True, blank=True)  # מתיר ערכים ריקים
    rating = models.IntegerField(null=True, blank=True)  # מתיר ערכים ריקים
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reviews'  # שם הטבלה בבסיס הנתונים

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.rating})"





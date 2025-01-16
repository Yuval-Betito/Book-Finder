
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import send_mail
import uuid
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from django.shortcuts import  get_object_or_404
from django.http import HttpResponseNotFound
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from .forms import AddBookForm
from .models import Book, Genre, FavoriteBook
from django.contrib import admin
from django.db import IntegrityError
from django.utils.timezone import now
from datetime import timedelta

def welcome(request):
    return render(request, 'welcome.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_home')
        else:
            messages.error(request, "Invalid email or password.")
    return render(request, 'login.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            # חיפוש משתמש לפי האימייל
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # אם המשתמש לא נמצא
            messages.error(request, 'No user with this email exists.')
            return render(request, 'forgot_password.html')

        # יצירת טוקן ייחודי
        token = str(uuid.uuid4())

        # שליחת מייל עם הטוקן
        send_mail(
            'Reset Your Password',
            f'Here is your password reset token: {token}',
            'your-email@example.com',  # שימי פה את כתובת המייל שלך
            [email],
            fail_silently=False,
        )

        # שמירת האימייל והטוקן ב-Session
        request.session['reset_email'] = email
        request.session['reset_token'] = token

        messages.success(request, 'Reset token has been sent to your email.')
        return redirect('reset_password')  # מפנה לעמוד Reset Password

    return render(request, 'forgot_password.html')


def reset_password(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        new_password = request.POST.get('new_password')
        email = request.session.get('reset_email')

        if token == request.session.get('reset_token') and email:
            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)  # עדכון הסיסמה בצורה מאובטחת
                user.save()

                # ניקוי ה-Session לאחר האיפוס
                request.session.flush()
                messages.success(request, 'Your password has been reset successfully! Please log in.')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'No user with this email exists.')
        else:
            messages.error(request, 'Invalid token or email. Please try again.')

    return render(request, 'reset_password.html')

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # בדיקת סיסמאות
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')

        # יצירת משתמש חדש
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email is already registered.")
        else:
            User.objects.create_user(username=email, email=email, password=password)
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')  # מפנה לעמוד Login
    return render(request, 'register.html')


@login_required
def user_home(request):
    if request.user.is_staff:
        # מנהלים מופנים לדשבורד
        return redirect('admin_dashboard')

    # חיפוש ספרים לפי טופס חיפוש
    query = request.GET.get('q', '').strip()
    books = Book.objects.all()  # שאילתת בסיס

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(genres__name__icontains=query)
        ).distinct()

    # רשימת הספרים המועדפים של המשתמש
    favorite_books = Book.objects.filter(favorited_by__user=request.user)  # ספרים מועדפים

    return render(request, 'user_home.html', {
        'books': books,
        'favorite_books': favorite_books
    })




def guest_home(request):
    # חיפוש ספרים לפי טופס חיפוש
    query = request.GET.get('q', '').strip()
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(genres__name__icontains=query)
        ).distinct()
    else:
        books = Book.objects.all()
    return render(request, 'guest_home.html', {'books': books})






def book_detail(request, book_id):
    # שליפת הספר לפי book_id (לא id)
    book = get_object_or_404(Book, book_id=book_id)

    # רשימת ה-IDs של הספרים המועדפים על המשתמש
    user_favorite_books = []
    if request.user.is_authenticated:
        user_favorite_books = FavoriteBook.objects.filter(user=request.user).values_list('book_id', flat=True)

    return render(request, 'book_detail.html', {
        'book': book,
        'user_favorite_books': user_favorite_books,
    })



def search_books(request):
    query = request.GET.get('q', '').strip()
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(genres__name__icontains=query)
        ).distinct()
    else:
        books = Book.objects.all()
    return render(request, 'search_results.html', {'books': books, 'query': query})


from .forms import AddBookForm

@login_required
def add_book(request):
    if request.method == 'POST':
        form = AddBookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Book added successfully!")
            return redirect('user_home')
    else:
        form = AddBookForm()
    return render(request, 'add_book.html', {'form': form})



@login_required
def user_favorites(request):
    # שליפת הספרים המועדפים של המשתמש
    favorites = FavoriteBook.objects.filter(user=request.user).select_related('book')
    return render(request, 'user_favorites.html', {'favorites': favorites})


@login_required
def add_to_favorites(request, book_id):
    # בדיקה שהספר קיים בטבלה books
    book = get_object_or_404(Book, book_id=book_id)

    try:
        # הוספה למועדפים
        favorite, created = FavoriteBook.objects.get_or_create(user=request.user, book=book)
        if created:
            print("Book added to favorites.")
        else:
            print("Book is already in favorites.")
    except IntegrityError as e:
        print(f"Error adding book to favorites: {e}")  # טיפול במקרה של שגיאה

    return redirect('book_detail', book_id=book_id)


@login_required
def remove_from_favorites(request, book_id):
    # בדיקה שהספר קיים בטבלה books
    book = get_object_or_404(Book, book_id=book_id)

    try:
        # מחיקת הספר מרשימת המועדפים
        FavoriteBook.objects.filter(user=request.user, book=book).delete()
        print("Book removed from favorites.")
    except Exception as e:
        print(f"Error removing book from favorites: {e}")

    return redirect('user_favorites')
















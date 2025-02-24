
from django.contrib import messages
from django.core.mail import send_mail
import uuid
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.db.models import Q
from .forms import AddBookForm
from django.db import IntegrityError
from django.utils.timezone import now
from .models import FavoriteBook, Review
from django.shortcuts import render, redirect, get_object_or_404
from library.models import Book
from library.forms import BookForm
from django.contrib.auth.decorators import user_passes_test

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

            user = User.objects.get(email=email)
        except User.DoesNotExist:

            messages.error(request, 'No user with this email exists.')
            return render(request, 'forgot_password.html')

        token = str(uuid.uuid4())

        send_mail(
            'Reset Your Password',
            f'Here is your password reset token: {token}',
            'your-email@example.com',
            [email],
            fail_silently=False,
        )

        request.session['reset_email'] = email
        request.session['reset_token'] = token

        messages.success(request, 'Reset token has been sent to your email.')
        return redirect('reset_password')

    return render(request, 'forgot_password.html')

def reset_password(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        new_password = request.POST.get('new_password')
        email = request.session.get('reset_email')

        if token == request.session.get('reset_token') and email:
            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()

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

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email is already registered.")
        else:
            User.objects.create_user(username=email, email=email, password=password)
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')
    return render(request, 'register.html')


@login_required
def user_home(request):
    query = request.GET.get('q', '').strip()
    books = Book.objects.all()

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(genres__name__icontains=query)
        ).distinct()

    favorite_books = Book.objects.filter(favorited_by__user=request.user)

    return render(request, 'user_home.html', {
        'books': books,
        'favorite_books': favorite_books,
        'is_staff': request.user.is_staff
    })



def guest_home(request):
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
    book = get_object_or_404(Book, book_id=book_id)
    user_favorite_books = []
    if request.user.is_authenticated:
        user_favorite_books = FavoriteBook.objects.filter(user=request.user).values_list('book_id', flat=True)

    reviews = Review.objects.filter(book=book).order_by('-created_at')

    if request.method == 'POST' and request.user.is_authenticated:
        rating = request.POST.get('rating')
        review_text = request.POST.get('review_text')


        if rating and review_text:
            try:
                Review.objects.create(
                    user=request.user,
                    book=book,
                    rating=int(rating),
                    review_text=review_text.strip()
                )

                return redirect('book_detail', book_id=book_id)
            except Exception as e:

                print(f"Error saving review: {e}")

    return render(request, 'book_detail.html', {
        'book': book,
        'user_favorite_books': user_favorite_books,
        'reviews': reviews,
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
    favorites = FavoriteBook.objects.filter(user=request.user).select_related('book')
    return render(request, 'user_favorites.html', {'favorites': favorites})

@login_required
def add_to_favorites(request, book_id):
    book = get_object_or_404(Book, book_id=book_id)

    try:
        favorite, created = FavoriteBook.objects.get_or_create(user=request.user, book=book)
        if created:
            print("Book added to favorites.")
        else:
            print("Book is already in favorites.")
    except IntegrityError as e:
        print(f"Error adding book to favorites: {e}")

    return redirect('book_detail', book_id=book_id)

@login_required
def remove_from_favorites(request, book_id):

    book = get_object_or_404(Book, book_id=book_id)

    try:

        FavoriteBook.objects.filter(user=request.user, book=book).delete()
        print("Book removed from favorites.")
    except Exception as e:
        print(f"Error removing book from favorites: {e}")

    return redirect('user_favorites')

@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

@user_passes_test(lambda u: u.is_staff)
def manage_users(request):
    users = User.objects.all()

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return redirect('manage_users')

    return render(request, 'manage_users.html', {'users': users})


@user_passes_test(lambda u: u.is_staff)
def admin_reports(request):

    today = now().date()
    new_users_today = User.objects.filter(date_joined__date=today).count()


    new_books_today = Book.objects.filter(created_at__date=today).count()


    total_users = User.objects.count()


    total_books = Book.objects.count()

    return render(request, 'admin_reports.html', {
        'new_users_today': new_users_today,
        'new_books_today': new_books_today,
        'total_users': total_users,
        'total_books': total_books,
    })


@user_passes_test(lambda u: u.is_staff)
def manage_books(request):
    books = Book.objects.all()

    # מחיקת ספר
    if request.method == 'POST' and 'delete_book_id' in request.POST:
        book_id = request.POST.get('delete_book_id')
        book = get_object_or_404(Book, book_id=book_id)
        book.delete()
        return redirect('manage_books')

    return render(request, 'manage_books.html', {'books': books})


@user_passes_test(lambda u: u.is_staff)
def edit_book(request, book_id):
    book = get_object_or_404(Book, book_id=book_id)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('manage_books')
    else:
        form = BookForm(instance=book)

    return render(request, 'edit_book.html', {'form': form, 'book': book})


@user_passes_test(lambda u: u.is_staff)
def delete_book(request, book_id):
    book = get_object_or_404(Book, book_id=book_id)
    book.delete()
    return redirect('manage_books')
















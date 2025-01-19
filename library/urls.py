from django.urls import path
from . import views
from library.views import  admin_reports
from library.views import manage_books, edit_book
urlpatterns = [
    path('', views.welcome, name='welcome'),  # דף Welcome
    path('login/', views.login_view, name='login'),    # דף Login
    path('forgot-password/', views.forgot_password, name='forgot_password'),  # דף שכחתי סיסמה
    path('reset-password/', views.reset_password, name='reset_password'),  # דף איפוס סיסמה
    path('register/', views.register, name='register'),  # דף הרשמה
    path('user-home/', views.user_home, name='user_home'),  # דף הבית למשתמשים
    path('guest-home/', views.guest_home, name='guest_home'), # דף הבית לאורחים
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('search/', views.search_books, name='search_books'), # דשבורד למנהלים
    path('add-book/', views.add_book, name='add_book'),
    path('favorites/', views.user_favorites, name='user_favorites'),
    path('add-to-favorites/<int:book_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove-from-favorites/<int:book_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/manage-users/', views.manage_users, name='manage_users'),
    path('admin-reports/', views.admin_reports, name='admin_reports'),
    path('admin-reports/', admin_reports, name='admin_reports'),
    path('manage-books/', manage_books, name='manage_books'),
    path('edit-book/<int:book_id>/', edit_book, name='edit_book'),
    path('delete-book/<int:book_id>/', views.delete_book, name='delete_book'),


]

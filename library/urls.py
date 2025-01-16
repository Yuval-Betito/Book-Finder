from django.urls import path
from . import views


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
    path('favorites/', views.user_favorites, name='user_favorites'),
    path('books/<int:book_id>/add_to_favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('books/<int:book_id>/remove_from_favorites/', views.remove_from_favorites, name='remove_from_favorites'),

]

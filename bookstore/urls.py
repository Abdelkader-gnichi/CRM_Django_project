from os import name
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [
    path('home/', views.home, name= 'home'),
    path('books/', views.books, name= 'books'),
    path('customer/<int:pk>/', views.customer, name='customer'),
    path('create_order/', views.create_order, name= 'create_order'),
    path('multi_create_order/<int:pk>', views.multi_create_order, name= 'multi_create_order'),
    path('update_order/<int:pk>', views.update_order, name= 'update_order'),
    path('delete_order/<int:pk>', views.delete_order, name= 'delete_order'),
    path('create_customer/', views.create_customer, name='create_customer'),
    path('update_customer/<int:pk>', views.update_customer, name='update_customer'),
    path('delete_customer/<int:pk>', views.delete_customer, name='delete_customer'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name= 'logout'),
    path('user/', views.user_profile, name= 'user_profile'),
    path('profile/', views.profile_info, name= 'profile_info'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name= 'bookstore/reset_password.html'), name= 'reset_password'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name= 'bookstore/password_reset_sent.html'), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='bookstore/password_reset_form.html'), name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='bookstore/password_reset_done.html'), name='password_reset_complete'),
    path('', views.home),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]

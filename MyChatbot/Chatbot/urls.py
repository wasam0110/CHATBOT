from django.shortcuts import redirect
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    path('verify_email/', views.verify_email, name='verify_email'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('chat/', views.chat_page, name='chat'),
    path('get_response/', views.get_response, name='get_response'),
    path('saved_chats/', views.saved_chats, name='saved_chats'),
    path('', lambda request: redirect('login')),
]

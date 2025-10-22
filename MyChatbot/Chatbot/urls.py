from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_page, name='chat_page'),
    path('send/', views.send_message, name='send_message'),
    path('register/', views.register, name='register'),
    path('verify/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

]

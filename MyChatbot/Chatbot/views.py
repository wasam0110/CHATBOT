from django.shortcuts import render
from django.http import JsonResponse
from .models import ChatHistory
from django.contrib.auth.decorators import login_required
import requests, os
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from .models import Profile

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False
        user.save()
        Profile.objects.create(user=user)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        domain = get_current_site(request).domain
        link = f"http://{domain}/verify/{uid}/{token}/"
        email_subject = "Verify your email"
        message = render_to_string("verify_email.html", {"link": link, "user": user})
        EmailMessage(email_subject, message, to=[email]).send()

        messages.success(request, "Verification email sent!")
        return redirect('login')

    return render(request, "register.html")

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        Profile.objects.filter(user=user).update(is_verified=True)
        messages.success(request, "Email verified! You can now log in.")
        return redirect('login')
    else:
        messages.error(request, "Invalid verification link.")
        return redirect('register')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('chat_page')
            else:
                messages.error(request, "Verify your email first.")
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, "login.html")

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required
def chat_page(request):
    return render(request, "chat.html")

@login_required
def send_message(request):
    if request.method == "POST":
        user_msg = request.POST.get("message")
        headers = {"Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}"}
        data = {"messages": [{"role": "user", "content": user_msg}]}

        res = requests.post("https://api.groq.com/openai/v1/chat/completions", json=data, headers=headers)
        bot_reply = res.json()["choices"][0]["message"]["content"]

        ChatHistory.objects.create(user=request.user, user_message=user_msg, bot_reply=bot_reply)
        return JsonResponse({"reply": bot_reply})

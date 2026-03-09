from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from .models import Profile, ChatHistory
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import os
import json
import random
import requests
# ---------------------- REGISTER ----------------------
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password1)
        code = str(random.randint(100000, 999999))
        user.profile.verification_code = code
        user.profile.save()

        send_mail(
            'Your Verification Code',
            f'Your verification code is {code}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        request.session['email'] = email
        messages.info(request, "Verification code sent to your email.")
        return redirect('verify_email')

    return render(request, 'register.html')

# ---------------------- VERIFY EMAIL ----------------------
def verify_email(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        email = request.session.get('email')
        profile = Profile.objects.get(user__email=email)

        if profile.verification_code == code:
            profile.is_verified = True
            profile.save()
            messages.success(request, "Email verified successfully! You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Invalid verification code")

    return render(request, 'verify.html')

# ---------------------- LOGIN ----------------------
def login_user(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username_or_email, password=password)
        if user is None:
            try:
                user_obj = User.objects.get(email=username_or_email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            if user.profile.is_verified:
                login(request, user)
                if not request.POST.get('remember_me'):
                    request.session.set_expiry(0)
                return redirect('chat')
            else:
                messages.error(request, "Please verify your email before logging in.")
                return redirect('verify_email')
        else:
            messages.error(request, "Invalid username/email or password")
            return redirect('login')

    return render(request, 'login.html')

# ---------------------- LOGOUT ----------------------
def logout_user(request):
    logout(request)
    return redirect('login')

# ---------------------- FORGOT PASSWORD ----------------------
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            code = str(random.randint(100000, 999999))
            request.session['reset_email'] = email
            request.session['reset_code'] = code

            send_mail(
                'Password Reset Code',
                f'Your verification code is {code}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            messages.info(request, 'Verification code sent to your email.')
            return redirect('reset_password')
        except User.DoesNotExist:
            messages.error(request, 'Email not found.')
    return render(request, 'forgot_password.html')

# ---------------------- RESET PASSWORD ----------------------
def reset_password(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        new_pass = request.POST.get('new_password')
        email = request.session.get('reset_email')
        stored_code = request.session.get('reset_code')

        if code == stored_code and email:
            user = User.objects.get(email=email)
            user.set_password(new_pass)
            user.save()
            messages.success(request, 'Password reset successful. You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid code or session expired.')
    return render(request, 'reset_password.html')

# ---------------------- CHAT PAGE ----------------------
@login_required
def chat_page(request):
    return render(request, 'chat.html')


@login_required
def get_response(request):
    if request.method == "POST":
        user_message = request.POST.get("message", "")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.GROQ_API_KEY}"
        }

        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "Explain everything simply and clearly like a teacher."},
                {"role": "user", "content": user_message}
            ]
        }

        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                data=json.dumps(data)
            )
            response_data = response.json()

            bot_response = response_data["choices"][0]["message"]["content"]

            # ✅ Save chat to database
            ChatHistory.objects.create(
                user=request.user,
                user_message=user_message,
                bot_response=bot_response
            )

            return JsonResponse({"response": bot_response})

        except Exception as e:
            return JsonResponse({"error": str(e)})

    return JsonResponse({"error": "Invalid request"})

@login_required
def saved_chats(request):
    chats = ChatHistory.objects.filter(user=request.user).order_by('-timestamp')
    chat_list = []
    for chat in chats:
        chat_list.append({
            "id": chat.id,
            "user_message": chat.user_message,
            "bot_response": chat.bot_response,
            "timestamp": chat.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        })
    return JsonResponse({"chats": chat_list})

@login_required
def get_saved_chats(request):
    try:
        chats = ChatHistory.objects.filter(user=request.user).order_by('-timestamp')
        chat_data = [
            {
                "id": chat.id,
                "user_message": chat.user_message,
                "bot_reply": chat.bot_reply,
                "timestamp": chat.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for chat in chats
        ]
        return JsonResponse({"chats": chat_data})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
# ---------------------- SEND MESSAGE ----------------------
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

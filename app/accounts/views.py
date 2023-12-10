from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth

def registerPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if len(password) >= 6 and len(username) >=6:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                auth.login(request, user)
                messages.info(request, 'User created')
                return redirect('index')
        else:
            messages.info(request, 'Password or Username too short')
            return redirect('register')
    return render(request, 'accounts/register.html')

def loginPage(request):
    if request.method == 'POST':
        email_username = request.POST.get('email_username')
        password = request.POST.get('password')
        
        user_auth = auth.authenticate(username=email_username, password=password)
        email_auth = auth.authenticate(email=email_username, password=password)
        
        if user_auth is not None:
            auth.login(request, user_auth)
            messages.info(request, 'Login successful')
            return redirect('index')
        elif email_auth is not None:
            auth.login(request, email_auth)
            messages.info(request, 'Login successful')
            return redirect('index')
        else:
            messages.info(request, 'Invalid credentials!')
            return redirect('login')
    return render(request, 'accounts/login.html')

def logoutPage(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.info(request, 'Logout successful')
        return redirect('index')

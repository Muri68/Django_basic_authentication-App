from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from validate_email import validate_email
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    
    def post(self, request):
        data = request.POST
        context={
            'data': data,
            'has_error': False,
            }
        
        full_name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if len(password) < 8:
            messages.add_message(request, messages.ERROR, 'Password should be 8 or more character ')
            context['has_error'] = True
            
        if password!=password2:
            messages.add_message(request, messages.ERROR, "Passwords didn't match")
            context['has_error'] = True
            
        if not validate_email(email):
            messages.add_message(request, messages.ERROR, 'Please provide a valid email')
            context['has_error'] = True
            
        try:
            if User.objects.get(email=email):
                messages.add_message(request, messages.ERROR, 'Email is taken')
                context['has_error'] = True

        except Exception as identifier:
            pass

        try:
            if User.objects.get(username=username):
                messages.add_message(
                    request, messages.ERROR, 'Username is taken')
                context['has_error'] = True

        except Exception as identifier:
            pass
            
        if context['has_error']:
            return render(request, 'authentication/register.html', context, status=400)
        
        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.first_name = full_name
        user.last_name = full_name
        user.save()
        
        messages.add_message(request, messages.SUCCESS, 'Account created successfuly')
        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        data = request.POST
        context={
            'data': data,
            'has_error': False,
            }
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username == '':
            messages.add_message(request, messages.ERROR, 'Username is required')
            context['has_error'] = True
        
        if password == '':
            messages.add_message(request, messages.ERROR, 'Password is required')
            context['has_error'] = True
        
        user = authenticate(request, username=username, password=password)
        
        if not user and not context['has_error']:
            messages.add_message(request, messages.ERROR, 'Invalid login credencials')
            context['has_error'] = True
        
        if context['has_error']:
            return render(request, 'authentication/login.html', context, status=400)
        
        login(request, user)
        return redirect('home')


class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')


class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'You have been Logged out')
        return redirect('login')
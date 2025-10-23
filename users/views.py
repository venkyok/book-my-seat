from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import UserRegisterForm, UserUpdateForm
from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from movies.models import Movie , Booking
from django.contrib import messages
from django.conf import settings
import os

# Check if running in demo mode (Vercel)
IS_DEMO_MODE = os.environ.get('VERCEL', False) or not os.access(settings.BASE_DIR, os.W_OK)

# Import demo data
if IS_DEMO_MODE:
    from movies import demo_data

def home(request):
    if IS_DEMO_MODE:
        movies = demo_data.get_demo_movies()
    else:
        movies = Movie.objects.all()
    return render(request,'home.html',{'movies':movies, 'is_demo': IS_DEMO_MODE})

def register(request):
    if IS_DEMO_MODE:
        # Demo mode - show message
        messages.warning(request, '🎭 Demo Mode: Registration is disabled on Vercel (read-only database). This is a visual demonstration. To use the full app with user accounts and bookings, run it locally or deploy to Render.com!')
        return redirect('movie-list')
    
    # Normal mode
    if request.method == 'POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password1')
            user=authenticate(username=username,password=password)
            login(request,user)
            return redirect('profile')
    else:
        form=UserRegisterForm()
    return render(request,'users/register.html',{'form':form})

def login_view(request):
    if IS_DEMO_MODE:
        # Demo mode - show message
        messages.warning(request, '🎭 Demo Mode: Login is disabled (no database writes). Browse movies and theaters to see the interface. For full functionality, run locally!')
        return redirect('movie-list')
    
    # Normal mode
    if request.method == 'POST':
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect('/')
    else:
        form=AuthenticationForm()
    return render(request,'users/login.html',{'form':form})

@login_required
def profile(request):
    if IS_DEMO_MODE:
        messages.info(request, '🎭 Demo Mode: Profile features are disabled.')
        return redirect('movie-list')
    
    bookings= Booking.objects.filter(user=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)

    return render(request, 'users/profile.html', {'u_form': u_form,'bookings':bookings})

@login_required
def reset_password(request):
    if request.method == 'POST':
        form=PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form=PasswordChangeForm(user=request.user)
    return render(request,'users/reset_password.html',{'form':form})
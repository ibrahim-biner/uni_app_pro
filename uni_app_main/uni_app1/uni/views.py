from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser
from django.contrib.auth import logout




@login_required
def home(request):
    user_role = request.user.role  # Kullanıcının rolünü al
    
    # Kullanıcı rolüne göre içerik belirleme
    context = {
        "user_role": user_role
    }
    
    return render(request, "home.html", context)

@login_required
def user_register(request):
    # Kullanıcı sadece Bölüm Başkanı veya Bölüm Sekreteri ise kullanıcı ekleyebilir
    if request.user.role not in ['bolum_baskani', 'bolum_sekreteri']:
        return HttpResponseForbidden("Bu işlemi yalnızca Bölüm Başkanı veya Bölüm Sekreteri yapabilir.")

    # Bölüm Başkanı dışındaki kullanıcılar sadece formu görebilir ancak rol seçemezler
    if request.user.role == 'bolum_baskani' and request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Anasayfaya yönlendir
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

def user_logout(request):
    logout(request)
    return redirect('login')


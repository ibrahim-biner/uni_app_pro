from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from .models import DersProgrami
from .forms import DersProgramiForm
from .models import Ders, Derslik
from .forms import DersForm, DerslikForm
from .forms import DersDuzenleForm




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



@login_required
def ders_programi_list(request):
    programlar = DersProgrami.objects.all()
    return render(request, 'ders_programi_list.html', {'programlar': programlar})

@login_required
def ders_programi_ekle(request):
    if request.method == "POST":
        form = DersProgramiForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ders_programi_list')  # Listeye yönlendir
    else:
        form = DersProgramiForm()

    return render(request, 'ders_programi_ekle.html', {'form': form})

@login_required
def ders_programi_sil(request, pk):
    program = get_object_or_404(DersProgrami, pk=pk)
    program.delete()
    return redirect('ders_programi_list')


@login_required
def ders_ekle(request):
    if request.method == "POST":
        form = DersForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ders_listesi')  # Ders listesini gösterecek sayfaya yönlendir
    else:
        form = DersForm()

    return render(request, 'ders_ekle.html', {'form': form})

def ders_listesi(request):
    dersler = Ders.objects.all()  # Tüm dersleri al
    return render(request, 'ders_listesi.html', {'dersler': dersler})

@login_required
def derslik_ekle(request):
    if request.method == "POST":
        form = DerslikForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('derslik_listesi')  # Derslik listesini gösterecek sayfaya yönlendir
    else:
        form = DerslikForm()

    return render(request, 'derslik_ekle.html', {'form': form})

def derslik_listesi(request):
    derslikler = Derslik.objects.all()
    return render(request, 'derslik_listesi.html', {'derslikler': derslikler})


def ders_duzenle(request, ders_id):
    ders = get_object_or_404(Ders, pk=ders_id)

    if request.method == 'POST':
        form = DersDuzenleForm(request.POST, instance=ders)
        if form.is_valid():
            form.save()  # Ders bilgisini kaydet
            return redirect('ders_listesi')  # Ders listesine yönlendir
    else:
        form = DersDuzenleForm(instance=ders)

    return render(request, 'duzenle_ders.html', {'form': form, 'ders': ders})


def ders_sil(request, ders_id):
    ders = get_object_or_404(Ders, pk=ders_id)
    ders.delete()
    return redirect('ders_listesi')

def derslik_sil(request, derslik_id):
    derslik = get_object_or_404(Derslik, pk=derslik_id)
    derslik.delete()  # Dersliği sil
    return redirect('derslik_listesi')  # Derslik listesine yönlendir


def derslik_detay(request, derslik_id):
    derslik = get_object_or_404(Derslik, pk=derslik_id)
    dersler = DersProgrami.objects.filter(derslik=derslik)
    return render(request, "derslik_detay.html", {"derslik": derslik, "dersler": dersler})
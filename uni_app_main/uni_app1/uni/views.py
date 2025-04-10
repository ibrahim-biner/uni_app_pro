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
from .models import SinavProgrami
from .forms import SinavProgramiForm
from django.http import JsonResponse
from .models import SinavProgrami, CustomUser, OturmaPlani
from reportlab.pdfgen import canvas
from django.http import HttpResponse






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

@login_required
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

@login_required
def derslik_listesi(request):
    derslikler = Derslik.objects.all()
    return render(request, 'derslik_listesi.html', {'derslikler': derslikler})

@login_required
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

@login_required
def ders_sil(request, ders_id):
    ders = get_object_or_404(Ders, pk=ders_id)
    ders.delete()
    return redirect('ders_listesi')

@login_required
def derslik_sil(request, derslik_id):
    derslik = get_object_or_404(Derslik, pk=derslik_id)
    derslik.delete()  # Dersliği sil
    return redirect('derslik_listesi')  # Derslik listesine yönlendir

@login_required
def derslik_detay(request, derslik_id):
    derslik = get_object_or_404(Derslik, pk=derslik_id)
    dersler = DersProgrami.objects.filter(derslik=derslik)
    return render(request, "derslik_detay.html", {"derslik": derslik, "dersler": dersler})


@login_required
def sinav_ekle(request):
    if request.method == 'POST':
        form = SinavProgramiForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sinav_listesi')  # Sınav listesine yönlendirme
    else:
        form = SinavProgramiForm()
    
    return render(request, 'sinav_ekle.html', {'form': form})

@login_required
def sinav_listesi(request):
    sinavlar = SinavProgrami.objects.all()
    return render(request, 'sinav_listesi.html', {'sinavlar': sinavlar})



import math, random
@login_required
def oturma_plani_goruntule(request, sinav_id):
    # Seçilen sınavı alıyoruz
    sinav = get_object_or_404(SinavProgrami, id=sinav_id)
    ders = sinav.ders
    derslik = sinav.derslik

    # Dersin aldığı öğrenci sayısı (ders tablosundaki ogrenci_sayisi)
    ogrenci_sayisi = ders.ogrenci_sayisi

    # Sistemde kayıtlı, 'ogrenci' rolündeki kullanıcılar arasından,
    # dersin aldığı öğrenci sayısı kadarını alıyoruz (ilk ogrenci_sayisi kadar)
    ogrenciler = list(CustomUser.objects.filter(role='ogrenci')[:ogrenci_sayisi])
    random.shuffle(ogrenciler)

    # Oturma düzeni: her sırada 3 koltuk olacak.
    # Ancak kullanılabilecek maksimum sıra sayısı, derslik kapasitesinin 3'e bölümü kadar olsun.
    max_rows = derslik.kapasite // 3
    # Gerçek öğrenci sayısına göre kaç sıra gerektiğini hesapla (yani ceil(ogrenci/3))
    required_rows = math.ceil(len(ogrenciler) / 3) if ogrenciler else 0
    row_count = min(required_rows, max_rows)

    # Oturma düzenini 2 boyutlu liste şeklinde oluşturalım
    oturma_duzeni = []
    index = 0
    for _ in range(row_count):
        row = []
        for _ in range(3):
            if index < len(ogrenciler):
                row.append(ogrenciler[index])
                index += 1
            else:
                row.append(None)  # Boş koltuk
        oturma_duzeni.append(row)

    context = {
        'sinav': sinav,
        'derslik': derslik,
        'oturma_duzeni': oturma_duzeni,
    }
    return render(request, 'oturma_plani.html', context)

from reportlab.lib.pagesizes import letter

@login_required
def oturma_plani_pdf(request, sinav_id):
    # Aynı oturma planını PDF olarak oluşturacağız
    sinav = get_object_or_404(SinavProgrami, id=sinav_id)
    ders = sinav.ders
    derslik = sinav.derslik
    ogrenci_sayisi = ders.ogrenci_sayisi
    ogrenciler = list(CustomUser.objects.filter(role='ogrenci')[:ogrenci_sayisi])
    random.shuffle(ogrenciler)

    max_rows = derslik.kapasite // 3
    required_rows = math.ceil(len(ogrenciler) / 3) if ogrenciler else 0
    row_count = min(required_rows, max_rows)
    oturma_duzeni = []
    index = 0
    for _ in range(row_count):
        row = []
        for _ in range(3):
            if index < len(ogrenciler):
                row.append(ogrenciler[index].username)  # PDF'de username gösterelim
                index += 1
            else:
                row.append("Bos")
        oturma_duzeni.append(row)

    # PDF oluşturma
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="oturma_plani_{sinav.id}.pdf"'
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 50, f"Ders: {ders.ad}")
    p.drawString(50, height - 70, f"Tarih: {sinav.tarih}  Saat: {sinav.saat}")
    p.drawString(50, height - 90, f"Derslik: {derslik.ad}")
    if sinav.gozetmen:
        p.drawString(50, height - 110, f"Gözetmen: {sinav.gozetmen.username}")
    else:
        p.drawString(50, height - 110, "Gözetmen: Yok")
    y = height - 140
    for row in oturma_duzeni:
        row_text = " | ".join(row)
        p.drawString(50, y, row_text)
        y -= 20
    p.showPage()
    p.save()
    return response


def user_logout(request):
    logout(request)
    return redirect('login') 
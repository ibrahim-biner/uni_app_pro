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
from .forms import DersDuzenleForm,SinavYorumForm
from .models import SinavProgrami
from .forms import SinavProgramiForm
from django.http import JsonResponse
from .models import SinavProgrami, CustomUser, OturmaPlani,SinavYorum
from reportlab.pdfgen import canvas
from django.http import HttpResponse






@login_required
def home(request):
    user_role = request.user.role 
    
    
    context = {
        "user_role": user_role
    }
    
    return render(request, "home.html", context)

@login_required
def user_register(request):
    if request.user.role not in ['bolum_baskani', 'bolum_sekreteri']:
        return HttpResponseForbidden("Bu işlemi yalnızca Bölüm Başkanı veya Bölüm Sekreteri yapabilir.")

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request_user=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            if request.user.role == 'bolum_sekreteri':
                user.role ='ogrenci'  
            user.save()
            return redirect('home')
    else:
        form = CustomUserCreationForm(request_user=request.user)

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
def ders_programi_list1(request):
    
    programlar = DersProgrami.objects.all().order_by('gun', 'baslangic_saati')
    return render(request, 'ders_programi_list.html', {'programlar': programlar})


def ders_programi_list(request):
    
    gun_sirasi = {
        'Pazartesi': 0,
        'Salı': 1,
        'Çarşamba': 2,
        'Perşembe': 3,
        'Cuma': 4,
    }

    
    programlar = DersProgrami.objects.all()

    
    programlar = sorted(programlar, key=lambda x: (gun_sirasi.get(x.gun, 5), x.baslangic_saati))

    return render(request, 'ders_programi_list.html', {'programlar': programlar})

@login_required
def ders_programi_ekle1(request):
    if request.method == "POST":
        form = DersProgramiForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ders_programi_list')  
    else:
        form = DersProgramiForm()

    return render(request, 'ders_programi_ekle.html', {'form': form})

from django.db.models import Q
@login_required
def ders_programi_ekle2(request):
    if request.method == "POST":
        form = DersProgramiForm(request.POST)
        
        if form.is_valid():
            
            derslik = form.cleaned_data['derslik']
            gun = form.cleaned_data['gun']
            baslangic_saati = form.cleaned_data['baslangic_saati']
            bitis_saati = form.cleaned_data['bitis_saati']

            
    
            ders_var_mi = DersProgrami.objects.filter(
                Q(gun=gun) &
                Q(derslik=derslik) &
                (
                    Q(baslangic_saati__lt=bitis_saati) & Q(bitis_saati__gt=baslangic_saati)  
                )
            ).exists()

            if ders_var_mi:
                form.add_error(None, "Bu derslikte belirtilen saat diliminde başka bir ders bulunmaktadır. Lütfen farklı bir zaman dilimi seçin.")
            else:
                form.save()
                return redirect('ders_programi_list')  

    else:
        form = DersProgramiForm()

    return render(request, 'ders_programi_ekle.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import DersProgramiForm
from .models import DersProgrami
from django.db.models import Q

@login_required
def ders_programi_ekle3(request):
    if request.method == "POST":
        form = DersProgramiForm(request.POST)
        
        if form.is_valid():
            
            derslik = form.cleaned_data['derslik']
            gun = form.cleaned_data['gun']
            baslangic_saati = form.cleaned_data['baslangic_saati']
            bitis_saati = form.cleaned_data['bitis_saati']

            # Çakışma kontrolü
            
            ders_var_mi = DersProgrami.objects.filter(
                Q(gun=gun) &
                Q(derslik=derslik) &
                (
                    Q(baslangic_saati__lt=bitis_saati) & Q(bitis_saati__gt=baslangic_saati)  # Saatler çakışıyorsa
                )
            ).exists()

            if ders_var_mi:
                form.add_error(None, "Seçilen derslikte belirtilen gün ve saatlerde ders vardır. Lütfen farklı bir zaman dilimi seçin.")
            else:
                form.save()
                return redirect('ders_programi_list')  

        
        else:
            form.add_error(None, "Eksik ya da hatalı bilgi var. Lütfen formu kontrol edin.")

    else:
        form = DersProgramiForm()

    return render(request, 'ders_programi_ekle.html', {'form': form})

@login_required
def ders_programi_ekleBu(request):
    if request.method == "POST":
        form = DersProgramiForm(request.POST)

        if form.is_valid():
            derslik = form.cleaned_data['derslik']
            ders = form.cleaned_data['ders']
            gun = form.cleaned_data['gun']
            baslangic_saati = form.cleaned_data['baslangic_saati']
            bitis_saati = form.cleaned_data['bitis_saati']

            cakisma_var_mi = DersProgrami.objects.filter(
                Q(gun=gun) &
                Q(derslik=derslik) &
                Q(baslangic_saati__lt=bitis_saati) &
                Q(bitis_saati__gt=baslangic_saati)
            ).exists()

            if cakisma_var_mi:
                form.add_error(None, "Seçilen derslikte belirtilen gün ve saatlerde başka bir ders vardır.")

            elif ders.ogrenci_sayisi > derslik.kapasite:
                form.add_error(
                    None,
                    f"Bu dersi alan öğrenci sayısı ({ders.ogrenci_sayisi}), seçilen dersliğin kapasitesini ({derslik.kapasite}) aşıyor."
                )

            else:
                form.save()
                return redirect('ders_programi_list')

    else:
        form = DersProgramiForm()

    return render(request, 'ders_programi_ekle.html', {
        'form': form,
        'hatalar': form.errors if form.errors else None,
    })

@login_required
def ders_programi_ekle(request):
    if request.method == "POST":
        form = DersProgramiForm(request.POST)

        if form.is_valid():
            derslik = form.cleaned_data['derslik']
            ders = form.cleaned_data['ders']
            ogretim_elemani = form.cleaned_data['ogretim_elemani']
            gun = form.cleaned_data['gun']
            baslangic_saati = form.cleaned_data['baslangic_saati']
            bitis_saati = form.cleaned_data['bitis_saati']

            
            derslik_cakisiyor = DersProgrami.objects.filter(
                gun=gun,
                derslik=derslik,
                baslangic_saati__lt=bitis_saati,
                bitis_saati__gt=baslangic_saati
            ).exists()

            
            akademisyen_cakisiyor = DersProgrami.objects.filter(
                gun=gun,
                ogretim_elemani=ogretim_elemani,
                baslangic_saati__lt=bitis_saati,
                bitis_saati__gt=baslangic_saati
            ).exists()

            
            kapasite_asimi = ders.ogrenci_sayisi > derslik.kapasite

            if derslik_cakisiyor:
                form.add_error(None, "Seçilen derslikte belirtilen gün ve saatlerde başka bir ders bulunmaktadır.")
            elif akademisyen_cakisiyor:
                form.add_error(None, "Bu akademisyenin belirtilen gün ve saatlerde başka bir dersi bulunmaktadır.")
            elif kapasite_asimi:
                form.add_error(None, f"Bu dersi alan öğrenci sayısı ({ders.ogrenci_sayisi}), "
                                     f"seçilen dersliğin kapasitesini ({derslik.kapasite}) aşıyor.")
            else:
                form.save()
                return redirect('ders_programi_list')

    else:
        form = DersProgramiForm()

    return render(request, 'ders_programi_ekle.html', {
        'form': form,
    })


def bolum_yetkili_mi(user):
    return user.role in ['bölüm başkanı', 'bölüm sekreteri']

from django.contrib.auth.decorators import user_passes_test

@login_required
def ders_programi_duzenle1(request, pk):
    program = get_object_or_404(DersProgrami, pk=pk)
    if request.method == 'POST':
        form = DersProgramiForm(request.POST, instance=program)
        if form.is_valid():
            form.save()
            return redirect('ders_programi_list')
    else:
        form = DersProgramiForm(instance=program)

    return render(request, 'ders_programi_duzenle.html', {'form': form})


@login_required
def ders_programi_duzenle(request, pk):
    program = get_object_or_404(DersProgrami, pk=pk)

    if request.method == 'POST':
        form = DersProgramiForm(request.POST, instance=program)
        if form.is_valid():
            derslik = form.cleaned_data['derslik']
            ders = form.cleaned_data['ders']
            ogretim_elemani = form.cleaned_data['ogretim_elemani']
            gun = form.cleaned_data['gun']
            baslangic_saati = form.cleaned_data['baslangic_saati']
            bitis_saati = form.cleaned_data['bitis_saati']

            # 1. Derslik çakışması kontrol
            derslik_cakisiyor = DersProgrami.objects.filter(
                gun=gun,
                derslik=derslik,
                baslangic_saati__lt=bitis_saati,
                bitis_saati__gt=baslangic_saati
            ).exclude(pk=program.pk).exists()

            # 2. Akademisyen çakışması kontrol
            akademisyen_cakisiyor = DersProgrami.objects.filter(
                gun=gun,
                ogretim_elemani=ogretim_elemani,
                baslangic_saati__lt=bitis_saati,
                bitis_saati__gt=baslangic_saati
            ).exclude(pk=program.pk).exists()

            # 3. Kapasite kontrol
            kapasite_asimi = ders.ogrenci_sayisi > derslik.kapasite

            if derslik_cakisiyor:
                form.add_error(None, "Seçilen derslikte belirtilen gün ve saatlerde başka bir ders bulunmaktadır.")
            elif akademisyen_cakisiyor:
                form.add_error(None, "Bu akademisyenin belirtilen gün ve saatlerde başka bir dersi bulunmaktadır.")
            elif kapasite_asimi:
                form.add_error(None, f"Bu dersi alan öğrenci sayısı ({ders.ogrenci_sayisi}), "
                                     f"seçilen dersliğin kapasitesini ({derslik.kapasite}) aşıyor.")
            else:
                form.save()
                return redirect('ders_programi_list')

    else:
        form = DersProgramiForm(instance=program)

    return render(request, 'ders_programi_duzenle.html', {'form': form})

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
            return redirect('ders_listesi')  
    else:
        form = DersForm()

    return render(request, 'ders_ekle.html', {'form': form})

@login_required
def ders_listesi(request):
    dersler = Ders.objects.all()  
    return render(request, 'ders_listesi.html', {'dersler': dersler})

@login_required
def derslik_ekle(request):
    if request.method == "POST":
        form = DerslikForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('derslik_listesi')  
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
            form.save()  
            return redirect('ders_listesi')  
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
    derslik.delete()  
    return redirect('derslik_listesi')  

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
            return redirect('sinav_listesi')  
    else:
        form = SinavProgramiForm()
    
    return render(request, 'sinav_ekle.html', {'form': form})

@login_required
def sinav_listesi(request):
    sinavlar = SinavProgrami.objects.all()
    return render(request, 'sinav_listesi.html', {'sinavlar': sinavlar})

@login_required
def oturma_plani_olustur(request, sinav_id):
    sinav = get_object_or_404(SinavProgrami, id=sinav_id)
    ders = sinav.ders
    derslik = sinav.derslik
    ogrenci_sayisi = ders.ogrenci_sayisi
    ogrenciler = list(CustomUser.objects.filter(role='ogrenci')[:ogrenci_sayisi])
    random.shuffle(ogrenciler)

    # Daha önce oluşturulmuşsa sil
    OturmaPlani.objects.filter(sinav=sinav).delete()

    for idx, ogrenci in enumerate(ogrenciler):
        OturmaPlani.objects.create(sinav=sinav, ogrenci=ogrenci, sira_no=idx + 1)

    return redirect('oturma_plani', sinav_id=sinav.id)

@login_required
def oturma_plani_goruntule(request, sinav_id):
    sinav = get_object_or_404(SinavProgrami, id=sinav_id)
    kapasite = sinav.derslik.kapasite

    sutun_sayisi = 3  # Sabit
    toplam_koltuk = kapasite
    satir_sayisi = (kapasite + sutun_sayisi - 1) // sutun_sayisi  # Yuvarlama

    # Boş tablo (None ile)
    oturma_listesi = [None] * toplam_koltuk

    # Öğrencileri al ve karıştır
    planlar = OturmaPlani.objects.filter(sinav=sinav)
    ogrenciler = [p.ogrenci for p in planlar]
    random.shuffle(ogrenciler)

    # Öğrencileri rastgele boş koltuklara yerleştir
    for ogrenci in ogrenciler:
        while True:
            pos = random.randint(0, toplam_koltuk - 1)
            if oturma_listesi[pos] is None:
                oturma_listesi[pos] = ogrenci
                break

    # 2D oturma düzenine çevir
    oturma_duzeni = []
    for i in range(0, toplam_koltuk, sutun_sayisi):
        oturma_duzeni.append(oturma_listesi[i:i + sutun_sayisi])

    return render(request, 'oturma_plani.html', {
        'sinav': sinav,
        'oturma_duzeni': oturma_duzeni,
    })


@login_required
def oturma_plani_olusturBU(request, sinav_id):
    sinav = get_object_or_404(SinavProgrami, id=sinav_id)
    ders = sinav.ders
    derslik = sinav.derslik
    ogrenci_sayisi = ders.ogrenci_sayisi
    ogrenciler = list(CustomUser.objects.filter(role='ogrenci')[:ogrenci_sayisi])
    random.shuffle(ogrenciler)

    # Daha önce oluşturulmuşsa sil (Yeniden oluştur butonu için)
    OturmaPlani.objects.filter(sinav=sinav).delete()

    for idx, ogrenci in enumerate(ogrenciler):
        OturmaPlani.objects.create(sinav=sinav, ogrenci=ogrenci, sira_no=idx+1)

    return redirect('oturma_plani', sinav_id=sinav.id)

import random
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import SinavProgrami, OturmaPlani, CustomUser


@login_required
def oturma_plani_goruntuleDenme(request, sinav_id):
    sinav = get_object_or_404(SinavProgrami, id=sinav_id)
    kapasite = sinav.derslik.kapasite  # Örn: 36

    # 3 sütun sabit
    sutun_sayisi = 3
    toplam_sira = kapasite // sutun_sayisi  # Örn: 36 // 3 = 12 sıra
    satir_sayisi = toplam_sira // sutun_sayisi  # 12 / 3 = 4 satır

    planlar = list(OturmaPlani.objects.filter(sinav=sinav))
    ogrenciler = [plan.ogrenci for plan in planlar]
    random.shuffle(ogrenciler)

    # Tüm sıraları temsil eden boş liste (None ile doldur)
    oturma_listesi = [None] * toplam_sira

    # Öğrencileri sıralara yerleştir
    for ogrenci in ogrenciler:
        while True:
            pozisyon = random.randint(0, toplam_sira - 1)
            if oturma_listesi[pozisyon] is None:
                oturma_listesi[pozisyon] = ogrenci
                break

    # Şimdi bu 1D listeyi 2D tabloya çevir (satır × sütun)
    oturma_duzeni = []
    for i in range(0, toplam_sira, sutun_sayisi):
        oturma_duzeni.append(oturma_listesi[i:i + sutun_sayisi])

    return render(request, 'oturma_plani.html', {
        'sinav': sinav,
        'oturma_duzeni': oturma_duzeni
    })


@login_required
def oturma_plani_goruntuleBU(request, sinav_id):
    sinav = get_object_or_404(SinavProgrami, id=sinav_id)
    planlar = OturmaPlani.objects.filter(sinav=sinav).order_by('sira_no')
    oturma_duzeni = []
    row = []

    for i, plan in enumerate(planlar):
        row.append(plan.ogrenci)
        if (i + 1) % 3 == 0:
            oturma_duzeni.append(row)
            row = []
    if row:
        oturma_duzeni.append(row)

    return render(request, 'oturma_plani.html', {
        'sinav': sinav,
        'oturma_duzeni': oturma_duzeni
    })


import math, random
@login_required
def oturma_plani_goruntule1(request, sinav_id):
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

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.lib import colors

@login_required
def oturma_plani_pdfBU(request, sinav_id):
    sinav = get_object_or_404(SinavProgrami, id=sinav_id)
    planlar = OturmaPlani.objects.filter(sinav=sinav).order_by('sira_no')

    # PDF hazırlığı
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="oturma_plani_{sinav.id}.pdf"'
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    margin = 50
    box_width = 60
    box_height = 30
    boxes_per_row = 3
    start_y = height - 180

    # Üst bilgi
    p.setFont("Helvetica-Bold", 14)
    p.drawString(margin, height - 50, f"Ders: {sinav.ders.ad}")
    p.setFont("Helvetica", 12)
    p.drawString(margin, height - 70, f"Tarih: {sinav.tarih}")
    p.drawString(margin, height - 90, f"Saat: {sinav.saat}")
    p.drawString(margin, height - 110, f"Derslik: {sinav.derslik.ad}")
    p.drawString(margin, height - 130, f"Gözetmen: {sinav.gozetmen.username if sinav.gozetmen else 'Yok'}")

    # Oturma düzenini 3'lü sıralar halinde çiz
    x = margin
    y = start_y
    p.setFont("Helvetica", 10)

    for i, plan in enumerate(planlar):
        ogrenci_adi = plan.ogrenci.get_full_name() or plan.ogrenci.username

        # Kutu çiz
        p.rect(x, y, box_width, box_height, fill=0)
        p.drawString(x + 5, y + box_height / 2 - 4, ogrenci_adi)

        # Konum güncelle
        if (i + 1) % boxes_per_row == 0:
            x = margin
            y -= box_height + 10
            if y < 50:
                p.showPage()
                y = height - margin
        else:
            x += box_width + 20

    p.showPage()
    p.save()
    return response

from io import BytesIO
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import random
from .models import OturmaPlani, SinavProgrami

@login_required
def oturma_plani_pdf(request, sinav_id):
    sinav = get_object_or_404(SinavProgrami, id=sinav_id)
    kapasite = sinav.derslik.kapasite
    sutun_sayisi = 3
    toplam_koltuk = kapasite
    satir_sayisi = (kapasite + sutun_sayisi - 1) // sutun_sayisi

    oturma_listesi = [None] * toplam_koltuk
    planlar = OturmaPlani.objects.filter(sinav=sinav)
    ogrenciler = [p.ogrenci for p in planlar]
    random.shuffle(ogrenciler)

    for ogrenci in ogrenciler:
        while True:
            pos = random.randint(0, toplam_koltuk - 1)
            if oturma_listesi[pos] is None:
                oturma_listesi[pos] = ogrenci
                break

    oturma_duzeni = []
    for i in range(0, toplam_koltuk, sutun_sayisi):
        oturma_duzeni.append(oturma_listesi[i:i + sutun_sayisi])

    template = get_template("oturma_plani_pdf.html")
    html = template.render({
        'sinav': sinav,
        'oturma_duzeni': oturma_duzeni
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{sinav.ders.ad}_oturma_plani.pdf"'
    pisa_status = pisa.CreatePDF(
        BytesIO(html.encode('UTF-8')), dest=response, encoding='UTF-8'
    )

    if pisa_status.err:
        return HttpResponse("PDF oluşturulurken hata oluştu", status=500)
    return response


@login_required
def oturma_plani_pdf1(request, sinav_id):
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


@login_required
def assign_roles(request):
    if request.user.role != 'bolum_baskani':
        return HttpResponseForbidden("Bu sayfaya sadece bölüm başkanı erişebilir.")

    users = CustomUser.objects.filter(role='ogrenci').exclude(is_superuser=True)

    return render(request, 'assign_roles.html', {'users': users})


# views.py
@login_required
def assign_role_to_user1(request, user_id):
    if request.user.role != 'bolum_baskani':
        return HttpResponseForbidden()

    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, instance=user, request_user=request.user)
        if form.is_valid():
            form.save()
            return redirect('assign_roles')
    else:
        form = CustomUserCreationForm(instance=user, request_user=request.user)

    return render(request, 'register.html', {'form': form})

from .forms import RoleSelectionForm
@login_required
def assign_role_to_user(request, user_id):
    if request.user.role != 'bolum_baskani':
        return HttpResponseForbidden("Bu sayfaya sadece bölüm başkanı erişebilir.")

    # Kullanıcıyı al
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        form = RoleSelectionForm(request.POST, instance=user)
        if form.is_valid():
            form.save()  # Kullanıcının rolünü kaydet
            return redirect('assign_roles')  # Rol atama sayfasına yönlendir
    else:
        form = RoleSelectionForm(instance=user)  # Mevcut kullanıcı verileriyle formu yükle

    return render(request, 'role_selection.html', {'form': form, 'user': user})


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from django.contrib.auth.decorators import login_required

GUNLER = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma']

@login_required
def akademisyen_ders_programi(request):
    user = request.user
    # Tüm dersleri çek
    programlar = DersProgrami.objects.filter(ogretim_elemani=user)

    # queryset'i listeye çevir
    programlar = list(programlar)

    # Gün sırasına göre sıralama fonksiyonu
    def gun_index(ders):
        try:
            return GUNLER.index(ders.gun)
        except ValueError:
            return 999  # Eğer gün listede yoksa sona at

    # Sıralama: önce gün, sonra başlama saati
    programlar.sort(key=lambda d: (gun_index(d), d.baslangic_saati))

    return render(request, 'akademisyen_ders_programi.html', {
        'programlar': programlar,
        'gunler': GUNLER,
        'akademisyen': user,
    })

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from django.http import HttpResponse
from io import BytesIO

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.contrib.auth.decorators import login_required
from .models import DersProgrami

from django.http import HttpResponse
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa

GUNLER = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma']

def akademisyen_ders_programi_pdf(request):
    akademisyen = request.user
    programlar = list(DersProgrami.objects.filter(ogretim_elemani=akademisyen))

    def gun_index(ders):
        try:
            return GUNLER.index(ders.gun)
        except ValueError:
            return 999

    programlar.sort(key=lambda d: (gun_index(d), d.baslangic_saati))

    context = {
        'akademisyen': akademisyen,
        'programlar': programlar,
    }

    template_path = 'akademisyen_ders_programi_pdf.html'

    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{akademisyen.username}_ders_programi.pdf"'

    result = BytesIO()

    # Türkçe karakterler için DejaVuSans.ttf fontunu kullanmak için CSS eklenmeli
    # Şablonda font-face ve style ayarlanmalı.

    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result, encoding='UTF-8')
    if not pdf.err:
        response.write(result.getvalue())
        return response
    else:
        return HttpResponse('PDF oluşturulurken hata oluştu.', status=500)

@login_required
def akademisyen_ders_programi_pdf1(request):
    akademisyen = request.user
    programlar = DersProgrami.objects.filter(ogretim_elemani=akademisyen).order_by('gun', 'baslangic_saati')

    template_path = 'akademisyen_ders_programi_pdf.html'  # HTML şablonun
    context = {
        'akademisyen': akademisyen,
        'programlar': programlar,
    }

    # PDF çıktısı için response hazırla
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{akademisyen.username}_ders_programi.pdf"'

    # HTML'i PDF'e dönüştür
    template = get_template(template_path)
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result, encoding='UTF-8')

    if not pdf.err:
        response.write(result.getvalue())
        return response
    else:
        return HttpResponse('PDF oluşturulurken hata oluştu.', status=500)
    

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from .models import DersProgrami, OnaylanmisDersProgrami

def is_bolum_baskani(user):
    return user.role == 'bolum_baskani'

@login_required
@user_passes_test(is_bolum_baskani)
def ders_programini_onayla(request):
    if request.method == "POST":
        # Önceki tüm onaylanmış programları sil
        OnaylanmisDersProgrami.objects.all().delete()

        # Mevcut ders programlarını onaylı tabloya tek tek kopyala
        mevcut_programlar = DersProgrami.objects.all().distinct()
        for p in mevcut_programlar:
            OnaylanmisDersProgrami.objects.create(
                ders=p.ders,
                derslik=p.derslik,
                ogretim_elemani=p.ogretim_elemani,
                gun=p.gun,
                baslangic_saati=p.baslangic_saati,
                bitis_saati=p.bitis_saati
            )
        return redirect('onaylanmis_ders_programi')
    
    return redirect('ders_programi_list')

@login_required
def onaylanmis_ders_programi(request):
    programlar = OnaylanmisDersProgrami.objects.all().order_by('gun', 'baslangic_saati')
    return render(request, 'onaylanmis_ders_programi.html', {'programlar': programlar})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import DersProgrami, DersProgramiYorum
from .forms import YorumForm

@login_required
def yorum_ekle1(request):
    if request.method == 'POST':
        form = YorumForm(request.POST)
        if form.is_valid():
            yorum = form.save(commit=False)
            yorum.yazar = request.user
            # Program bilgisini form üzerinden alıyoruz
            program_id = request.POST.get("program")
            yorum.program = get_object_or_404(DersProgrami, id=program_id)
            yorum.save()
            return redirect('yorumlari_gor')
    else:
        form = YorumForm()

    programlar = DersProgrami.objects.all()
    return render(request, 'yorum_ekle.html', {'form': form, 'programlar': programlar})


@login_required
def yorum_ekle(request):
    if request.method == 'POST':
        form = YorumForm(request.POST)
        if form.is_valid():
            yorum = form.save(commit=False)
            yorum.yazar = request.user
            yorum.save()
            return redirect('home')  # istersen 'yorumlari_gor' da yapabilirsin
    else:
        form = YorumForm()

    return render(request, 'yorum_ekle.html', {'form': form})

@login_required
def yorumlari_gor(request):
    yorumlar = DersProgramiYorum.objects.all().order_by('-tarih')
    return render(request, 'yorumlari_gor.html', {'yorumlar': yorumlar})

@login_required
def yorum_sil(request, yorum_id):
    yorum = get_object_or_404(DersProgramiYorum, id=yorum_id)
    if yorum.yazar == request.user or request.user.role == 'bolum_baskani':
        yorum.delete()
    return redirect('yorumlari_gor')


from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .models import SinavProgrami, OnaylanmisSinavProgrami

def is_bolum_baskani(user):
    return user.role == 'bolum_baskani'



@login_required
@user_passes_test(is_bolum_baskani)
def sinav_programini_onayla(request):
    if request.method == "POST":
        OnaylanmisSinavProgrami.objects.all().delete()  # öncekini sil
        for s in SinavProgrami.objects.all():
            OnaylanmisSinavProgrami.objects.create(
                ders=s.ders,
                derslik=s.derslik,
                tarih=s.tarih,
                saat=s.saat,
                gozetmen=s.gozetmen
            )
        return redirect('onaylanmis_sinav_programi')
    return redirect('sinav_programi_listesi')

@login_required
def onaylanmis_sinav_programi(request):
    sinavlar = OnaylanmisSinavProgrami.objects.all().order_by('tarih', 'saat')
    return render(request, 'onaylanmis_sinav_programi.html', {'sinavlar': sinavlar})

@login_required
def sinav_sil(request, sinav_id):
    if request.method == 'POST':
        sinav = get_object_or_404(SinavProgrami, id=sinav_id)
        sinav.delete()
    return redirect('sinav_listesi')


@login_required
def sinav_yorum_ekle(request):
    if request.method == 'POST':
        form = SinavYorumForm(request.POST)
        if form.is_valid():
            yorum = form.save(commit=False)
            yorum.yazar = request.user
            yorum.save()
            return redirect('home')  # Yorum sonrası yönlendirme
    else:
        form = SinavYorumForm()
    return render(request, 'sinav_yorum_ekle.html', {'form': form})




from django.contrib.auth.decorators import user_passes_test

def is_bolum_baskani(user):
    return user.role == 'bolum_baskani'

@login_required
@user_passes_test(is_bolum_baskani)
def sinav_yorumlari_gor(request):
    yorumlar = SinavYorum.objects.all().order_by('-tarih')
    return render(request, 'sinav_yorumlari_gor.html', {'yorumlar': yorumlar})

@login_required
@user_passes_test(is_bolum_baskani)
def sinav_yorum_sil(request, yorum_id):
    yorum = get_object_or_404(SinavYorum, id=yorum_id)
    yorum.delete()
    return redirect('sinav_yorumlari_gor')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import SinavProgrami

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import SinavProgrami, DersProgrami

@login_required
def akademisyen_verdigi_sinavlar(request):
    user = request.user

    # Akademisyenin verdiği derslerin ID'leri (unique)
    ders_ids = set(DersProgrami.objects.filter(
        ogretim_elemani=user
    ).values_list('ders_id', flat=True))

    # Bu derslere ait sınavları getir
    sinavlar = SinavProgrami.objects.filter(
        ders_id__in=ders_ids
    ).select_related('ders', 'derslik', 'gozetmen').order_by('tarih', 'saat')

    return render(request, 'akademisyen_verdigi_sinavlar.html', {
        'sinavlar': sinavlar,
        'akademisyen': user,
    })

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404
from .models import DersProgrami, CustomUser

GUNLER = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma']

def is_bolum_sekreteri(user):
    return user.role == 'bolum_sekreteri'

@login_required
@user_passes_test(is_bolum_sekreteri)
def bolum_sekreteri_ders_programi1(request):
    akademisyenler = CustomUser.objects.filter(role='akademisyen')
    akademisyen_id = request.GET.get('akademisyen_id')
    secilen = None
    programlar = []

    if akademisyen_id:
        secilen = get_object_or_404(CustomUser, id=akademisyen_id, role='akademisyen')
        programlar = DersProgrami.objects.filter(ogretim_elemani=secilen)

        # Gün ve saat sıralı liste
        def gun_index(d):
            try:
                return GUNLER.index(d.gun)
            except:
                return 999
        programlar = sorted(programlar, key=lambda d: (gun_index(d), d.baslangic_saati))

    return render(request, 'akademisyen_sec_ders_programi.html', {
        'akademisyenler': akademisyenler,
        'secilen': secilen,
        'programlar': programlar,
    })


from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from .models import DersProgrami, CustomUser

GUNLER = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma']

def is_bolum_sekreteri(user):
    return user.role == 'bolum_sekreteri'

@login_required
@user_passes_test(is_bolum_sekreteri)
def bolum_sekreteri_ders_programi(request):
    akademisyenler = CustomUser.objects.filter(role='akademisyen')
    akademisyen_id = request.GET.get('akademisyen_id')

    # Eğer akademisyen seçilirse gösterim sayfasına yönlendir
    if akademisyen_id:
        return redirect('bolum_sekreteri_ders_programi_goster', akademisyen_id=akademisyen_id)

    return render(request, 'akademisyen_sec_ders_programi.html', {
        'akademisyenler': akademisyenler,
    })


@login_required
@user_passes_test(is_bolum_sekreteri)
def bolum_sekreteri_ders_programi_goster1(request, akademisyen_id):
    secilen = get_object_or_404(CustomUser, id=akademisyen_id, role='akademisyen')
    programlar = DersProgrami.objects.filter(ogretim_elemani=secilen)

    def gun_index(d):
        try:
            return GUNLER.index(d.gun)
        except:
            return 999
    programlar = sorted(programlar, key=lambda d: (gun_index(d), d.baslangic_saati))

    return render(request, 'akademisyen_ders_programi_detay.html', {
        'secilen': secilen,
        'programlar': programlar,
    })

@login_required
@user_passes_test(is_bolum_sekreteri)
def bolum_sekreteri_ders_programi_goster(request, akademisyen_id):
    secilen = get_object_or_404(CustomUser, id=akademisyen_id, role='akademisyen')
    programlar = DersProgrami.objects.filter(ogretim_elemani=secilen)

    def gun_index(d):
        try:
            return GUNLER.index(d.gun)
        except:
            return 999

    programlar = sorted(programlar, key=lambda d: (gun_index(d), d.baslangic_saati))

    return render(request, 'akademisyen_ders_programi_detay.html', {
        'secilen': secilen,
        'akademisyen': secilen,  # EKLENDİ: PDF butonu düzgün çalışsın diye
        'programlar': programlar,
    })



from django.contrib.auth import get_user_model
from django.template.loader import get_template
from django.http import HttpResponse
from io import BytesIO
from xhtml2pdf import pisa

GUNLER = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma']
User = get_user_model()

def secilen_akademisyen_ders_programi_pdf(request, akademisyen_id):
    akademisyen = get_object_or_404(User, id=akademisyen_id)

    programlar = list(DersProgrami.objects.filter(ogretim_elemani=akademisyen))

    def gun_index(ders):
        try:
            return GUNLER.index(ders.gun)
        except ValueError:
            return 999

    programlar.sort(key=lambda d: (gun_index(d), d.baslangic_saati))

    context = {
        'akademisyen': akademisyen,
        'programlar': programlar,
    }

    template_path = 'akademisyen_ders_programi_pdf.html'
    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{akademisyen.username}_ders_programi.pdf"'

    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result, encoding='UTF-8')

    if not pdf.err:
        response.write(result.getvalue())
        return response
    else:
        return HttpResponse('PDF oluşturulurken hata oluştu.', status=500)

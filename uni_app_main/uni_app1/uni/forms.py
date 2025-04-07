from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import DersProgrami
from .models import Ders, Derslik
from .models import SinavProgrami, Derslik, Ders, CustomUser

class DersDuzenleForm(forms.ModelForm):
    class Meta:
        model = Ders
        fields = ['kod', 'ad', 'ogrenci_sayisi','kredi','bolum']

class DersForm(forms.ModelForm):
    class Meta:
        model = Ders
        fields = ['kod', 'ad','ogrenci_sayisi' ,'kredi', 'bolum']

class DerslikForm(forms.ModelForm):
    class Meta:
        model = Derslik
        fields = ['ad', 'kapasite']

class DersProgramiForm(forms.ModelForm):
    class Meta:
        model = DersProgrami
        fields = ['ders', 'derslik', 'ogretim_elemani', 'gun', 'baslangic_saati', 'bitis_saati']
        widgets = {
            'baslangic_saati': forms.TimeInput(attrs={'type': 'time'}),
            'bitis_saati': forms.TimeInput(attrs={'type': 'time'}),
        }



class CustomUserCreationForm(UserCreationForm):
    # Bölüm Başkanı tarafından belirlenen roller
    role_choices = [
        ('akademisyen', 'Akademisyen'),
        ('ogrenci', 'Öğrenci'),
        ('bolum_sekreteri', 'Bölüm Sekreteri'),
    ]
    
    role = forms.ChoiceField(choices=role_choices, label="Rol Seçin", required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']



class SinavProgramiForm1(forms.ModelForm):
    class Meta:
        model = SinavProgrami
        fields = ['ders', 'tarih', 'saat', 'derslik', 'gozetmen']

    def __init__(self, *args, **kwargs):
        super(SinavProgramiForm1, self).__init__(*args, **kwargs)
        
        # Ders seçildiğinde uygun derslikleri filtrele
        if 'ders' in self.data:
            try:
                ders_id = int(self.data.get('ders'))
                ders = Ders.objects.get(id=ders_id)
                
                # Minimum kapasite hesaplama (dersliği 3'e böl, tam kısmını al)
                minimum_kapasite = (ders.ogrenci_sayisi // 3) or 1
                
                # Kapasitesi yeterli olan derslikleri listele
                self.fields['derslik'].queryset = Derslik.objects.filter(kapasite__gte=minimum_kapasite)
            except (ValueError, TypeError, Ders.DoesNotExist):
                self.fields['derslik'].queryset = Derslik.objects.none()
        else:
            self.fields['derslik'].queryset = Derslik.objects.none()

        # Sadece akademisyenleri göster
        self.fields['gozetmen'].queryset = CustomUser.objects.filter(role='akademisyen')

class SinavProgramiForm(forms.ModelForm):
    class Meta:
        model = SinavProgrami
        fields = ['ders', 'tarih', 'saat', 'derslik', 'gozetmen']

    def __init__(self, *args, **kwargs):
        super(SinavProgramiForm, self).__init__(*args, **kwargs)

        # Varsayılan olarak tüm derslikleri göster (form yüklenirken)
        self.fields['derslik'].queryset = Derslik.objects.all()

        if 'ders' in self.data:
            try:
                ders_id = int(self.data.get('ders'))
                ders = Ders.objects.get(id=ders_id)

                # Dersin öğrenci sayısını kontrol et (None veya 0 olmamalı)
                ogrenci_sayisi = ders.ogrenci_sayisi if ders.ogrenci_sayisi else 1

                # Derslik kapasitesi kontrolü
                uygun_derslikler = Derslik.objects.filter(kapasite__gte=ogrenci_sayisi)

                # Dersliklerin filtrelenmiş listesini kullan
                self.fields['derslik'].queryset = uygun_derslikler

            except (ValueError, TypeError, Ders.DoesNotExist):
                self.fields['derslik'].queryset = Derslik.objects.none()

        # Sadece akademisyenleri göster
        self.fields['gozetmen'].queryset = CustomUser.objects.filter(role='akademisyen')

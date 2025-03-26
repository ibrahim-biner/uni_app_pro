from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import DersProgrami
from .models import Ders, Derslik

class DersDuzenleForm(forms.ModelForm):
    class Meta:
        model = Ders
        fields = ['kod', 'ad', 'kredi', 'bolum']

class DersForm(forms.ModelForm):
    class Meta:
        model = Ders
        fields = ['kod', 'ad', 'kredi', 'bolum']

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

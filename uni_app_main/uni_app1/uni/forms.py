from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

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

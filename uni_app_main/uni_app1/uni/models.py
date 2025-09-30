from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('bolum_baskani', 'Bölüm Başkanı'),
        ('bolum_sekreteri', 'Bölüm Sekreteri'),
        ('akademisyen', 'Akademisyen'),
        ('ogrenci', 'Öğrenci'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.role:
            group, created = Group.objects.get_or_create(name=self.role)
            self.groups.add(group)



User = get_user_model()  

class Ders(models.Model):
    kod = models.CharField(max_length=10, unique=True)
    ad = models.CharField(max_length=100)
    ogrenci_sayisi = models.IntegerField(default=0) 
    kredi = models.IntegerField()
    bolum = models.CharField(max_length=100) 

    def __str__(self):
        return f"{self.kod} - {self.ad}"

class Derslik(models.Model):
    ad = models.CharField(max_length=50, unique=True)
    kapasite = models.IntegerField()

    def __str__(self):
        return self.ad

class DersProgrami(models.Model):
    GUNLER = [
        ('Pazartesi', 'Pazartesi'),
        ('Salı', 'Salı'),
        ('Çarşamba', 'Çarşamba'),
        ('Perşembe', 'Perşembe'),
        ('Cuma', 'Cuma'),
    ]

    ders = models.ForeignKey(Ders, on_delete=models.CASCADE)
    derslik = models.ForeignKey(Derslik, on_delete=models.CASCADE)
    ogretim_elemani = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'akademisyen'})
    gun = models.CharField(max_length=10, choices=GUNLER)
    baslangic_saati = models.TimeField()
    bitis_saati = models.TimeField()

    class Meta:
        unique_together = ['ders', 'gun', 'baslangic_saati']

    def __str__(self):
        return f"{self.ders} - {self.gun} ({self.baslangic_saati} - {self.bitis_saati})"
    



class SinavProgrami(models.Model):
    ders = models.ForeignKey(Ders, on_delete=models.CASCADE)
    derslik = models.ForeignKey(Derslik, on_delete=models.CASCADE)
    tarih = models.DateField()
    saat = models.TimeField()
    gozetmen = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'akademisyen'})

    def __str__(self):
        return f"{self.ders.ad} - {self.tarih} {self.saat}"
    


class OturmaPlani(models.Model):
    sinav = models.ForeignKey(SinavProgrami, on_delete=models.CASCADE)
    ogrenci = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'ogrenci'})
    sira_no = models.IntegerField()  # Sıra numarası

    class Meta:
        unique_together = ('sinav', 'ogrenci')  # Aynı sınav için aynı öğrenci tekrar eklenemez



class OnaylanmisDersProgrami(models.Model):
    ders = models.ForeignKey(Ders, on_delete=models.CASCADE)
    derslik = models.ForeignKey(Derslik, on_delete=models.CASCADE)
    ogretim_elemani = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'akademisyen'})
    gun = models.CharField(max_length=10, choices=DersProgrami.GUNLER)
    baslangic_saati = models.TimeField()
    bitis_saati = models.TimeField()
    onay_tarihi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ders.ad} - {self.gun} ({self.baslangic_saati}-{self.bitis_saati})"
    

class DersProgramiYorum(models.Model):
    program = models.ForeignKey(DersProgrami, on_delete=models.CASCADE)
    yazar = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'akademisyen'})
    icerik = models.TextField()
    tarih = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.yazar.username} - {self.program} - {self.tarih.strftime('%Y-%m-%d %H:%M')}"
    

class OnaylanmisSinavProgrami(models.Model):
    ders = models.ForeignKey(Ders, on_delete=models.CASCADE)
    derslik = models.ForeignKey(Derslik, on_delete=models.CASCADE)
    tarih = models.DateField()
    saat = models.TimeField()
    gozetmen = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'akademisyen'})

    def __str__(self):
        return f"{self.ders.ad} - {self.tarih} {self.saat}"


class SinavYorum(models.Model):
    sinav = models.ForeignKey(SinavProgrami, on_delete=models.CASCADE)
    yazar = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'akademisyen'})
    icerik = models.TextField()
    tarih = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.yazar.username} - {self.sinav} - {self.tarih.strftime('%Y-%m-%d %H:%M')}"


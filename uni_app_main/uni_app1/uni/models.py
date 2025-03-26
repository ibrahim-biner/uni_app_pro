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
        # Kullanıcı rolü belirtildiğinde ilgili gruba dahil edilir
        if self.role:
            group, created = Group.objects.get_or_create(name=self.role)
            self.groups.add(group)



User = get_user_model()  # Django'nun özel kullanıcı modelini alıyoruz

class Ders(models.Model):
    kod = models.CharField(max_length=10, unique=True)
    ad = models.CharField(max_length=100)
    kredi = models.IntegerField()
    bolum = models.CharField(max_length=100)  # Hangi bölümde olduğu

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

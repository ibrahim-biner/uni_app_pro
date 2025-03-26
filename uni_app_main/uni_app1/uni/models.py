from django.contrib.auth.models import AbstractUser, Group
from django.db import models

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

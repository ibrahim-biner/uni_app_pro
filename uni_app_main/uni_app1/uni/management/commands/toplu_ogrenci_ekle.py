import csv
from django.core.management.base import BaseCommand
from uni.models import CustomUser

class Command(BaseCommand):
    help = 'CSV dosyasından toplu öğrenci ekler'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help="Öğrenci listesinin CSV dosya yolu")

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # İlk satır başlık olduğu için atlıyoruz
            
            for row in reader:
                username = row[0]  # Sadece username var

                # Varsayılan e-posta, şifre ve rol belirle
                email = f"{username}@ogrenci.edu.tr"
                password = "123456"  # Tüm öğrenciler için varsayılan parola
                role = "ogrenci"

                # Eğer öğrenci zaten ekli değilse ekle
                if not CustomUser.objects.filter(username=username).exists():
                    CustomUser.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        role=role
                    )
                    self.stdout.write(self.style.SUCCESS(f"✅ {username} eklendi."))
                else:
                    self.stdout.write(self.style.WARNING(f"⚠️ {username} zaten mevcut."))

        self.stdout.write(self.style.SUCCESS("🎉 Tüm öğrenciler başarıyla eklendi!"))

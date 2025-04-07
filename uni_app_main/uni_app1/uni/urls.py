from django.urls import path
from . import views
from .views import user_register, user_login, user_logout
from .views import ders_programi_list, ders_programi_ekle, ders_programi_sil,ders_ekle, derslik_ekle,ders_listesi,derslik_listesi
from .views import ders_duzenle, ders_sil,derslik_sil,derslik_detay,sinav_ekle,sinav_listesi

urlpatterns = [
    path("login/", user_login, name="login"),
    path("register/", user_register, name="register"),
    path("logout/", user_logout, name="logout"),
    path('home/', views.home, name='home'),
    path('ders-programi/', ders_programi_list, name='ders_programi_list'),
    path('ders-programi/ekle/', ders_programi_ekle, name='ders_programi_ekle'),
    path('ders-programi/sil/<int:pk>/', ders_programi_sil, name='ders_programi_sil'),
    path('ders/ekle/', ders_ekle, name='ders_ekle'),
    path('derslik/ekle/', derslik_ekle, name='derslik_ekle'),
    path('ders/listesi/', ders_listesi, name='ders_listesi'),
    path('derslik/listesi/', derslik_listesi, name='derslik_listesi'),
    path('ders/duzenle/<int:ders_id>/', ders_duzenle, name='ders_duzenle'),
     path('ders/sil/<int:ders_id>/', ders_sil, name='ders_sil'),
     path('derslik/sil/<int:derslik_id>/', derslik_sil, name='derslik_sil'),
     path('derslik/<int:derslik_id>/', derslik_detay, name='derslik_detay'),
      path('sinav-ekle/', sinav_ekle, name='sinav_ekle'),
    path('sinav-listesi/', sinav_listesi, name='sinav_listesi'),
    path('oturma-plani/<int:sinav_id>/', views.oturma_plani_goruntule, name='oturma_plani'),
    path('oturma-plani/pdf/<int:sinav_id>/', views.oturma_plani_pdf, name='oturma_plani_pdf'),
    
]
    


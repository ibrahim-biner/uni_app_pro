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
    path('assign_roles/', views.assign_roles, name='assign_roles'),
    path('assign_role/<int:user_id>/', views.assign_role_to_user, name='assign_role_to_user'),
    path('ders_programi/duzenle/<int:pk>/', views.ders_programi_duzenle, name='ders_programi_duzenle'),
    path('akademisyen/ders-programi/', views.akademisyen_ders_programi, name='akademisyen_ders_programi'),
    path('akademisyen/ders-programi/pdf/', views.akademisyen_ders_programi_pdf, name='akademisyen_ders_programi_pdf'),
     path('ders-programi/onayla/', views.ders_programini_onayla, name='ders_programi_onayla'),
    path('ders-programi/onaylanmis/', views.onaylanmis_ders_programi, name='onaylanmis_ders_programi'),
    path('ders-programi/yorum-ekle/', views.yorum_ekle, name='yorum_ekle'),
    path('yorumlar/', views.yorumlari_gor, name='yorumlari_gor'),
    path('yorumlar/sil/<int:yorum_id>/', views.yorum_sil, name='yorum_sil'),
    path('sinav-onayla/', views.sinav_programini_onayla, name='sinav_programini_onayla'),
    path('onayli-sinav-listesi/', views.onaylanmis_sinav_programi, name='onaylanmis_sinav_programi'),
    path('sinav/<int:sinav_id>/sil/', views.sinav_sil, name='sinav_sil'),
    path('sinav-yorum-ekle/', views.sinav_yorum_ekle, name='sinav_yorum_ekle'),
    path('sinav-yorumlari/', views.sinav_yorumlari_gor, name='sinav_yorumlari_gor'),
    path('sinav-yorum-sil/<int:yorum_id>/', views.sinav_yorum_sil, name='sinav_yorum_sil'),
    
]
    

    


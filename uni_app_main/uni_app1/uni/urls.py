from django.urls import path
from . import views
from .views import user_register, user_login, user_logout

urlpatterns = [
    path("login/", user_login, name="login"),
    path("register/", user_register, name="register"),
    path("logout/", user_logout, name="logout"),
    path('home/', views.home, name='home'),
]

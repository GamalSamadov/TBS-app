
from django.urls import path, include
from django.contrib import admin
from . import AdminViews, UstozViews, MudarrisViews, views


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.loginPage, name="login"),
    path('doLogin/', views.doLogin, name="doLogin"),
#     path('get_user_details/', views.get_user_details, name="get_user_details"),
    path('chiqish/', views.chiqish, name="chiqish"),


     # Admin Urls
    path('check_email_exist/', AdminViews.check_email_exist,
         name="check_email_exist"),
    path('check_username_exist/', AdminViews.check_username_exist,
         name="check_username_exist"),

     path('admin_asosiy/', AdminViews.admin_asosiy, name="admin_asosiy"),
     path('admin_profil/', AdminViews.admin_profil, name="admin_profil"),
     path('admin_profil/tahrirlash/', AdminViews.admin_profil_tahrirlash, name="admin_profil_tahrirlash"),
     path('admin_profil/tahrirlash/so\'ratni_o\'chirish/', AdminViews.admin_profile_suratni_uchirish, name="admin_profil_suratni_uchirish"),


  
    # # Ustoz Urls
    path('ustoz_asosiy/', UstozViews.ustoz_asosiy, name="ustoz_asosiy"),

    # # Mudarris Urls
    path('mudarris_asosiy/', MudarrisViews.mudarris_asosiy, name="mudarris_asosiy"),

]

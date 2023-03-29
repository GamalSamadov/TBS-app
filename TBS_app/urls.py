
from django.urls import path, include
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from . import AdminViews, UstozViews, MudarrisViews, views

# app_name = 'TBS_app'

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.loginPage, name="login"),
    path('doLogin/', views.doLogin, name="doLogin"),
#     path('get_user_details/', views.get_user_details, name="get_user_details"),
    path('chiqish/', views.chiqish, name="chiqish"),
    path('foydalanuvchi-nomini-tekshirish/', csrf_exempt(AdminViews.UsernameTekshirish.as_view()), name='foydalanuvchi_nomini_tekshirish'),
    path('emailni-tekshirish/', csrf_exempt(AdminViews.EmailTekshirish.as_view()), name="emailni_tekshirish"),

     # Admin Urls
     path('admin_asosiy/', AdminViews.admin_asosiy, name="admin_asosiy"),
     path('admin_profil/', AdminViews.admin_profil, name="admin_profil"),
     path('admin_profil/tahrirlash/', AdminViews.admin_profil_tahrirlash, name="admin_profil_tahrirlash"),
     path('admin_profil/tahrirlash/so\'ratni_o\'chirish/', AdminViews.admin_profil_suratni_uchirish, name="admin_profil_suratni_uchirish"),

    path('ustozlar/', AdminViews.ustozlar, name="ustozlar"),
    path('ustozlar/kiritish/', AdminViews.ustoz_kiritish, name="ustoz_kiritish"),
    path('ustozlar/<int:id>/', AdminViews.ustoz_profil, name="ustoz_profil"),
    path('ustozlar/<int:id>/tahrirlash/', AdminViews.ustoz_profil_tahrirlash, name="ustoz_profil_tahrirlash"),
    path('ustozlar/<int:id>/o\'chirish/', AdminViews.ustozni_uchirish, name="ustozni_uchirish"),
    path('ustozlar/<int:id>/tahrirlash/profil_so\'ratni_o\'chirish/', AdminViews.ustoz_profil_suratni_uchirish, name="ustoz_profil_suratni_uchirish"),
  
    path('xujralar/', AdminViews.hujralar, name="hujralar"),
    path('xujralar/kiritish/', AdminViews.hujra_kiritish, name="hujra_kiritish"),
    path('xujralar/<int:id>/', AdminViews.hujra_profil, name="hujra_profil"),
    path('xujralar/<int:id>/tahrirlash/', AdminViews.hujra_profil_tahrirlash, name="hujra_profil_tahrirlash"),
    path('xujralar/<int:id>/o\'chirish/', AdminViews.hujra_uchirish, name="hujra_uchirish"),

    path('mudarrislar/', AdminViews.mudarrislar, name="mudarrislar"),
    path('mudarrislar/kiritish/', AdminViews.mudarris_kiritish, name="mudarris_kiritish"),
    path('mudarrislar/<int:id>/', AdminViews.mudarris_profil, name="mudarris_profil"),
    path('mudarrislar/<int:id>/tahrirlash/', AdminViews.mudarris_profil_tahrirlash, name="mudarris_profil_tahrirlash"),
    path('mudarrislar/<int:id>/tahrirlash/paspurt/', AdminViews.mudarris_paspurt_tahrirlash, name="mudarris_paspurt_tahrirlash"),
    path('mudarrislar/<int:id>/o\'chirish/', AdminViews.mudarrisni_uchirish, name="mudarrisni_uchirish"),
    path('mudarrislar/<int:id>/tahrirlash/profil_so\'ratni_o\'chirish/', AdminViews.mudarris_profil_suratni_uchirish, name="mudarris_profil_suratni_uchirish"),
    path('mudarrislar/<int:id>/tahrirlash/paspurt_so\'ratni_o\'chirish/', AdminViews.mudarris_pasport_suratni_uchirish, name="mudarris_paspurt_suratni_uchirish"),
  
    path('talabalar/', AdminViews.talabalar, name="talabalar"),
    path('talabalar/kiritish/', AdminViews.talaba_kiritish, name="talaba_kiritish"),
    path('talabalar/<int:id>/', AdminViews.talaba_profil, name="talaba_profil"),
    path('talabalar/<int:id>/tahrirlash/', AdminViews.talaba_profil_tahrirlash, name="talaba_profil_tahrirlash"),
    path('talabalar/<int:id>/tahrirlash/paspurt/', AdminViews.talaba_paspurt_tahrirlash, name="talaba_paspurt_tahrirlash"),
    path('talabalar/<int:id>/o\'chirish/', AdminViews.talabani_uchirish, name="talabani_uchirish"),
    path('talabalar/<int:id>/tahrirlash/profil_so\'ratni_o\'chirish/', AdminViews.talaba_profil_suratni_uchirish, name="talaba_profil_suratni_uchirish"),
    path('talabalar/<int:id>/tahrirlash/paspurt_so\'ratni_o\'chirish/', AdminViews.talaba_pasport_suratni_uchirish, name="talaba_pasport_suratni_uchirish"),

  
    # # Ustoz Urls
    path('ustoz_asosiy/', UstozViews.ustoz_asosiy, name="ustoz_asosiy"),

    # # Mudarris Urls
    path('mudarris_asosiy/', MudarrisViews.mudarris_asosiy, name="mudarris_asosiy"),

]

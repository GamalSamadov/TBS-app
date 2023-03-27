
from django.urls import path, include
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from . import AdminViews, UstozViews, MudarrisViews, views


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.loginPage, name="login"),
    path('doLogin/', views.doLogin, name="doLogin"),
#     path('get_user_details/', views.get_user_details, name="get_user_details"),
    path('chiqish/', views.chiqish, name="chiqish"),
    path('foydalanuvchi-nomini-tekshirish/', csrf_exempt(AdminViews.UsernameTekshirish.as_view())),
    path('emailni-tekshirish/', csrf_exempt(AdminViews.EmailTekshirish.as_view())),

     # Admin Urls
     path('admin_asosiy/', AdminViews.admin_asosiy, name="admin_asosiy"),
     path('admin_profil/', AdminViews.admin_profil, name="admin_profil"),
     path('admin_profil/tahrirlash/', AdminViews.admin_profil_tahrirlash, name="admin_profil_tahrirlash"),
     path('admin_profil/tahrirlash/so\'ratni_o\'chirish/', AdminViews.admin_profil_suratni_uchirish, name="admin_profil_suratni_uchirish"),

     path('hujralar/', AdminViews.hujralar, name="hujralar"),
     path('kurslari/', AdminViews.kurslar, name="kurslar"),
    #  path('kurslari/kiritish/', AdminViews.kurslar_kiritish, name="kurslar_kiritish"),
    #  path('kurslari/<int:id>/', AdminViews.kurs_profil, name="kurs_profil"),

    path('ustozlar/', AdminViews.ustozlar, name="ustozlar"),
    path('ustozlar/kiritish/', AdminViews.ustoz_kiritish, name="ustoz_kiritish"),
    path('ustozlar/<int:id>/', AdminViews.ustoz_profil, name="ustoz_profil"),
    path('ustozlar/<int:id>/tahrirlash/', AdminViews.ustoz_profil_tahrirlash, name="ustoz_profil_tahrirlash"),
    path('ustozlar/<int:id>/o\'chirish/', AdminViews.ustozni_uchirish, name="ustozni_uchirish"),
    path('ustozlar/<int:id>/tahrirlash/so\'ratni_o\'chirish/', AdminViews.ustoz_profil_suratni_uchirish, name="ustoz_profil_suratni_uchirish"),
  


  
    # # Ustoz Urls
    path('ustoz_asosiy/', UstozViews.ustoz_asosiy, name="ustoz_asosiy"),

    # # Mudarris Urls
    path('mudarris_asosiy/', MudarrisViews.mudarris_asosiy, name="mudarris_asosiy"),

]

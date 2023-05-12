from django.urls import path, include
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from . import AdminViews, UstozViews, MudarrisViews, views

urlpatterns = [
    path('', views.loginPage, name="login"),
    path('kirish/', views.doLogin, name="doLogin"),
    path('chiqish/', views.chiqish, name="chiqish"),
    path('foydalanuvchi-nomini-tekshirish/', csrf_exempt(AdminViews.UsernameTekshirish.as_view()), name='foydalanuvchi_nomini_tekshirish'),
    path('emailni-tekshirish/', csrf_exempt(AdminViews.EmailTekshirish.as_view()), name="emailni_tekshirish"),
    # -------------------------
     # Admin Urls
     # Admin
     path('admin_asosiy/', AdminViews.admin_asosiy, name="admin_asosiy"),
     path('admin_profil/', AdminViews.admin_profil, name="admin_profil"),
     path('admin_profil/tahrirlash/', AdminViews.admin_profil_tahrirlash, name="admin_profil_tahrirlash"),
     path('admin_profil/tahrirlash/so\'ratni_o\'chirish/', AdminViews.admin_profil_suratni_uchirish, name="admin_profil_suratni_uchirish"),
    # Ustoz
    path('ustozlar/', AdminViews.ustozlar, name="ustozlar"),
    path('ustozlar/kiritish/', AdminViews.ustoz_kiritish, name="ustoz_kiritish"),
    path('ustozlar/<int:id>/', AdminViews.ustoz_profil, name="ustoz_profil"),
    path('ustozlar/<int:id>/mudarrislar/', AdminViews.ustoz_profil_mudarrislar, name="ustoz_profil_mudarrislar"),
    path('ustozlar/<int:id>/talabalar/', AdminViews.ustoz_profil_talabalar, name="ustoz_profil_talabalar"),
    path('ustozlar/<int:id>/fanlar/', AdminViews.ustoz_profil_fanlar, name="ustoz_profil_fanlar"),
    path('ustozlar/<int:id>/hujralar/', AdminViews.ustoz_profil_hujralar, name="ustoz_profil_hujralar"),
    path('ustozlar/<int:id>/hujralar/kiritish/', AdminViews.ustoz_profil_hujralar_kiritish, name="ustoz_profil_hujralar_kiritish"),
    path('ustozlar/<int:ustozId>/hujralar/<int:hujraId>/o\'chirish/', AdminViews.ustoz_profil_hujralar_uchirish, name="ustoz_profil_hujralar_uchirish"),
    path('ustozlar/<int:id>/tahrirlash/', AdminViews.ustoz_profil_tahrirlash, name="ustoz_profil_tahrirlash"),
    path('ustozlar/<int:id>/o\'chirish/', AdminViews.ustozni_uchirish, name="ustozni_uchirish"),
    path('ustozlar/<int:id>/tahrirlash/profil_so\'ratni_o\'chirish/', AdminViews.ustoz_profil_suratni_uchirish, name="ustoz_profil_suratni_uchirish"),
    # Hujra
    path('xujralar/', AdminViews.hujralar, name="hujralar"),
    path('xujralar/kiritish/', AdminViews.hujra_kiritish, name="hujra_kiritish"),
    path('xujralar/<int:id>/', AdminViews.hujra_profil, name="hujra_profil"),
    path('xujralar/<int:id>/talabalar/', AdminViews.hujra_profil_talabalar, name="hujra_profil_talabalar"),
    path('xujralar/<int:id>/talabalar/kiritish/', AdminViews.hujra_profil_talabalar_kiritish, name="hujra_profil_talabalar_kiritish"),
    path('xujralar/<int:hujraId>/talabalar/<int:talabaId>/o\'chirish/', AdminViews.hujra_profil_talabalar_uchirish, name="hujra_profil_talabalar_uchirish"),
    path('xujralar/<int:id>/mudarrislar/', AdminViews.hujra_profil_mudarrislar, name="hujra_profil_mudarrislar"),
    path('xujralar/<int:id>/mudarrislar/kiritish/', AdminViews.hujra_profil_mudarrislar_kiritish, name="hujra_profil_mudarrislar_kiritish"),
    path('xujralar/<int:hujraId>/mudarrislar/<int:mudarrisId>/o\'chirish/', AdminViews.hujra_profil_mudarrislar_uchirish, name="hujra_profil_mudarrislar_uchirish"),
    path('xujralar/<int:id>/tahrirlash/', AdminViews.hujra_profil_tahrirlash, name="hujra_profil_tahrirlash"),
    path('xujralar/<int:id>/o\'chirish/', AdminViews.hujra_uchirish, name="hujra_uchirish"),
    #Mudarris
    path('mudarrislar/', AdminViews.mudarrislar, name="mudarrislar"),
    path('mudarrislar/kiritish/', AdminViews.mudarris_kiritish, name="mudarris_kiritish"),
    path('mudarrislar/<int:id>/', AdminViews.mudarris_profil, name="mudarris_profil"),
    path('mudarrislar/<int:id>/o\'z_fanlar/', AdminViews.mudarris_profil_uz_fanlar, name="mudarris_profil_uz_fanlar"),
    path('mudarrislar/<int:id>/fanlar/', AdminViews.mudarris_profil_fanlar, name="mudarris_profil_fanlar"),
    path('mudarrislar/<int:id>/fanlar/kiritish/', AdminViews.mudarris_profil_fanlar_kiritish, name="mudarris_profil_fanlar_kiritish"),
    path('mudarrislar/<int:id>/talabalar/', AdminViews.mudarris_profil_talabalar, name="mudarris_profil_talabalar"),
    path('mudarrislar/<int:id>/tahrirlash/', AdminViews.mudarris_profil_tahrirlash, name="mudarris_profil_tahrirlash"),
    path('mudarrislar/<int:id>/tahrirlash/paspurt/', AdminViews.mudarris_paspurt_tahrirlash, name="mudarris_paspurt_tahrirlash"),
    path('mudarrislar/<int:id>/o\'chirish/', AdminViews.mudarrisni_uchirish, name="mudarrisni_uchirish"),
    path('mudarrislar/<int:id>/tahrirlash/profil_so\'ratni_o\'chirish/', AdminViews.mudarris_profil_suratni_uchirish, name="mudarris_profil_suratni_uchirish"),
    path('mudarrislar/<int:id>/tahrirlash/paspurt_so\'ratni_o\'chirish/', AdminViews.mudarris_pasport_suratni_uchirish, name="mudarris_paspurt_suratni_uchirish"),
    # Talaba
    path('talabalar/', AdminViews.talabalar, name="talabalar"),
    path('talabalar/kiritish/', AdminViews.talaba_kiritish, name="talaba_kiritish"),
    path('talabalar/<int:id>/', AdminViews.talaba_profil, name="talaba_profil"),
    path('talabalar/<int:id>/fanlar/', AdminViews.talaba_profil_fanlar, name="talaba_profil_fanlar"),
    path('talabalar/<int:id>/tahrirlash/', AdminViews.talaba_profil_tahrirlash, name="talaba_profil_tahrirlash"),
    path('talabalar/<int:id>/tahrirlash/paspurt/', AdminViews.talaba_paspurt_tahrirlash, name="talaba_paspurt_tahrirlash"),
    path('talabalar/<int:id>/o\'chirish/', AdminViews.talabani_uchirish, name="talabani_uchirish"),
    path('talabalar/<int:id>/tahrirlash/profil_so\'ratni_o\'chirish/', AdminViews.talaba_profil_suratni_uchirish, name="talaba_profil_suratni_uchirish"),
    path('talabalar/<int:id>/tahrirlash/paspurt_so\'ratni_o\'chirish/', AdminViews.talaba_pasport_suratni_uchirish, name="talaba_pasport_suratni_uchirish"),
    # Fan Ustoz - Talaba
    path('fanlar/ustoz_talaba/', AdminViews.fanlar_ustoz_talaba, name="fanlar_ustoz_talaba"),
    path('fanlar/ustoz_talaba/<int:id>/', AdminViews.fan_ustoz_talaba_profil, name="fan_ustoz_talaba_profil"),
    path('fanlar/ustoz_talaba/<int:id>/tahrirlash/', AdminViews.fan_ustoz_talaba_profil_tahrirlash, name="fan_ustoz_talaba_profil_tahrirlash"),
    path('fanlar/ustoz_talaba/<int:id>/talabalar/', AdminViews.fan_ustoz_talaba_profil_talabalar, name="fan_ustoz_talaba_profil_talabalar"),
    path('fanlar/ustoz_talaba/<int:id>/talabalar/kiritish/', AdminViews.fan_ustoz_talaba_profil_talabalar_kiritish, name="fan_ustoz_talaba_profil_talabalar_kiritish"),
    path('fanlar/ustoz_talaba/<int:fanId>/talabalar/<int:talabaId>/uchirish/', AdminViews.fan_ustoz_talaba_profil_talabalar_uchirish, name="fan_ustoz_talaba_profil_talabalar_uchirish"),
    path('fanlar/ustoz_talaba/kiritish/', AdminViews.fan_ustoz_talaba_kiritish, name='fan_ustoz_talaba_kiritish'),
    path('fanlar/ustoz_talaba/<int:id>/uchirish/', AdminViews.fan_ustoz_talaba_uchirish, name="fan_ustoz_talaba_uchirish"),
    # Fan Ustoz - Mudarris
    path('fanlar/ustoz_mudarris/', AdminViews.fanlar_ustoz_mudarris, name="fanlar_ustoz_mudarris"),
    path('fanlar/ustoz_mudarris/<int:id>/', AdminViews.fan_ustoz_mudarris_profil, name="fan_ustoz_mudarris_profil"),
    path('fanlar/ustoz_mudarris/<int:id>/tahrirlash/', AdminViews.fan_ustoz_mudarris_profil_tahrirlash, name="fan_ustoz_mudarris_profil_tahrirlash"),
    path('fanlar/ustoz_mudarris/<int:id>/mudarrislar/', AdminViews.fan_ustoz_mudarris_profil_mudarrislar, name="fan_ustoz_mudarris_profil_mudarrislar"),
    path('fanlar/ustoz_mudarris/<int:id>/mudarrislar/kiritish/', AdminViews.fan_ustoz_mudarris_profil_mudarrislar_kiritish, name="fan_ustoz_mudarris_profil_mudarrislar_kiritish"),
    path('fanlar/ustoz_mudarris/<int:fanId>/mudarrislar/<int:mudarrisId>/uchirish/', AdminViews.fan_ustoz_mudarris_profil_mudarrislar_uchirish, name="fan_ustoz_mudarris_profil_mudarrislar_uchirish"),
    path('fanlar/ustoz_mudarris/kiritish/', AdminViews.fan_ustoz_mudarris_kiritish, name='fan_ustoz_mudarris_kiritish'),
    path('fanlar/ustoz_mudarris/<int:id>/uchirish/', AdminViews.fan_ustoz_mudarris_uchirish, name="fan_ustoz_mudarris_uchirish"),
    # Fan Mudarris - talaba
    path('fanlar/mudarris_talaba/', AdminViews.fanlar_mudarris_talaba, name="fanlar_mudarris_talaba"),
    path('fanlar/mudarris_talaba/<int:id>/', AdminViews.fan_mudarris_talaba_profil, name="fan_mudarris_talaba_profil"),
    path('fanlar/mudarris_talaba/<int:id>/tahrirlash/', AdminViews.fan_mudarris_talaba_profil_tahrirlash, name="fan_mudarris_talaba_profil_tahrirlash"),
    path('fanlar/mudarris_talaba/<int:id>/talabalar/', AdminViews.fan_mudarris_talaba_profil_talabalar, name="fan_mudarris_talaba_profil_talabalar"),
    path('fanlar/mudarris_talaba/<int:id>/talabalar/kiritish/', AdminViews.fan_mudarris_talaba_profil_talabalar_kiritish, name="fan_mudarris_talaba_profil_talabalar_kiritish"),
    path('fanlar/mudarris_talaba/<int:fanId>/talabalar/<int:talabaId>/uchirish/', AdminViews.fan_mudarris_talaba_profil_talabalar_uchirish, name="fan_mudarris_talaba_profil_talabalar_uchirish"),
    path('fanlar/mudarris_talaba/kiritish/', AdminViews.fan_mudarris_talaba_kiritish, name='fan_mudarris_talaba_kiritish'),
    path('fanlar/mudarris_talaba/<int:id>/uchirish/', AdminViews.fan_mudarris_talaba_uchirish, name="fan_mudarris_talaba_uchirish"),
    # Kundalik baholar Ustoz - Talaba
    path('kundalik_baholar/ustoz_talaba/', AdminViews.kundalik_baholar_ustoz_talaba, name="kundalik_baholar_ustoz_talaba"),
    path('kundalik_baholar/ustoz_talaba/fan/<int:id>/', AdminViews.kundalik_baholar_ustoz_talaba_talaba_tanlash, name="kundalik_baholar_ustoz_talaba_talaba_tanlash"),
    path('kundalik_baholar/ustoz_talaba/fan/<int:fanId>/talaba/<int:talabaId>/', AdminViews.kundalik_baholar_ustoz_talaba_baholar, name="kundalik_baholar_ustoz_talaba_baholar"),
    path('kundalik_baholar/ustoz_talaba/fan/<int:fanId>/talaba/<int:talabaId>/api/', AdminViews.kundalik_baholar_ustoz_talaba_baholar_api, name="kundalik_baholar_ustoz_talaba_baholar_api"),
    path('kundalik_baholar/ustoz_talaba/fan/<int:fanId>/talaba/<int:talabaId>/kiritish/', AdminViews.kundalik_baholar_ustoz_talaba_baholar_kiritish, name="kundalik_baholar_ustoz_talaba_baholar_kiritish"),
    path('kundalik_baholar/ustoz_talaba/fan/<int:fanId>/talaba/<int:talabaId>/tahrirlash/', AdminViews.kundalik_baholar_ustoz_talaba_baholar_tahrirlash, name="kundalik_baholar_ustoz_talaba_baholar_tahrirlash"),
    path('kundalik_baholar/ustoz_talaba/fan/<int:fanId>/talaba/<int:talabaId>/tahrirlash/sana/', AdminViews.kundalik_baholar_ustoz_talaba_baholar_sana_tahrirlash, name="kundalik_baholar_ustoz_talaba_baholar_sana_tahrirlash"),
    path('kundalik_baholar/ustoz_talaba/fan/<int:fanId>/talaba/<int:talabaId>/uchirish/', AdminViews.kundalik_baholar_ustoz_talaba_baholar_uchirish, name="kundalik_baholar_ustoz_talaba_baholar_uchirish"),
    # Kundalik baholar Ustoz - Mudarris
    path('kundalik_baholar/ustoz_mudarris/', AdminViews.kundalik_baholar_ustoz_mudarris, name="kundalik_baholar_ustoz_mudarris"),
    path('kundalik_baholar/ustoz_mudarris/fan/<int:id>/', AdminViews.kundalik_baholar_ustoz_mudarris_mudarris_tanlash, name="kundalik_baholar_ustoz_mudarris_mudarris_tanlash"),
    path('kundalik_baholar/ustoz_mudarris/fan/<int:fanId>/mudarris/<int:mudarrisId>/', AdminViews.kundalik_baholar_ustoz_mudarris_baholar, name="kundalik_baholar_ustoz_mudarris_baholar"),
    path('kundalik_baholar/ustoz_mudarris/fan/<int:fanId>/mudarris/<int:mudarrisId>/api/', AdminViews.kundalik_baholar_ustoz_mudarris_baholar_api, name="kundalik_baholar_ustoz_mudarris_baholar_api"),
    path('kundalik_baholar/ustoz_mudarris/fan/<int:fanId>/mudarris/<int:mudarrisId>/kiritish/', AdminViews.kundalik_baholar_ustoz_mudarris_baholar_kiritish, name="kundalik_baholar_ustoz_mudarris_baholar_kiritish"),
    path('kundalik_baholar/ustoz_mudarris/fan/<int:fanId>/mudarris/<int:mudarrisId>/tahrirlash/', AdminViews.kundalik_baholar_ustoz_mudarris_baholar_tahrirlash, name="kundalik_baholar_ustoz_mudarris_baholar_tahrirlash"),
    path('kundalik_baholar/ustoz_mudarris/fan/<int:fanId>/mudarris/<int:mudarrisId>/tahrirlash/sana/', AdminViews.kundalik_baholar_ustoz_mudarris_baholar_sana_tahrirlash, name="kundalik_baholar_ustoz_mudarris_baholar_sana_tahrirlash"),
    path('kundalik_baholar/ustoz_mudarris/fan/<int:fanId>/mudarris/<int:mudarrisId>/uchirish/', AdminViews.kundalik_baholar_ustoz_mudarris_baholar_uchirish, name="kundalik_baholar_ustoz_mudarris_baholar_uchirish"),
    # Kundalik baholar Mudarris - Talaba
    path('kundalik_baholar/mudarris_talaba/', AdminViews.kundalik_baholar_mudarris_talaba, name="kundalik_baholar_mudarris_talaba"),
    path('kundalik_baholar/mudarris_talaba/fan/<int:id>/', AdminViews.kundalik_baholar_mudarris_talaba_talaba_tanlash, name="kundalik_baholar_mudarris_talaba_talaba_tanlash"),
    path('kundalik_baholar/mudarris_talaba/fan/<int:fanId>/talaba/<int:talabaId>/', AdminViews.kundalik_baholar_mudarris_talaba_baholar, name="kundalik_baholar_mudarris_talaba_baholar"),
    path('kundalik_baholar/mudarris_talaba/fan/<int:fanId>/talaba/<int:talabaId>/api/', AdminViews.kundalik_baholar_mudarris_talaba_baholar_api, name="kundalik_baholar_mudarris_talaba_baholar_api"),
    path('kundalik_baholar/mudarris_talaba/fan/<int:fanId>/talaba/<int:talabaId>/kiritish/', AdminViews.kundalik_baholar_mudarris_talaba_baholar_kiritish, name="kundalik_baholar_mudarris_talaba_baholar_kiritish"),
    path('kundalik_baholar/mudarris_talaba/fan/<int:fanId>/talaba/<int:talabaId>/tahrirlash/', AdminViews.kundalik_baholar_mudarris_talaba_baholar_tahrirlash, name="kundalik_baholar_mudarris_talaba_baholar_tahrirlash"),
    path('kundalik_baholar/mudarris_talaba/fan/<int:fanId>/talaba/<int:talabaId>/tahrirlash/sana/', AdminViews.kundalik_baholar_mudarris_talaba_baholar_sana_tahrirlash, name="kundalik_baholar_mudarris_talaba_baholar_sana_tahrirlash"),
    path('kundalik_baholar/mudarris_talaba/fan/<int:fanId>/talaba/<int:talabaId>/uchirish/', AdminViews.kundalik_baholar_mudarris_talaba_baholar_uchirish, name="kundalik_baholar_mudarris_talaba_baholar_uchirish"),
    # Imtihon baholar Ustoz - Talaba
    path('imtihon_baholar/ustoz_talaba/', AdminViews.imtihon_baholar_ustoz_talaba, name="imtihon_baholar_ustoz_talaba"),
    path('imtihon_baholar/ustoz_talaba/fan/<int:id>/', AdminViews.imtihon_baholar_ustoz_talaba_talaba_tanlash, name="imtihon_baholar_ustoz_talaba_talaba_tanlash"),
    path('imtihon_baholar/ustoz_talaba/fan/<int:fanId>/talaba/<int:talabaId>/', AdminViews.imtihon_baholar_ustoz_talaba_baholar, name="imtihon_baholar_ustoz_talaba_baholar"),
    path('imtihon_baholar/ustoz_talaba/fan/<int:fanId>/talaba/<int:talabaId>/api/', AdminViews.imtihon_baholar_ustoz_talaba_baholar_api, name="imtihon_baholar_ustoz_talaba_baholar_api"),
    path('imtihon_baholar/ustoz_talaba/fan/<int:fanId>/talaba/<int:talabaId>/kiritish/', AdminViews.imtihon_baholar_ustoz_talaba_baholar_kiritish, name="imtihon_baholar_ustoz_talaba_baholar_kiritish"),
    path('imtihon_baholar/ustoz_talaba/fan/<int:fanId>/talaba/<int:talabaId>/tahrirlash/sana/', AdminViews.imtihon_baholar_ustoz_talaba_baholar_sana_tahrirlash, name="imtihon_baholar_ustoz_talaba_baholar_sana_tahrirlash"),
    path('imtihon_baholar/ustoz_talaba/fan/<int:fanId>/talaba/<int:talabaId>/tahrirlash/', AdminViews.imtihon_baholar_ustoz_talaba_baholar_tahrirlash, name="imtihon_baholar_ustoz_talaba_baholar_tahrirlash"),
    path('imtihon_baholar/ustoz_talaba/fan/<int:fanId>/talaba/<int:talabaId>/uchirish/', AdminViews.imtihon_baholar_ustoz_talaba_baholar_uchirish, name="imtihon_baholar_ustoz_talaba_baholar_uchirish"),
    # Imtihon baholar Ustoz - Mudarris
    path('imtihon_baholar/ustoz_mudarris/', AdminViews.imtihon_baholar_ustoz_mudarris, name="imtihon_baholar_ustoz_mudarris"),
    # Imtihon baholar Mudarris - Talaba
    path('imtihon_baholar/mudarris_talaba/', AdminViews.imtihon_baholar_mudarris_talaba, name="imtihon_baholar_mudarris_talaba"),
    # -------------------------
    # Ustoz Urls
    path('ustoz_asosiy/', UstozViews.ustoz_asosiy, name="ustoz_asosiy"),
    # -------------------------
    # Mudarris Urls
    path('mudarris_asosiy/', MudarrisViews.mudarris_asosiy, name="mudarris_asosiy"),

]

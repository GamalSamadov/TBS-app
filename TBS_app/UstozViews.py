from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.files.storage import FileSystemStorage 
from django.urls import reverse
from .models import *
from .forms import *
from validate_email import validate_email 
from datetime import date, datetime
from datetime import timedelta
import pandas as pd
import json, os


def ustoz_asosiy(request):
    admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
    ustoz = Ustoz.objects.get(admin=request.user.id)
    hujralar = []
    mudarrislar = []
    talabalar = []
    fanlar = []
    for hujra in Hujra.objects.filter(ustoz=ustoz):
        hujralar.append(hujra)
        for mudarris in hujra.mudarris_set.all():
            mudarrislar.append(mudarris)
        for talaba in hujra.talaba_set.all():
            talabalar.append(talaba)
    for fan in FanUstozTalaba.objects.all():
        fanlar.append(fan)
    for fan in FanUstozMudarris.objects.all():
        fanlar.append(fan)
    context = {
        "admin" : admin,
        "hujralar_soni" : len(hujralar),
        "mudarrislar_soni" : len(mudarrislar),
        'talabalar_soni' : len(talabalar),
        'fanlar_soni' : len(fanlar)

        }
    return render(request, 'ustoz_templates/asosiy.html', context)


def ustoz_profil(request):
    admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
    ustoz = Ustoz.objects.get(admin=request.user.id)
    context = {
        'admin' : admin,
        'ustoz' : ustoz,
    }
    return render(request, 'ustoz_templates/ustoz_profil.html', context)


@require_http_methods(["GET", "POST"])
def ustoz_profil_tahrirlash(request):
    if request.method == 'GET':
        admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
        ustoz = Ustoz.objects.get(admin=request.user.id)
        context = {
            'admin':admin,
            'ustoz' : ustoz,
        }
        return render(request, 'ustoz_templates/ustoz_profil_tahrirlash.html', context)
    
    if request.method == 'POST':
        email =  request.POST.get('email')
        username = request.POST.get('username')
        parol = request.POST.get('parol')
        parolga_ishora = request.POST.get('parolga_ishora')
        ism = request.POST.get('ism')
        familya = request.POST.get('familya')

        ustoz = Ustoz.objects.get(admin=request.user.id)
        try:
            if len(request.FILES) != 0:
                profil_surati = request.FILES['profile_pic']
                fs = FileSystemStorage()
                if ustoz.profil_surati:
                    appDir = os.path.dirname(os.path.abspath(__file__))
                    directory = os.path.dirname(appDir)
                    fs.delete(directory + str(ustoz.profil_surati))
                filename = fs.save(profil_surati.name, profil_surati)
                profil_surati_url = fs.url(filename)
            else:
                profil_surati_url = None
                
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = ism
            customuser.last_name = familya
            if username != None and username != "":
                customuser.username = username
            if email != None and email != "":
                customuser.email = email
            if parol != None and parol != "":
                customuser.set_password(parol)
            
            ustoz.parolga_ishora = parolga_ishora
            if profil_surati_url != None:
                ustoz.profil_surati = profil_surati_url
            customuser.save()
            ustoz.save()
            messages.success(request, "Ustoz profil muvaffaqiyatli yangilandi")
            return redirect('ustoz_profil')
        except:
            messages.error(request, "Afsuski ustoz profil yangilanmadi")
            return redirect('ustoz_profil')


def ustoz_profil_suratni_uchirish(request):
    ustoz = Ustoz.objects.get(admin=request.user.id)
    try:
        fs = FileSystemStorage()
        if ustoz.profil_surati:
            appDir = os.path.dirname(os.path.abspath(__file__))
            directory = os.path.dirname(appDir)
            fs.delete(directory + str(ustoz.profil_surati))
        ustoz.profil_surati = None
        ustoz.save()    
        messages.success(request, "Ustoz profil surati muvaffaqiyatli o'chirildi")
        return redirect('ustoz_profil')
    except:
        messages.error(request, "Afsuski ustoz profil surati o'chirilmadi")
        return redirect('ustoz_profil')


# Hujralar
def hujralar(request):
    admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
    hujralar = Hujra.objects.select_related('ustoz').filter(ustoz__admin__id=request.user.id)
    context = {
        'admin' : admin,
        'hujralar' : hujralar,

    }
    return render(request, 'ustoz_templates/hujralar.html', context)


def hujra_profil(request, id):
    admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
    hujra = Hujra.objects.select_related('ustoz').get(id=id)
    mudarrislar = Mudarris.objects.select_related('hujra').filter(hujra=hujra)
    talabalar = Talaba.objects.select_related('hujra').filter(hujra=hujra)
    context = {
        'admin' : admin,
        'hujra' : hujra,
        'mudarrislar_soni' : mudarrislar.count(),
        'talabalar_soni' : talabalar.count(),

    }
    return render(request, 'ustoz_templates/hujra_profil.html', context)


def hujra_profil_mudarrislar(request, id):
    admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
    hujra = Hujra.objects.select_related('ustoz').get(id=id)
    mudarrislar = Mudarris.objects.select_related('hujra').filter(hujra=hujra)
    context = {
        'admin' : admin,
        'hujra' : hujra,
        'mudarrislar' : mudarrislar,

    }
    return render(request, 'ustoz_templates/hujra_profil_mudarrislar.html', context)


def hujra_profil_talabalar(request, id):
    admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
    hujra = Hujra.objects.select_related('ustoz').get(id=id)
    talabalar = Talaba.objects.select_related('hujra').filter(hujra=hujra)
    context = {
        'admin' : admin,
        'hujra' : hujra,
        'talabalar' : talabalar,

    }
    return render(request, 'ustoz_templates/hujra_profil_talabalar.html', context)


# Mudarrislar
def mudarrislar(request):
    admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
    ustoz = Ustoz.objects.get(admin=request.user.id)
    hujralar = Hujra.objects.filter(ustoz=ustoz)
    mudarrislar = []
    for hujra in hujralar:
        for mudarris in hujra.mudarris_set.all():
            mudarrislar.append(mudarris)
    context = {
        'admin' : admin,
        'mudarrislar' : mudarrislar
    }
    return render(request, 'ustoz_templates/mudarrislar.html', context)


def mudarris_profil(request, id):
    admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
    mudarris = Mudarris.objects.select_related('admin', 'hujra').get(admin=id)
    dars_beradigan_fanlar = FanMudarrisTalaba.objects.select_related('mudarris').prefetch_related('talaba').filter(mudarris=mudarris.id)
    uz_fanlar = mudarris.fanustozmudarris_set.all()
    talabalar = []
    for fan in dars_beradigan_fanlar:
        for talaba in fan.talaba.all():
            if talaba not in talabalar:
                talabalar.append(talaba)

    context = {
        'admin' : admin,
        'mudarris' : mudarris,
        'dars_beradigan_fanlar_soni' : dars_beradigan_fanlar.count(),
        'uz_fanlar_soni' : uz_fanlar.count(),
        'talabalar_soni' : len(talabalar),
    }
    return render(request, 'ustoz_templates/mudarris_profil.html', context)


def mudarris_profil_uz_fanlar(request, id):
    admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
    mudarris = Mudarris.objects.select_related('admin').get(admin=id)
    fanlar = mudarris.fanustozmudarris_set.all()
    context = {
        'admin' : admin,
        'mudarris' : mudarris,
        'fanlar' : fanlar
    }
    return render(request, 'ustoz_templates/mudarris_profil_uz_fanlar.html', context)


def mudarris_profil_fanlar(request, id):
    admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
    mudarris = Mudarris.objects.select_related('admin').get(admin=id)
    fanlar = FanMudarrisTalaba.objects.select_related('mudarris').prefetch_related('talaba').filter(mudarris=mudarris.id)
    context = {
        'admin' : admin,
        'mudarris' : mudarris,
        'fanlar' : fanlar
    }
    return render(request, 'ustoz_templates/mudarris_profil_fanlar.html', context)


def mudarris_profil_talabalar(request, id):
    admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
    mudarris = Mudarris.objects.select_related('admin').get(admin=id)
    fanlar = FanMudarrisTalaba.objects.select_related('mudarris').prefetch_related('talaba').filter(mudarris=mudarris.id)
    talabalar = []
    for fan in fanlar:
        for talaba in fan.talaba.all():
            if talaba not in talabalar:
                talabalar.append(talaba)
    context = {
        'admin' : admin,
        'mudarris' : mudarris,
        'talabalar' : talabalar,
    }
    return render(request, 'ustoz_templates/mudarris_profil_talabalar.html', context)


# talabalar
def talabalar(request):
    admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
    ustoz = Ustoz.objects.get(admin=request.user.id)
    hujralar = Hujra.objects.filter(ustoz=ustoz)
    talabalar = []
    for hujra in hujralar:
        for talaba in hujra.talaba_set.all():
            talabalar.append(talaba)
    context = {
        'admin' : admin,
        'talabalar' : talabalar
    }
    return render(request, 'ustoz_templates/talabalar.html', context)


def talaba_profil(request, id):
    admin = CustomUser.objects.select_related('ustoz').get(id=request.user.id)
    talaba = Talaba.objects.select_related('hujra').get(id=id)
    ustoz_fan = talaba.fanustoztalaba_set.all()
    mudarris_fan = talaba.fanmudarristalaba_set.all()
    hamma_fanlar = []
    for fan in ustoz_fan:
        hamma_fanlar.append(fan)
    for fan in mudarris_fan:
        hamma_fanlar.append(fan)    
    context = {
        'admin' : admin,
        'talaba' : talaba,
        'fanlar_soni' : len(hamma_fanlar),
    }
    return render(request, 'ustoz_templates/talaba_profil.html', context)


def talaba_profil_fanlar(request, id):
    admin = CustomUser.objects.select_related('ustoz').get(id=request.user.id)
    talaba = Talaba.objects.select_related('hujra').get(id=id)
    ustoz_fan = talaba.fanustoztalaba_set.all()
    mudarris_fan = talaba.fanmudarristalaba_set.all()
    hamma_fanlar = []
    for fan in ustoz_fan:
        hamma_fanlar.append(fan)
    for fan in mudarris_fan:
        hamma_fanlar.append(fan)    
    context = {
        'admin' : admin,
        'talaba' : talaba,
        'fanlar' : hamma_fanlar,
        'ustoz_fan' : ustoz_fan,
        'mudarris_fan' : mudarris_fan,
    }
    return render(request, 'ustoz_templates/talaba_profil_fanlar.html', context)


# Fan talaba
def fanlar_talaba(request):
    admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
    ustoz = Ustoz.objects.get(admin=request.user.id)
    fanlar = FanUstozTalaba.objects.select_related('ustoz').prefetch_related('talaba').filter(ustoz=ustoz)
    context = {
        'admin' : admin,
        'fanlar' : fanlar
    }
    return render(request, 'ustoz_templates/fanlar_ustoz_talaba.html', context)


def fan_talaba_profil(request, id):
    admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
    fan = FanUstozTalaba.objects.select_related('ustoz').prefetch_related('talaba').get(id=id)
    talabalar_soni = fan.talaba.count()
    context = {
        'admin' : admin,
        'fan' : fan,
        'talabalar_soni' : talabalar_soni
    }
    return render(request, 'ustoz_templates/fan_ustoz_talaba_profil.html', context)


def fan_talaba_profil_talabalar(request, id):
    admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
    fan = FanUstozTalaba.objects.select_related('ustoz').prefetch_related('talaba').get(id=id)
    talabalar = fan.talaba.all()
    context = {
        'admin' : admin,
        'fan' : fan,
        'talabalar' : talabalar
    }
    return render(request, 'ustoz_templates/fan_ustoz_talaba_profil_talabalar.html', context)


# Fan Mudarris
def fanlar_mudarris(request):
    admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
    ustoz = Ustoz.objects.get(admin=request.user.id)
    fanlar = FanUstozMudarris.objects.select_related('ustoz').filter(ustoz=ustoz)
    context = {
        'admin' : admin,
        'fanlar' : fanlar
    }
    return render(request, 'ustoz_templates/fanlar_ustoz_mudarris.html', context)


def fan_mudarris_profil(request, id):
    admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
    fan = FanUstozMudarris.objects.select_related('ustoz').prefetch_related('mudarris').get(id=id)
    mudarrislar_soni = fan.mudarris.count()
    context = {
        'admin' : admin,
        'fan' : fan,
        'mudarrislar_soni' : mudarrislar_soni
    }
    return render(request, 'ustoz_templates/fan_ustoz_mudarris_profil.html', context)


def fan_mudarris_profil_mudarrislar(request, id):
    admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
    fan = FanUstozMudarris.objects.select_related('ustoz').prefetch_related('mudarris').get(id=id)
    mudarrislar = fan.mudarris.all()
    context = {
        'admin' : admin,
        'fan' : fan,
        'mudarrislar' : mudarrislar
    }
    return render(request, 'ustoz_templates/fan_ustoz_mudarris_profil_mudarrislar.html', context)


# Baho Talaba
def baho_talaba(request):
    admin = CustomUser.objects.get(id=request.user.id)
    ustoz = Ustoz.objects.get(admin=request.user.id)
    fanlar = FanUstozTalaba.objects.select_related('ustoz').prefetch_related('talaba').filter(ustoz=ustoz)
    context = {
        'admin' : admin,
        'fanlar' : fanlar,
    }
    return render(request, 'ustoz_templates/kundalik_baholar_ustoz_talaba.html', context)


def baho_talaba_tanlash(request, id):
    admin = CustomUser.objects.get(id=request.user.id)
    fan = FanUstozTalaba.objects.select_related('ustoz').prefetch_related('talaba').get(id=id)
    talabalar = fan.talaba.all()
    context = {
        'admin' : admin,
        'talabalar' : talabalar,
        'fan' : fan,
    }
    return render(request, 'ustoz_templates/kundalik_baholar_ustoz_talaba_talaba_tanlash.html', context)


def baholar_talaba(request, fanId, talabaId):
    admin = CustomUser.objects.get(id=request.user.id)
    fan = FanUstozTalaba.objects.get(id=fanId)
    talaba = Talaba.objects.get(id=talabaId)
    baholar = KundalikBahoUstozTalaba.objects.filter(fan__id=fanId).filter(talaba__id=talabaId)
    context = {
        'admin' : admin,
        'baholar' : baholar,
        'fan' : fan,
        'talaba' : talaba
    }
    return render(request, 'ustoz_templates/kundalik_baholar_ustoz_talaba_baholar.html', context)


def baholar_talaba_api(request, fanId, talabaId):
    baholar = KundalikBahoUstozTalaba.objects.filter(fan__id=fanId).filter(talaba__id=talabaId)
    out = []
    for baho in baholar:
        out.append({
            'title' : baho.baho,
            'id' : baho.id,
            'start' : baho.sana.strftime("%Y-%m-%d"),
            'izoh' : baho.izoh,
            
            
        })
    return JsonResponse(out, safe=False)


def baholar_talaba_kiritish(request, fanId, talabaId):
    start = request.GET.get('start', None)
    title = request.GET.get('title', None)
    izoh = request.GET.get('izoh', None)
    fan = FanUstozTalaba.objects.get(id=fanId)
    talaba = Talaba.objects.get(id=talabaId)
    baho = KundalikBahoUstozTalaba(baho=int(title), fan=fan, talaba=talaba, sana=start, izoh=izoh)
    baho.save()
    data = {}
    return JsonResponse(data)


def baholar_talaba_sana_tahrirlash(request, fanId, talabaId):
    start = request.GET.get('start', None)
    id = request.GET.get('id', None)
    baho = KundalikBahoUstozTalaba.objects.get(id=id)
    baho.sana = start
    baho.save()
    data = {}
    return JsonResponse(data)


def baholar_talaba_tahrirlash(request, fanId, talabaId):
    title = request.GET.get('title', None)
    izoh = request.GET.get('izoh', None)
    id = request.GET.get('id', None)
    baho = KundalikBahoUstozTalaba.objects.get(id=id)
    baho.baho = title
    baho.izoh = izoh
    baho.save()
    data = {}
    return JsonResponse(data)


def baholar_talaba_uchirish(request, fanId, talabaId):
    id = request.GET.get('id', None)
    baho = KundalikBahoUstozTalaba.objects.get(id=id)
    baho.delete()
    data = {}
    return JsonResponse(data)


# Baho - Mudarris
def baho_mudarris(request):
    admin = CustomUser.objects.get(id=request.user.id)
    ustoz = Ustoz.objects.get(admin=request.user.id)
    fanlar = FanUstozMudarris.objects.select_related('ustoz').prefetch_related('mudarris').filter(ustoz=ustoz)
    context = {
        'admin' : admin,
        'fanlar' : fanlar,
    }
    return render(request, 'ustoz_templates/kundalik_baholar_ustoz_mudarris.html', context)


def baho_mudarris_tanlash(request, id):
    fan = FanUstozMudarris.objects.select_related('ustoz').prefetch_related('mudarris').get(id=id)
    mudarrislar = fan.mudarris.all()
    context = {
        'mudarrislar' : mudarrislar,
        'fan' : fan
    }
    return render(request, 'ustoz_templates/kundalik_baholar_ustoz_mudarris_mudarris_tanlash.html', context)


def baholar_mudarris(request, fanId, mudarrisId):
    admin = CustomUser.objects.get(id=request.user.id)
    fan = FanUstozMudarris.objects.get(id=fanId)
    mudarris = Mudarris.objects.get(id=mudarrisId)
    baholar = KundalikBahoUstozMudarris.objects.filter(fan__id=fanId).filter(mudarris__id=mudarrisId)
    context = {
        'admin' : admin,
        'baholar' : baholar,
        'fan' : fan,
        'mudarris' : mudarris
    }
    return render(request, 'ustoz_templates/kundalik_baholar_ustoz_mudarris_baholar.html', context)


def baholar_mudarris_api(request, fanId, mudarrisId):
    baholar = KundalikBahoUstozMudarris.objects.filter(fan__id=fanId).filter(mudarris__id=mudarrisId)
    out = []
    for baho in baholar:
        out.append({
            'title' : baho.baho,
            'id' : baho.id,
            'start' : baho.sana.strftime("%Y-%m-%d"),
            'izoh':baho.izoh,
        })
    return JsonResponse(out, safe=False)


def baholar_mudarris_kiritish(request, fanId, mudarrisId):
    start = request.GET.get('start', None)
    title = request.GET.get('title', None)
    fan = FanUstozMudarris.objects.filter(id=fanId).get(mudarris__id=mudarrisId)
    mudarris = Mudarris.objects.get(id=mudarrisId)
    baho = KundalikBahoUstozMudarris(baho=int(title), fan=fan, mudarris=mudarris, sana=start)
    baho.save()
    data = {}
    return JsonResponse(data)


def baholar_mudarris_sana_tahrirlash(request, fanId, mudarrisId):
    start = request.GET.get('start', None)
    id = request.GET.get('id', None)
    baho = KundalikBahoUstozMudarris.objects.get(id=id)
    baho.sana = start
    baho.save()
    data = {}
    return JsonResponse(data)


def baholar_mudarris_tahrirlash(request, fanId, mudarrisId):
    title = request.GET.get('title', None)
    izoh = request.GET.get('izoh', None)
    id = request.GET.get('id', None)
    baho = KundalikBahoUstozMudarris.objects.get(id=id)
    baho.baho = title
    baho.izoh = izoh
    baho.save()
    data = {}
    return JsonResponse(data)


def baholar_mudarris_uchirish(request, fanId, mudarrisId):
    id = request.GET.get('id', None)
    baho = KundalikBahoUstozMudarris.objects.get(id=id)
    baho.delete()
    data = {}
    return JsonResponse(data)


# Username ni tekshirish
class UsernameTekshirish(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error' : 'Nomi faqat harf va raqamdan iborat bo\'lishi kerak!'}, status=400)
        if CustomUser.objects.filter(username=username).exists():
            return JsonResponse({'username_error' : 'Bunday nom bazada mavjud. Boshqa nom yozing...'}, status=400)
        else:
            return JsonResponse({'username_valid' : True})


# Emailni tekshirish
class EmailTekshirish(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error' : 'Email to\'g\'ri emas!'}, status=400)
        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({'email_error' : 'Bunday email mavjud. Boshqa email yozing...'}, status=400)
        return JsonResponse({'email_valid' : True})



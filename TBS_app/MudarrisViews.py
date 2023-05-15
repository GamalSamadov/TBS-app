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


def mudarris_asosiy(request):
    admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
    mudarris = Mudarris.objects.get(admin=request.user.id)
    fanlar = []
    talabalar = []
    for fan in FanMudarrisTalaba.objects.filter(mudarris=mudarris):
        if fan not in fanlar:
            fanlar.append(fan)
        for talaba in fan.talaba.all():
            if talaba not in talabalar:
                talabalar.append(talaba)

    context = {
        'admin' : admin,
        'fanlar_soni' : len(fanlar),
        'talabalar_soni' : len(talabalar),
    }
    return render(request, 'mudarris_templates/asosiy.html', context)


def mudarris_profil(request):
    admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
    mudarris = Mudarris.objects.get(admin=request.user.id)
    context = {
        'admin' : admin,
        'mudarris' : mudarris,
    }
    return render(request, 'mudarris_templates/mudarris_profil.html', context)


@require_http_methods(["GET", "POST"])
def mudarris_profil_tahrirlash(request):
    if request.method == 'GET':
        admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
        mudarris = Mudarris.objects.get(admin=request.user.id)
        context = {
            'admin':admin,
            'mudarris' : mudarris,
        }
        return render(request, 'mudarris_templates/mudarris_profil_tahrirlash.html', context)
    
    if request.method == 'POST':
        email =  request.POST.get('email')
        username = request.POST.get('username')
        parol = request.POST.get('parol')
        parolga_ishora = request.POST.get('parolga_ishora')
        ism = request.POST.get('ism')
        familya = request.POST.get('familya')

        mudarris = Mudarris.objects.get(admin=request.user.id)
        try:
            if len(request.FILES) != 0:
                profil_surati = request.FILES['profile_pic']
                fs = FileSystemStorage()
                if mudarris.profil_surati:
                    appDir = os.path.dirname(os.path.abspath(__file__))
                    directory = os.path.dirname(appDir)
                    fs.delete(directory + str(mudarris.profil_surati))
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
            
            mudarris.parolga_ishora = parolga_ishora
            if profil_surati_url != None:
                mudarris.profil_surati = profil_surati_url
            customuser.save()
            mudarris.save()
            messages.success(request, "Mudarris profil muvaffaqiyatli yangilandi")
            return redirect('mudarris_profil')
        except:
            messages.error(request, "Afsuski mudarris profil yangilanmadi")
            return redirect('mudarris_profil')


def mudarris_profil_suratni_uchirish(request):
    mudarris = Mudarris.objects.get(admin=request.user.id)
    try:
        fs = FileSystemStorage()
        if mudarris.profil_surati:
            appDir = os.path.dirname(os.path.abspath(__file__))
            directory = os.path.dirname(appDir)
            fs.delete(directory + str(mudarris.profil_surati))
        mudarris.profil_surati = None
        mudarris.save()    
        messages.success(request, "Mudarris profil surati muvaffaqiyatli o'chirildi")
        return redirect('mudarris_profil')
    except:
        messages.error(request, "Afsuski mudarris profil surati o'chirilmadi")
        return redirect('mudarris_profil')


# talabalar
def talabalar(request):
    admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
    mudarris = Mudarris.objects.get(admin=request.user.id)
    fanlar = FanMudarrisTalaba.objects.filter(mudarris=mudarris)
    talabalar = []
    for fan in fanlar:
        for talaba in fan.talaba.all():
            if talaba not in talabalar:
                talabalar.append(talaba)
    context = {
        'admin' : admin,
        'talabalar' : talabalar
    }
    return render(request, 'mudarris_templates/talabalar.html', context)


def talaba_profil(request, id):
    admin = CustomUser.objects.select_related('ustoz').get(id=request.user.id)
    mudarris = Mudarris.objects.get(admin=request.user.id)
    talaba = Talaba.objects.get(id=id)
    fanlar = talaba.fanmudarristalaba_set.filter(mudarris=mudarris)
    context = {
        'admin' : admin,
        'fanlar_soni' : fanlar.count(),
    }
    return render(request, 'mudarris_templates/talaba_profil.html', context)


def talaba_profil_fanlar(request, id):
    admin = CustomUser.objects.select_related('ustoz').get(id=request.user.id)
    talaba = Talaba.objects.select_related('hujra').get(id=id)
    talaba = Talaba.objects.get(id=id)
    fanlar = talaba.fanmudarristalaba_set.filter(mudarris=mudarris)
    context = {
        'admin' : admin,
        'talaba' : talaba,
        'fanlar' : fanlar,
    }
    return render(request, 'mudarris_templates/talaba_profil_fanlar.html', context)


# Fan talaba
def fanlar_talaba(request):
    admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
    mudarris = Mudarris.objects.get(admin=request.user.id)
    fanlar = FanMudarrisTalaba.objects.select_related('mudarris').prefetch_related('talaba').filter(mudarris=mudarris)
    context = {
        'admin' : admin,
        'fanlar' : fanlar
    }
    return render(request, 'mudarris_templates/fanlar_mudarris_talaba.html', context)


def fan_talaba_profil(request, id):
    admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
    fan = FanMudarrisTalaba.objects.select_related('mudarris').prefetch_related('talaba').get(id=id)
    talabalar_soni = fan.talaba.count()
    context = {
        'admin' : admin,
        'fan' : fan,
        'talabalar_soni' : talabalar_soni
    }
    return render(request, 'mudarris_templates/fan_mudarris_talaba_profil.html', context)


def fan_talaba_profil_talabalar(request, id):
    admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
    fan = FanMudarrisTalaba.objects.select_related('mudarris').prefetch_related('talaba').get(id=id)
    talabalar = fan.talaba.all()
    context = {
        'admin' : admin,
        'fan' : fan,
        'talabalar' : talabalar
    }
    return render(request, 'mudarris_templates/fan_mudarris_talaba_profil_talabalar.html', context)


# Baho Talaba
def baho_talaba(request):
    admin = CustomUser.objects.get(id=request.user.id)
    mudarris = Mudarris.objects.get(admin=request.user.id)
    fanlar = FanMudarrisTalaba.objects.select_related('mudarris').prefetch_related('talaba').filter(mudarris=mudarris)
    context = {
        'admin' : admin,
        'fanlar' : fanlar,
    }
    return render(request, 'mudarris_templates/kundalik_baholar_mudarris_talaba.html', context)


def baho_talaba_tanlash(request, id):
    admin = CustomUser.objects.get(id=request.user.id)
    fan = FanMudarrisTalaba.objects.select_related('mudarris').prefetch_related('talaba').get(id=id)
    talabalar = fan.talaba.all()
    context = {
        'admin' : admin,
        'talabalar' : talabalar,
        'fan' : fan,
    }
    return render(request, 'mudarris_templates/kundalik_baholar_mudarris_talaba_talaba_tanlash.html', context)


def baholar_talaba(request, fanId, talabaId):
    admin = CustomUser.objects.get(id=request.user.id)
    fan = FanMudarrisTalaba.objects.get(id=fanId)
    talaba = Talaba.objects.get(id=talabaId)
    baholar = KundalikBahoMudarrisTalaba.objects.filter(fan__id=fanId).filter(talaba__id=talabaId)
    context = {
        'admin' : admin,
        'baholar' : baholar,
        'fan' : fan,
        'talaba' : talaba
    }
    return render(request, 'mudarris_templates/kundalik_baholar_mudarris_talaba_baholar.html', context)


def baholar_talaba_api(request, fanId, talabaId):
    baholar = KundalikBahoMudarrisTalaba.objects.filter(fan__id=fanId).filter(talaba__id=talabaId)
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
    fan = FanMudarrisTalaba.objects.get(id=fanId)
    talaba = Talaba.objects.get(id=talabaId)
    baho = KundalikBahoMudarrisTalaba(baho=int(title), fan=fan, talaba=talaba, sana=start, izoh=izoh)
    baho.save()
    data = {}
    return JsonResponse(data)


def baholar_talaba_sana_tahrirlash(request, fanId, talabaId):
    start = request.GET.get('start', None)
    id = request.GET.get('id', None)
    baho = KundalikBahoMudarrisTalaba.objects.get(id=id)
    baho.sana = start
    baho.save()
    data = {}
    return JsonResponse(data)


def baholar_talaba_tahrirlash(request, fanId, talabaId):
    title = request.GET.get('title', None)
    izoh = request.GET.get('izoh', None)
    id = request.GET.get('id', None)
    baho = KundalikBahoMudarrisTalaba.objects.get(id=id)
    baho.baho = title
    baho.izoh = izoh
    baho.save()
    data = {}
    return JsonResponse(data)


def baholar_talaba_uchirish(request, fanId, talabaId):
    id = request.GET.get('id', None)
    baho = KundalikBahoMudarrisTalaba.objects.get(id=id)
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



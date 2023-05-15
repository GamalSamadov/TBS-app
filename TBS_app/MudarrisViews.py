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
    return render(request, 'mudarris_templates/asosiy.html')


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
    mudarris = Ustoz.objects.get(admin=request.user.id)
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



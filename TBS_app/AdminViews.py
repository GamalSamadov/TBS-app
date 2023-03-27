from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.files.storage import FileSystemStorage 
from django.urls import reverse
from validate_email import validate_email # To upload Profile Picture
import json

from .models import *
from .forms import *


def admin_asosiy(request):
    user = CustomUser.objects.get(id=request.user.id)
    admin = Admin.objects.get(admin=request.user.id)
    context = {
        'user' : user,
        'admin' : admin,
    }
    return render(request, 'admin_templates/asosiy.html', context)


def admin_profil(request):
    user = CustomUser.objects.get(id=request.user.id)
    admin = Admin.objects.get(admin=request.user.id)
    context = {
        'user' : user,
        'admin' : admin,
    }
    return render(request, 'admin_templates/admin_profil.html', context)


@require_http_methods(["GET", "POST"])
def admin_profil_tahrirlash(request):
    if request.method == 'GET':
        user = CustomUser.objects.get(id=request.user.id)
        admin = Admin.objects.get(admin=request.user.id)
        form = AdminProfileForm()
        form.fields['username'].initial = user.username
        form.fields['email'].initial = user.email
        form.fields['first_name'].initial = user.first_name
        form.fields['last_name'].initial = user.last_name
        form.fields['password_hint'].initial = admin.password_hint
        context = {
            "user": user,
            'form': form,
            'admin':admin,
        }
        return render(request, 'admin_templates/admin_profil_tahrirlash.html', context)
    
    if request.method == 'POST':
        form = AdminProfileForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            password_hint = form.cleaned_data['password_hint']

            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None
            try:
                customuser = CustomUser.objects.get(id=request.user.id)
                admin = Admin.objects.get(admin=request.user.id)
                customuser.first_name = first_name
                customuser.last_name = last_name
                if admin.password_hint != None:
                    admin.password_hint = password_hint
                admin.password_hint = password_hint
                if password != None and password != "":
                    customuser.set_password(password)
                if profile_pic_url != None:
                    admin.profile_pic = profile_pic_url
                customuser.save()
                admin.save()
                messages.success(request, "Admin profil muvaffaqiyatli yangilandi")
                return redirect('admin_profil')
            except:
                messages.error(request, "Afsuski admin profil yangilanmadi")
                return redirect('admin_profil')
        else:
            return redirect('admin_profil')


def admin_profil_suratni_uchirish(request):
    admin = Admin.objects.get(admin=request.user.id)
    try:
        admin.profile_pic = None
        admin.save()    
        messages.success(request, "Admin profil surati muvaffaqiyatli o'chirildi")
        return redirect('admin_profil')
    except:
        messages.error(request, "Afsuski admin profil surati o'chirilmadi")
        return redirect('admin_profil')


def ustozlar(request):
    user = CustomUser.objects.get(id=request.user.id)
    admin = Admin.objects.get(admin=request.user.id)
    ustozlar = Ustoz.objects.all()
    context = {
        'user' : user,
        'admin' : admin,
        'ustozlar' : ustozlar
    }
    return render(request, 'admin_templates/ustozlar.html', context)


@require_http_methods(["GET", "POST"])
def ustoz_kiritish(request):
    if request.method == 'GET':
        user = CustomUser.objects.get(id=request.user.id)
        admin = Admin.objects.get(admin=request.user.id)
        form = UstozKiritishForm()
        context = {
            'user' : user,
            'admin' : admin,
            'form' : form
        }
        return render(request, 'admin_templates/ustoz_kiritish.html', context)
    if request.method == 'POST':
        email =  request.POST.get('email')
        username = request.POST.get('username')
        parol = request.POST.get('parol')
        parolga_ishora = request.POST.get('parolga_ishora')
        ism = request.POST.get('ism')
        familya = request.POST.get('familya')
        adres = request.POST.get('adres')
        jins = request.POST.get('jins')

        if len(request.FILES) != 0:
            profil_surati = request.FILES['profil_surati']
            fs = FileSystemStorage()
            filename = fs.save(profil_surati.name, profil_surati)
            profil_surati_url = fs.url(filename)
        else:
            profil_surati_url = None

        try:
            user = CustomUser.objects.create_user(username=username, password=parol, email=email, first_name=ism, last_name=familya, user_type=2)
            user.ustoz.parolga_ishora = parolga_ishora
            user.ustoz.adres = adres
            user.ustoz.jins = jins
            user.ustoz.profil_surati = profil_surati_url
            user.save()
            messages.success(
                request, "Ustoz kiritish muvaffaqiyatli amalga oshirildi :)")
            return redirect('ustozlar')
        except:
            messages.error(
                request, "Ustoz kiritish ba'zi muommolar uchun amalga oshirilmadi :(")
            return redirect('ustozlar')


def ustoz_profil(request, id):
    user = CustomUser.objects.get(id=request.user.id)
    admin = Admin.objects.get(admin=request.user.id)
    ustoz = Ustoz.objects.get(admin=id)
    context = {
        'user' : user,
        'admin' : admin,
        'ustoz' : ustoz,

    }
    return render(request, 'admin_templates/ustoz_profil.html', context)


@require_http_methods(["GET", "POST"])
def ustoz_profil_tahrirlash(request, id):
    if request.method == 'GET':
        user = CustomUser.objects.get(id=request.user.id)
        admin = Admin.objects.get(admin=request.user.id)
        ustoz = Ustoz.objects.get(admin=id)
        context = {
            'user' : user,
            'admin' : admin,
            'ustoz' : ustoz
        }
        return render(request, 'admin_templates/ustoz_profil_tahrirlash.html', context)
    else:
        email = request.POST.get('email')
        username = request.POST.get('username')
        ism = request.POST.get('ism')
        familya = request.POST.get('familya')
        parol = request.POST.get('parol')
        parolga_ishora = request.POST.get('parolga_ishora')
        adres = request.POST.get('adres')
        jins = request.POST.get('jins')

        if len(request.FILES) != 0:
            profil_surati = request.FILES['profil_surati']
            fs = FileSystemStorage()
            filename = fs.save(profil_surati.name, profil_surati)
            profil_surati_url = fs.url(filename)
        else:
            profil_surati_url = None
        
        try:
            ustoz = Ustoz.objects.get(admin=id)

            ustoz.admin.first_name = ism
            ustoz.admin.last_name = familya
            ustoz.admin.email = email
            ustoz.admin.username = username
            if parol != None and parol != "":
                ustoz.admin.password = parol
            if profil_surati_url != None:
                ustoz.profil_surati = profil_surati_url
            ustoz.parolga_ishora = parolga_ishora
            ustoz.adres = adres
            ustoz.jins = jins

            ustoz.save()

            messages.success(request, "Ustoz profil muvaffaqiyatli yangilandi")
            return HttpResponseRedirect(reverse('ustoz_profil', kwargs={'id': id}))
        except:
            messages.error(request, "Ustoz profilni yangilashda xato ro'y berdi :(")
            return HttpResponseRedirect(reverse('ustoz_profil', kwargs={'id': id}))

        
def ustoz_profil_suratni_uchirish(request, id):
    ustoz = Ustoz.objects.get(admin=id)
    try:
        ustoz.profil_surati = None
        ustoz.save()    
        messages.success(request, "Ustoz profil surati muvaffaqiyatli o'chirildi")
        return HttpResponseRedirect(reverse('ustoz_profil', kwargs={'id': id}))
    except:
        messages.error(request, "Afsuski ustoz profil surati o'chirilmadi")
        return HttpResponseRedirect(reverse('ustoz_profil', kwargs={'id': id}))


def ustozni_uchirish(request, id):
    user = CustomUser.objects.get(id=id)
    try:
        user.delete()
        messages.success(request, "Ustoz o\'chirildi.")
        return redirect('ustozlar')
    except:
        messages.error(request, "Ustozni ba'zi sabablarga ko'ra o'chirib bo'lmadi.")
        return redirect('ustozlar')


def hujralar(request):
    user = CustomUser.objects.get(id=request.user.id)
    admin = Admin.objects.get(admin=request.user.id)
    context = {
        'user' : user,
        'admin' : admin,
    }
    return render(request, 'admin_templates/hujralar.html', context)


def kurslar(request):
    user = CustomUser.objects.get(id=request.user.id)
    admin = Admin.objects.get(admin=request.user.id)
    context = {
        'user' : user,
        'admin' : admin,
    }
    return render(request, 'admin_templates/kurslar.html', context)


def ustozlar_kurs_profil(request, id):
    ustoz = Ustoz.objects.filter()
    user = CustomUser.objects.filter()
    admin = Admin.objects.get(admin=request.user.id)
    kurs = Kurs.objects.get(id=id)
    context = {
        'user' : user,
        'admin' : admin,
        'kurs' : kurs,
    }
    return render(request, 'admin_templates/ustoz_kurs_profil.html', context)


class UsernameTekshirish(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error' : 'Nomi faqat harf va raqamdan iborat bo\'lishi kerak!'}, status=400)
        if CustomUser.objects.filter(username=username).exists() and str(CustomUser.objects.filter(username=username).username) != str(username):
            return JsonResponse({'username_error' : 'Bunday nom bazada mavjud. Boshqa nom yozing...'}, status=400)
        return JsonResponse({'username_valid' : True})


class EmailTekshirish(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error' : 'Email to\'g\'ri emas!'}, status=400)
        if CustomUser.objects.filter(email=email).exists() and str(CustomUser.objects.filter(email=email).email) != str(email):
            return JsonResponse({'email_error' : 'Email mavjud. Boshqa email yozing...'}, status=400)
        return JsonResponse({'email_valid' : True})



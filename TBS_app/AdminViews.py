from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.files.storage import FileSystemStorage 
from django.urls import reverse
from validate_email import validate_email # To upload Profile Picture
import json
import os
from .models import *
from .forms import *


# Asosiy
def admin_asosiy(request):
    admin = CustomUser.objects.get(id=request.user.id)
    context = {
        'admin' : admin,
    }
    return render(request, 'admin_templates/asosiy.html', context)


# Admin
def admin_profil(request):
    admin = CustomUser.objects.get(id=request.user.id)
    context = {
        'admin' : admin,
    }
    return render(request, 'admin_templates/admin_profil.html', context)


@require_http_methods(["GET", "POST"])
def admin_profil_tahrirlash(request):
    if request.method == 'GET':
        admin = CustomUser.objects.get(id=request.user.id)
        context = {
            'admin':admin,
        }
        return render(request, 'admin_templates/admin_profil_tahrirlash.html', context)
    
    if request.method == 'POST':
        email =  request.POST.get('email')
        username = request.POST.get('username')
        parol = request.POST.get('parol')
        parolga_ishora = request.POST.get('parolga_ishora')
        ism = request.POST.get('ism')
        familya = request.POST.get('familya')

        try:
            admin = Admin.objects.get(admin=request.user.id)
            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                if admin.profile_pic:
                    appDir = os.path.dirname(os.path.abspath(__file__))
                    directory = os.path.dirname(appDir)
                    fs.delete(directory + str(admin.profile_pic))
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None
                
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = ism
            customuser.last_name = familya
            if username != None and username != "":
                customuser.username = username
            if email != None and email != "":
                customuser.email = email
            if parol != None and parol != "":
                customuser.set_password(parol)
            
            admin.password_hint = parolga_ishora
            if profile_pic_url != None:
                admin.profile_pic = profile_pic_url
            customuser.save()
            admin.save()
            messages.success(request, "Admin profil muvaffaqiyatli yangilandi")
            return redirect('admin_profil')
        except:
            messages.error(request, "Afsuski admin profil yangilanmadi")
            return redirect('admin_profil')   


def admin_profil_suratni_uchirish(request):
    admin = Admin.objects.get(admin=request.user.id)
    try:
        fs = FileSystemStorage()
        if admin.profile_pic:
            appDir = os.path.dirname(os.path.abspath(__file__))
            directory = os.path.dirname(appDir)
            fs.delete(directory + str(admin.profile_pic))
        admin.profile_pic = None
        admin.save()    
        messages.success(request, "Admin profil surati muvaffaqiyatli o'chirildi")
        return redirect('admin_profil')
    except:
        messages.error(request, "Afsuski admin profil surati o'chirilmadi")
        return redirect('admin_profil')


# Ustozlar
def ustozlar(request):
    admin = CustomUser.objects.get(id=request.user.id)
    ustozlar = Ustoz.objects.all()
    context = {
        'admin' : admin,
        'ustozlar' : ustozlar
    }
    return render(request, 'admin_templates/ustozlar.html', context)


@require_http_methods(["GET", "POST"])
def ustoz_kiritish(request):
    if request.method == 'GET':
        admin = CustomUser.objects.get(id=request.user.id)
        form = UstozKiritishForm()
        context = {
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
    admin = CustomUser.objects.get(id=request.user.id)
    ustoz = Ustoz.objects.get(admin=id)
    context = {
        'admin' : admin,
        'ustoz' : ustoz,

    }
    return render(request, 'admin_templates/ustoz_profil.html', context)


@require_http_methods(["GET", "POST"])
def ustoz_profil_tahrirlash(request, id):
    if request.method == 'GET':
        admin = CustomUser.objects.get(id=request.user.id)
        ustoz = Ustoz.objects.get(admin=id)
        context = {
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
        
        try:
            ustoz = Ustoz.objects.get(admin=id)

            ustoz.admin.first_name = ism
            ustoz.admin.last_name = familya
            ustoz.admin.email = email
            ustoz.admin.username = username

            if parol != None and parol != "":
                ustoz.admin.password = parol

            if len(request.FILES) != 0:
                profil_surati = request.FILES['profil_surati']
                fs = FileSystemStorage()
                if ustoz.profil_surati:
                    appDir = os.path.dirname(os.path.abspath(__file__))
                    directory = os.path.dirname(appDir)
                    fs.delete(directory + str(ustoz.profil_surati))
                filename = fs.save(profil_surati.name, profil_surati)
                profil_surati_url = fs.url(filename)
            else:
                profil_surati_url = None

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
        if ustoz.profil_surati:
            fs = FileSystemStorage()
            appDir = os.path.dirname(os.path.abspath(__file__))
            directory = os.path.dirname(appDir)
            fs.delete(directory + str(ustoz.profil_surati))
            ustoz.profil_surati = None
            ustoz.save()    
            messages.success(request, "Ustoz profil surati muvaffaqiyatli o'chirildi")
            return HttpResponseRedirect(reverse('ustoz_profil', kwargs={'id': id}))
        else:
            messages.error(request, "Uztozning surati yo'q. Avval ustozga surat kiriting...")
            return HttpResponseRedirect(reverse('ustoz_profil', kwargs={'id': id}))
    except:
        messages.error(request, "Afsuski ustoz profil surati o'chirilmadi")
        return HttpResponseRedirect(reverse('ustoz_profil', kwargs={'id': id}))


def ustozni_uchirish(request, id):
    user = CustomUser.objects.get(id=id)
    try:
        if user.ustoz.profil_surati:
            appDir = os.path.dirname(os.path.abspath(__file__))
            directory = os.path.dirname(appDir)
            os.remove(directory + str(user.ustoz.profil_surati))
        user.delete()
        messages.success(request, "Ustoz o\'chirildi.")
        return redirect('ustozlar')
    except:
        messages.error(request, "Ustozni ba'zi sabablarga ko'ra o'chirib bo'lmadi.")
        return redirect('ustozlar')


# Hujralar
def hujralar(request):
    admin = CustomUser.objects.get(id=request.user.id)
    hujralar = Hujra.objects.all()
    context = {
        'admin' : admin,
        'hujralar' : hujralar,

    }
    return render(request, 'admin_templates/hujralar.html', context)


@require_http_methods(['GET', 'POST'])
def hujra_kiritish(request):
    if request.method == 'GET':
        admin = CustomUser.objects.get(id=request.user.id)
        form = HujraKiritishForm()
        context = {
            'admin' : admin,
            'form' : form
        }
        return render(request, 'admin_templates/hujra_kiritish.html', context)
    if request.method == 'POST':
        form = HujraKiritishForm(request.POST)
        if form.is_valid():
            ism = form.cleaned_data['ism']
            adres = form.cleaned_data['adres']
            ustoz_id = form.cleaned_data['ustoz']
            try:
                ustoz = Ustoz.objects.get(admin=ustoz_id)
                hujra = Hujra(ism=ism, adres=adres, ustoz=ustoz)
                hujra.save()
                messages.success(request, "Hujra muvaffaqiyatli kiritildi")
                return redirect('hujralar')
            except:
                messages.error(request, "Afsuski ba'zi xatolar sababli hujra kiritilmadi...")
                return redirect('hujralar')


def hujra_profil(request, id):
    admin = CustomUser.objects.get(id=request.user.id)
    hujra = Hujra.objects.get(id=id)
    context = {
        'admin' : admin,
        'hujra' : hujra,

    }
    return render(request, 'admin_templates/hujra_profil.html', context)


@require_http_methods(['GET', 'POST'])
def hujra_profil_tahrirlash(request, id):
    if request.method == 'GET':
        admin = CustomUser.objects.get(id=request.user.id)
        hujra = Hujra.objects.get(id=id)
        ustozlar = Ustoz.objects.all()
        context = {
            'admin' : admin,
            'hujra' : hujra,
            'ustozlar' : ustozlar,
        }
        return render(request, 'admin_templates/hujra_profil_tahrirlash.html', context)
    if request.method == 'POST':
        ism =  request.POST.get('ism')
        adres = request.POST.get('adres')
        ustoz_id = request.POST.get('ustoz')
        try:
            hujra = Hujra.objects.get(id=id)
            hujra.ism = ism
            hujra.adres = adres
            if ustoz_id != "":
                ustoz = Ustoz.objects.get(id=ustoz_id)
                hujra.ustoz = ustoz
            hujra.save()
            messages.success(request, "Hujra muvaffaqiyatli tahrirlandi")
            return HttpResponseRedirect(reverse('hujra_profil', kwargs={'id': id}))
        except:
                messages.error(request, "Afsuski hujra tahrirlanmadi")
                return HttpResponseRedirect(reverse('hujra_profil', kwargs={'id': id}))


def hujra_uchirish(request, id):
    hujra = Hujra.objects.get(id=id)
    try:
        hujra.delete()
        messages.success(request, "Hujra o'chirildi.")
        return redirect("hujralar")

    except:
        messages.error(request, "Hujrani o'chirishda xatolik ro'y berdi.")
        return redirect("hujralar")


# Mudarrislar
def mudarrislar(request):
    admin = CustomUser.objects.get(id=request.user.id)
    mudarrislar = Mudarris.objects.all()
    context = {
        'admin' : admin,
        'mudarrislar' : mudarrislar
    }
    return render(request, 'admin_templates/mudarrislar.html', context)


@require_http_methods(["GET", "POST"])
def mudarris_kiritish(request):
    if request.method == 'GET':
        admin = CustomUser.objects.get(id=request.user.id)
        hujralar = Hujra.objects.all()
        context = {
            'admin' : admin,
            'hujralar' : hujralar,
        }
        return render(request, 'admin_templates/mudarris_kiritish.html', context)
    if request.method == 'POST':
        email =  request.POST.get('email')
        username = request.POST.get('username')
        parol = request.POST.get('parol')
        parolga_ishora = request.POST.get('parolga_ishora')
        ism = request.POST.get('ism')
        familya = request.POST.get('familya')
        adres = request.POST.get('adres')
        jins = request.POST.get('jins')
        hujra_id = request.POST.get('hujra')

        if len(request.FILES) != 0:
            profil_surati = request.FILES['profil_surati']
            pasport_surati = request.FILES['pasport_surati']
            fs = FileSystemStorage()
            profile_filename = fs.save(profil_surati.name, profil_surati)
            profil_surati_url = fs.url(profile_filename)
            pasport_filename = fs.save(pasport_surati.name, pasport_surati)
            pasport_surati_url = fs.url(pasport_filename)
        else:
            profil_surati_url = None
            pasport_surati_url = None
        # try:
        hujra = Hujra.objects.get(id=hujra_id)
        user = CustomUser.objects.create_user(username=username, password=parol, email=email, first_name=ism, last_name=familya, user_type=3)
        user.mudarris.parolga_ishora = parolga_ishora
        user.mudarris.adres = adres
        user.mudarris.jins = jins
        if profil_surati_url != None:
            user.mudarris.profil_surati = profil_surati_url
        if pasport_surati_url != None:
            user.mudarris.pasport_surati = pasport_surati_url
        user.mudarris.hujra = hujra
        user.save()
        messages.success(
            request, "Mudarris kiritish muvaffaqiyatli amalga oshirildi :)")
        return redirect('mudarrislar')
        # except:
        #     messages.error(
        #         request, "Mudarris kiritish ba'zi muommolar uchun amalga oshirilmadi :(")
        #     return redirect('mudarrislar')


def mudarris_profil(request, id):
    admin = CustomUser.objects.get(id=request.user.id)
    mudarris = Mudarris.objects.get(admin=id)
    context = {
        'admin' : admin,
        'mudarris' : mudarris,

    }
    return render(request, 'admin_templates/mudarris_profil.html', context)


@require_http_methods(["GET", "POST"])
def mudarris_profil_tahrirlash(request, id):
    if request.method == 'GET':
        admin = CustomUser.objects.get(id=request.user.id)
        mudarris = Mudarris.objects.get(admin=id)
        hujralar = Hujra.objects.all()
        context = {
            'admin' : admin,
            'mudarris' : mudarris,
            'hujralar' : hujralar,
        }
        return render(request, 'admin_templates/mudarris_profil_tahrirlash.html', context)
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        ism = request.POST.get('ism')
        familya = request.POST.get('familya')
        parol = request.POST.get('parol')
        parolga_ishora = request.POST.get('parolga_ishora')
        adres = request.POST.get('adres')
        jins = request.POST.get('jins')
        hujra_id = request.POST.get('hujra')
        
        try:
            mudarris = Mudarris.objects.get(admin=id)
            mudarris.admin.first_name = ism
            mudarris.admin.last_name = familya
            mudarris.admin.email = email
            mudarris.admin.username = username

            if parol != None and parol != "":
                mudarris.admin.password = parol

            if len(request.FILES) != 0:
                profil_surati = request.FILES['profil_surati']
                fs = FileSystemStorage()
                if mudarris.profil_surati:
                    appDir = os.path.dirname(os.path.abspath(__file__))
                    directory = os.path.dirname(appDir)
                    fs.delete(directory + str(mudarris.profil_surati))

                profilFileName = fs.save(profil_surati.name, profil_surati)
                profil_surati_url = fs.url(profilFileName)
            else:
                profil_surati_url = None

            if profil_surati_url != None:
                mudarris.profil_surati = profil_surati_url
            
            hujra = Hujra.objects.get(id=hujra_id)
            mudarris.hujra = hujra

            mudarris.parolga_ishora = parolga_ishora
            mudarris.adres = adres

            if jins != '':
                mudarris.jins = jins

            mudarris.save()

            messages.success(request, "Mudarris profil muvaffaqiyatli yangilandi")
            return HttpResponseRedirect(reverse('mudarris_profil', kwargs={'id': id}))
        except:
            messages.error(request, "Mudarris profilni yangilashda xato ro'y berdi :(")
            return HttpResponseRedirect(reverse('mudarris_profil', kwargs={'id': id}))

        
def mudarris_profil_suratni_uchirish(request, id):
    mudarris = Mudarris.objects.get(admin=id)
    try:
        if mudarris.profil_surati:
            fs = FileSystemStorage()
            appDir = os.path.dirname(os.path.abspath(__file__))
            directory = os.path.dirname(appDir)
            fs.delete(directory + str(mudarris.profil_surati))
            mudarris.profil_surati = None
            mudarris.save()    
            messages.success(request, "Mudarris profil surati muvaffaqiyatli o'chirildi")
            return HttpResponseRedirect(reverse('mudarris_profil', kwargs={'id': id}))
        else:
            messages.error(request, "Mudarrisning surati yo'q. Avval mudarrisga profil suratini kiriting...")
            return HttpResponseRedirect(reverse('mudarris_profil', kwargs={'id': id}))
    except:
        messages.error(request, "Afsuski mudarris profil surati o'chirilmadi")
        return HttpResponseRedirect(reverse('mudarris_profil', kwargs={'id': id}))


@require_http_methods(["GET", "POST"])
def mudarris_paspurt_tahrirlash(request, id):
    if request.method == 'GET':
        admin = CustomUser.objects.get(id=request.user.id)
        mudarris = Mudarris.objects.get(admin=id)
        context = {
        'admin' : admin,
        'mudarris' : mudarris,
        }
        return render(request, 'admin_templates/mudarris_paspurt_tahrirlash.html', context)
    if request.method == 'POST':
        mudarris = Mudarris.objects.get(admin=id)
        if len(request.FILES) != 0:
            pasport_surati = request.FILES['pasport_surati']
            fs = FileSystemStorage()
            if mudarris.pasport_surati:
                appDir = os.path.dirname(os.path.abspath(__file__))
                directory = os.path.dirname(appDir)
                fs.delete(directory + str(mudarris.pasport_surati))
            profilFileName = fs.save(pasport_surati.name, pasport_surati)
            paspurt_surati_url = fs.url(profilFileName)
        else:
            paspurt_surati_url = None
        try:
            if paspurt_surati_url != None:
                mudarris.pasport_surati = paspurt_surati_url
            mudarris.save()
            messages.success(request, "Mudarris paspurti muvaffaqiyatli yangilandi")
            return HttpResponseRedirect(reverse('mudarris_profil', kwargs={'id': id}))
        except:
            messages.error(request, "Mudarris paspurtini yangilashda xato ro'y berdi")
            return HttpResponseRedirect(reverse('mudarris_profil', kwargs={'id': id}))


def mudarris_pasport_suratni_uchirish(request, id):
    mudarris = Mudarris.objects.get(admin=id)
    try:
        if mudarris.pasport_surati:
            fs = FileSystemStorage()
            appDir = os.path.dirname(os.path.abspath(__file__))
            directory = os.path.dirname(appDir)
            fs.delete(directory + str(mudarris.pasport_surati))
            mudarris.pasport_surati = None
            mudarris.save()    
            messages.success(request, "Mudarris pasport surati muvaffaqiyatli o'chirildi")
            return HttpResponseRedirect(reverse('mudarris_profil', kwargs={'id': id}))
        else:
            messages.error(request, "Mudarrisning surati yo'q. Avval mudarrisning pasport suratini kiriting...")
            return HttpResponseRedirect(reverse('mudarris_profil', kwargs={'id': id}))
    except:
        messages.error(request, "Afsuski mudarris pasport surati o'chirilmadi")
        return HttpResponseRedirect(reverse('mudarris_profil', kwargs={'id': id}))


def mudarrisni_uchirish(request, id):
    user = CustomUser.objects.get(id=id)
    try:
        if user.mudarris.profil_surati:
            appDir = os.path.dirname(os.path.abspath(__file__))
            directory = os.path.dirname(appDir)
            os.remove(directory + str(user.mudarris.profil_surati))
        if user.mudarris.paspurt_surati:
            appDir = os.path.dirname(os.path.abspath(__file__))
            directory = os.path.dirname(appDir)
            os.remove(directory + str(user.mudarris.paspurt_surati))
        user.delete()
        messages.success(request, "Mudarris o\'chirildi.")
        return redirect('mudarrislar')
    except:
        messages.error(request, "Mudarrisni ba'zi sabablarga ko'ra o'chirib bo'lmadi.")
        return redirect('mudarrislar')


# talabalar
def talabalar(request):
    admin = CustomUser.objects.get(id=request.user.id)
    talabalar = Talaba.objects.all()
    context = {
        'admin' : admin,
        'talabalar' : talabalar
    }
    return render(request, 'admin_templates/talabalar.html', context)


@require_http_methods(["GET", "POST"])
def talaba_kiritish(request):
    if request.method == 'GET':
        admin = CustomUser.objects.get(id=request.user.id)
        hujralar = Hujra.objects.all()
        context = {
            'admin' : admin,
            'hujralar' : hujralar,
        }
        return render(request, 'admin_templates/talaba_kiritish.html', context)
    if request.method == 'POST':
        ism = request.POST.get('ism')
        familya = request.POST.get('familya')
        adres = request.POST.get('adres')
        jins = request.POST.get('jins')
        hujra_id = request.POST.get('hujra')
        try:
            if len(request.FILES) != 0:
                profil_surati = request.FILES['profil_surati']
                pasport_surati = request.FILES['pasport_surati']
                fs = FileSystemStorage()
                profile_filename = fs.save(profil_surati.name, profil_surati)
                profil_surati_url = fs.url(profile_filename)
                pasport_filename = fs.save(pasport_surati.name, pasport_surati)
                pasport_surati_url = fs.url(pasport_filename)
            else:
                profil_surati_url = None
                pasport_surati_url = None
        
            hujra = Hujra.objects.get(id=hujra_id)
            talaba = Talaba(ism=ism, familya=familya, adres=adres, jins=jins, profil_surati=profil_surati_url, pasport_surati=pasport_surati_url, hujra=hujra)
            talaba.save()
            messages.success(
                request, "Talaba kiritish muvaffaqiyatli amalga oshirildi :)")
            return redirect('talabalar')
        except:
            messages.error(
                request, "Talaba kiritish ba'zi muommolar uchun amalga oshirilmadi :(")
            return redirect('talabalar')


def talaba_profil(request, id):
    admin = CustomUser.objects.get(id=request.user.id)
    talaba = Talaba.objects.get(id=id)
    context = {
        'admin' : admin,
        'talaba' : talaba,

    }
    return render(request, 'admin_templates/talaba_profil.html', context)


@require_http_methods(["GET", "POST"])
def talaba_profil_tahrirlash(request, id):
    if request.method == 'GET':
        admin = CustomUser.objects.get(id=request.user.id)
        talaba = Talaba.objects.get(id=id)
        hujralar = Hujra.objects.all()
        context = {
            'admin' : admin,
            'talaba' : talaba,
            'hujralar' : hujralar,
        }
        return render(request, 'admin_templates/talaba_profil_tahrirlash.html', context)
    if request.method == 'POST':
        ism = request.POST.get('ism')
        familya = request.POST.get('familya')
        adres = request.POST.get('adres')
        jins = request.POST.get('jins')
        hujra_id = request.POST.get('hujra')
        
        try:
            talaba = Talaba.objects.get(id=id)
            talaba.ism = ism
            talaba.familya = familya
            if len(request.FILES) != 0:
                profil_surati = request.FILES['profil_surati']
                fs = FileSystemStorage()
                if talaba.profil_surati:
                    appDir = os.path.dirname(os.path.abspath(__file__))
                    directory = os.path.dirname(appDir)
                    fs.delete(directory + str(talaba.profil_surati))

                profilFileName = fs.save(profil_surati.name, profil_surati)
                profil_surati_url = fs.url(profilFileName)
            else:
                profil_surati_url = None

            if profil_surati_url != None:
                talaba.profil_surati = profil_surati_url
            
            hujra = Hujra.objects.get(id=hujra_id)
            talaba.hujra = hujra
            talaba.adres = adres

            if jins != '':
                talaba.jins = jins

            talaba.save()

            messages.success(request, "Talaba profil muvaffaqiyatli yangilandi")
            return HttpResponseRedirect(reverse('talaba_profil', kwargs={'id': id}))
        except:
            messages.error(request, "Talaba profilni yangilashda xato ro'y berdi :(")
            return HttpResponseRedirect(reverse('talaba_profil', kwargs={'id': id}))

        
def talaba_profil_suratni_uchirish(request, id):
    talaba = Talaba.objects.get(id=id)
    try:
        if talaba.profil_surati:
            fs = FileSystemStorage()
            appDir = os.path.dirname(os.path.abspath(__file__))
            directory = os.path.dirname(appDir)
            fs.delete(directory + str(talaba.profil_surati))
            talaba.profil_surati = None
            talaba.save()    
            messages.success(request, "Talaba profil surati muvaffaqiyatli o'chirildi")
            return HttpResponseRedirect(reverse('talaba_profil', kwargs={'id': id}))
        else:
            messages.error(request, "Mudarrisning surati yo'q. Avval mudarrisga profil suratini kiriting...")
            return HttpResponseRedirect(reverse('talaba_profil', kwargs={'id': id}))
    except:
        messages.error(request, "Afsuski talaba profil surati o'chirilmadi")
        return HttpResponseRedirect(reverse('talaba_profil', kwargs={'id': id}))


@require_http_methods(["GET", "POST"])
def talaba_paspurt_tahrirlash(request, id):
    if request.method == 'GET':
        admin = CustomUser.objects.get(id=request.user.id)
        talaba = Talaba.objects.get(id=id)
        context = {
        'admin' : admin,
        'talaba' : talaba,
        }
        return render(request, 'admin_templates/talaba_paspurt_tahrirlash.html', context)
    if request.method == 'POST':
        talaba = Talaba.objects.get(id=id)
        if len(request.FILES) != 0:
            pasport_surati = request.FILES['pasport_surati']
            fs = FileSystemStorage()
            if talaba.pasport_surati:
                appDir = os.path.dirname(os.path.abspath(__file__))
                directory = os.path.dirname(appDir)
                fs.delete(directory + str(talaba.pasport_surati))
            profilFileName = fs.save(pasport_surati.name, pasport_surati)
            paspurt_surati_url = fs.url(profilFileName)
        else:
            paspurt_surati_url = None
        try:
            if paspurt_surati_url != None:
                talaba.pasport_surati = paspurt_surati_url
            talaba.save()
            messages.success(request, "Talaba paspurti muvaffaqiyatli yangilandi")
            return HttpResponseRedirect(reverse('talaba_profil', kwargs={'id': id}))
        except:
            messages.error(request, "Talaba paspurtini yangilashda xato ro'y berdi")
            return HttpResponseRedirect(reverse('talaba_profil', kwargs={'id': id}))


def talaba_pasport_suratni_uchirish(request, id):
    talaba = Talaba.objects.get(id=id)
    try:
        if talaba.pasport_surati:
            fs = FileSystemStorage()
            appDir = os.path.dirname(os.path.abspath(__file__))
            directory = os.path.dirname(appDir)
            fs.delete(directory + str(talaba.pasport_surati))
            talaba.pasport_surati = None
            talaba.save()    
            messages.success(request, "Talaba pasport surati muvaffaqiyatli o'chirildi")
            return HttpResponseRedirect(reverse('talaba_profil', kwargs={'id': id}))
        else:
            messages.error(request, "Talabaning surati yo'q. Avval talabaning pasport suratini kiriting...")
            return HttpResponseRedirect(reverse('talaba_profil', kwargs={'id': id}))
    except:
        messages.error(request, "Afsuski talaba pasport surati o'chirilmadi")
        return HttpResponseRedirect(reverse('talaba_profil', kwargs={'id': id}))


def talabani_uchirish(request, id):
    talaba = Talaba.objects.get(id=id)
    try:
        if talaba.profil_surati:
            appDir = os.path.dirname(os.path.abspath(__file__))
            directory = os.path.dirname(appDir)
            os.remove(directory + str(talaba.profil_surati))
        if talaba.paspurt_surati:
            appDir = os.path.dirname(os.path.abspath(__file__))
            directory = os.path.dirname(appDir)
            os.remove(directory + str(talaba.paspurt_surati))
        talaba.delete()
        messages.success(request, "Talaba o\'chirildi.")
        return redirect('talabalar')
    except:
        messages.error(request, "Talabani ba'zi sabablarga ko'ra o'chirib bo'lmadi.")
        return redirect('talabalar')


# Fanlar Ustoz - talaba
def fanlar_ustoz_talaba(request):
    admin = CustomUser.objects.get(id=request.user.id)
    fanlar = FanUstozTalaba.objects.select_related('ustoz').all()
    context = {
        'admin' : admin,
        'fanlar' : fanlar
    }
    return render(request, 'admin_templates/fanlar_ustoz_talaba.html', context)


@require_http_methods(["GET", "POST"])
def fan_ustoz_talaba_kiritish(request):
    if request.method == 'GET':
        admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
        ustozlar = Ustoz.objects.select_related('admin').all()
        talabalar = Talaba.objects.all()
        context = {
            'admin' : admin,
            'ustozlar' : ustozlar,
            'talabalar' : talabalar
        }
        return render(request, 'admin_templates/fan_ustoz_talaba_kiritish.html', context)
    if request.method == 'POST':
        ism = request.POST.get('ism')
        ustoz_id = request.POST.get('ustoz')
        talabalar = request.POST.getlist('talabalar')
        tugash_vaqti = request.POST.get('tugash_vaqti')
        try:
            ustoz = Ustoz.objects.select_related('admin').get(admin=ustoz_id)
            fan = FanUstozTalaba.objects.create(ism=ism, ustoz=ustoz, tugash_vaqti=tugash_vaqti)
            for i in talabalar:
                fan.talaba.add(Talaba.objects.get(id=i))
            
            messages.success(request, 'Fan kiritildi')
            return redirect('fanlar_ustoz_talaba')
        except:
            messages.error(request, 'Fanni kiritishda qandaydur muommo yuz berdi')
            return redirect('fanlar_ustoz_talaba')


def fan_ustoz_talaba_profil(request, id):
    admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
    fan = FanUstozTalaba.objects.select_related('ustoz').prefetch_related('talaba').get(id=id)
    talabalar_soni = fan.talaba.count()
    context = {
        'admin' : admin,
        'fan' : fan,
        'talabalar_soni' : talabalar_soni
    }
    return render(request, 'admin_templates/fan_ustoz_talaba_profil.html', context)


@require_http_methods(["GET", "POST"])
def fan_ustoz_talaba_profil_tahrirlash(request, id):
     if request.method == 'GET':
        admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
        fan = FanUstozTalaba.objects.select_related('ustoz').get(id=id)
        ustozlar = Ustoz.objects.all()
        context = {
            'admin' : admin,
            'fan' : fan,
            'ustozlar' : ustozlar,
        }
        return render(request, 'admin_templates/fan_ustoz_talaba_profil_tahrirlash.html', context)
     if request.method == 'POST':
        ism = request.POST.get('ism')
        ustoz_id = request.POST.get('ustoz')
        tugash_vaqti = request.POST.get('tugash_vaqti')
        try:
            fan = FanUstozTalaba.objects.get(id=id)
            ustoz = Ustoz.objects.get(id=ustoz_id)
            fan.ism = ism
            fan.ustoz = ustoz
            if tugash_vaqti != None and tugash_vaqti != '':
                fan.tugash_vaqti = tugash_vaqti
            fan.save()
            messages.success(request, 'Fan yangilandi')
            return HttpResponseRedirect(reverse('fan_ustoz_talaba_profil', kwargs={'id': id}))
        except:
            messages.error(request, 'Fanni yangilashda muommo yuz berdi')
            return HttpResponseRedirect(reverse('fan_ustoz_talaba_profil', kwargs={'id': id}))


def fan_ustoz_talaba_profil_talabalar(request, id):
    admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
    fan = FanUstozTalaba.objects.select_related('ustoz').prefetch_related('talaba').get(id=id)
    talabalar = fan.talaba.all()
    context = {
        'admin' : admin,
        'fan' : fan,
        'talabalar' : talabalar
    }
    return render(request, 'admin_templates/fan_ustoz_talaba_profil_talabalar.html', context)


@require_http_methods(["GET", "POST"])
def fan_ustoz_talaba_profil_talabalar_kiritish(request, id):
    if request.method == 'GET':
        admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
        fan = FanUstozTalaba.objects.prefetch_related('talaba').get(id=id)
        talabalar = []
        for i in Talaba.objects.all():
            if i not in fan.talaba.all():
                talabalar.append(i)
        context = {
            'admin' : admin,
            'fan' : fan,
            'talabalar' : talabalar
            
        }
        return render(request, 'admin_templates/fan_ustoz_talaba_profil_talabalar_kiritish.html', context)
    if request.method == 'POST':
        talabalar = request.POST.getlist('talabalar')
        try:
            fan = FanUstozTalaba.objects.prefetch_related('talaba').get(id=id)
            for i in talabalar:
                fan.talaba.add(Talaba.objects.get(id=i))
            messages.success(request, 'Fanga talaba/lar kiritildi')
            return HttpResponseRedirect(reverse('fan_ustoz_talaba_profil_talabalar', kwargs={'id': id}))
        except:
            messages.error(request, 'Fanga talaba kiritishda qandaydur muommo yuz berdi')
            return HttpResponseRedirect(reverse('fan_ustoz_talaba_profil_talabalar', kwargs={'id': id}))


def fan_ustoz_talaba_profil_talabalar_uchirish(request, fanId, talabaId):
    fan = FanUstozTalaba.objects.prefetch_related('talaba').get(id=fanId)
    talaba = Talaba.objects.get(id=talabaId)
    try:
        fan.talaba.remove(talaba)
        messages.success(request, f'Fan "{fan.ism}"dan talaba "" o\'chirildi')
        return HttpResponseRedirect(reverse('fan_ustoz_talaba_profil_talabalar', kwargs={'id': fanId}))
    except:
        messages.error(request, f'Fan "{fan.ism}"dan talaba "" o\'chirildi')
        return HttpResponseRedirect(reverse('fan_ustoz_talaba_profil_talabalar', kwargs={'id': fanId}))


def fan_ustoz_talaba_uchirish(request, id):
    fan = FanUstozTalaba.objects.get(id=id)
    try:
        fan.delete()
        messages.success(request, 'Fan o\'chirildi')
        return redirect('fanlar_ustoz_talaba')
    except:
        messages.error(request, 'Fanni o\'chirishda qandaydir muommo ro\'y berdi')
        return redirect('fanlar_ustoz_talaba')


# Fanlar Ustoz - mudarris
def fanlar_ustoz_mudarris(request):
    admin = CustomUser.objects.get(id=request.user.id)
    fanlar = FanUstozMudarris.objects.select_related('ustoz').all()
    context = {
        'admin' : admin,
        'fanlar' : fanlar
    }
    return render(request, 'admin_templates/fanlar_ustoz_mudarris.html', context)


@require_http_methods(["GET", "POST"])
def fan_ustoz_mudarris_kiritish(request):
    if request.method == 'GET':
        admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
        ustozlar = Ustoz.objects.select_related('admin').all()
        mudarrislar = Mudarris.objects.all()
        context = {
            'admin' : admin,
            'ustozlar' : ustozlar,
            'mudarrislar' : mudarrislar
        }
        return render(request, 'admin_templates/fan_ustoz_mudarris_kiritish.html', context)
    if request.method == 'POST':
        ism = request.POST.get('ism')
        ustoz_id = request.POST.get('ustoz')
        mudarrislar = request.POST.getlist('mudarrislar')
        tugash_vaqti = request.POST.get('tugash_vaqti')
        try:
            ustoz = Ustoz.objects.select_related('admin').get(admin=ustoz_id)
            fan = FanUstozMudarris.objects.create(ism=ism, ustoz=ustoz, tugash_vaqti=tugash_vaqti)
            for i in mudarrislar:
                fan.mudarris.add(Mudarris.objects.get(id=i))
            
            messages.success(request, 'Fan kiritildi')
            return redirect('fanlar_ustoz_mudarris')
        except:
            messages.error(request, 'Fanni kiritishda qandaydur muommo yuz berdi')
            return redirect('fanlar_ustoz_mudarris')


def fan_ustoz_mudarris_profil(request, id):
    admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
    fan = FanUstozMudarris.objects.select_related('ustoz').prefetch_related('mudarris').get(id=id)
    mudarrislar_soni = fan.mudarris.count()
    context = {
        'admin' : admin,
        'fan' : fan,
        'mudarrislar_soni' : mudarrislar_soni
    }
    return render(request, 'admin_templates/fan_ustoz_mudarris_profil.html', context)


@require_http_methods(["GET", "POST"])
def fan_ustoz_mudarris_profil_tahrirlash(request, id):
     if request.method == 'GET':
        admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
        fan = FanUstozMudarris.objects.prefetch_related('mudarris').get(id=id)
        ustozlar = Ustoz.objects.all()
        context = {
            'admin' : admin,
            'fan' : fan,
            'ustozlar' : ustozlar,
        }
        return render(request, 'admin_templates/fan_ustoz_mudarris_profil_tahrirlash.html', context)
     if request.method == 'POST':
        try:
            ism = request.POST.get('ism')
            ustoz_id = request.POST.get('ustoz')
            tugash_vaqti = request.POST.get('tugash_vaqti')
            fan = FanUstozMudarris.objects.get(id=id)
            ustoz = Ustoz.objects.get(id=ustoz_id)
            fan.ism = ism
            fan.ustoz = ustoz
            if tugash_vaqti != None and tugash_vaqti != '':
                fan.tugash_vaqti = tugash_vaqti
            fan.save()
            messages.success(request, 'Fan yangilandi')
            return HttpResponseRedirect(reverse('fan_ustoz_mudarris_profil', kwargs={'id': id}))
        except:
            messages.error(request, 'Fanni yangilashda muommo yuz berdi')
            return HttpResponseRedirect(reverse('fan_ustoz_mudarris_profil', kwargs={'id': id}))


def fan_ustoz_mudarris_profil_mudarrislar(request, id):
    admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
    fan = FanUstozMudarris.objects.select_related('ustoz').prefetch_related('mudarris').get(id=id)
    mudarrislar = fan.mudarris.all()
    context = {
        'admin' : admin,
        'fan' : fan,
        'mudarrislar' : mudarrislar
    }
    return render(request, 'admin_templates/fan_ustoz_mudarris_profil_mudarrislar.html', context)


@require_http_methods(["GET", "POST"])
def fan_ustoz_mudarris_profil_mudarrislar_kiritish(request, id):
    if request.method == 'GET':
        admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
        fan = FanUstozMudarris.objects.prefetch_related('mudarris').get(id=id)
        mudarrislar = []
        for i in Mudarris.objects.select_related('admin').all():
            if i not in fan.mudarris.all():
                mudarrislar.append(i)
        context = {
            'admin' : admin,
            'fan' : fan,
            'mudarrislar' : mudarrislar
            
        }
        return render(request, 'admin_templates/fan_ustoz_mudarris_profil_mudarrislar_kiritish.html', context)
    if request.method == 'POST':
        mudarrislar = request.POST.getlist('mudarrislar')
        try:
            fan = FanUstozMudarris.objects.prefetch_related('mudarris').get(id=id)
            for i in mudarrislar:
                fan.mudarris.add(Mudarris.objects.get(id=i))
            messages.success(request, 'Fanga mudarris/lar kiritildi')
            return HttpResponseRedirect(reverse('fan_ustoz_mudarris_profil_mudarrislar', kwargs={'id': id}))
        except:
            messages.error(request, 'Fanga mudarris/lar kiritishda qandaydur muommo yuz berdi')
            return HttpResponseRedirect(reverse('fan_ustoz_mudarris_profil_mudarrislar', kwargs={'id': id}))


def fan_ustoz_mudarris_profil_mudarrislar_uchirish(request, fanId, mudarrisId):
    fan = FanUstozMudarris.objects.prefetch_related('mudarris').get(id=fanId)
    mudarris = Mudarris.objects.get(id=mudarrisId)
    try:
        fan.mudarris.remove(mudarris)
        messages.success(request, f'Fan "{fan.ism}"dan mudarris "" o\'chirildi')
        return HttpResponseRedirect(reverse('fan_ustoz_mudarris_profil_mudarrislar', kwargs={'id': fanId}))
    except:
        messages.error(request, f'Fan "{fan.ism}"dan mudarris "" o\'chirishda muommo ro\'y berdi')
        return HttpResponseRedirect(reverse('fan_ustoz_mudarris_profil_mudarrislar', kwargs={'id': fanId}))


def fan_ustoz_mudarris_uchirish(request, id):
    fan = FanUstozMudarris.objects.get(id=id)
    try:
        fan.delete()
        messages.success(request, 'Fan o\'chirildi')
        return redirect('fanlar_ustoz_mudarris')
    except:
        messages.error(request, 'Fanni o\'chirishda qandaydir muommo ro\'y berdi')
        return redirect('fanlar_ustoz_mudarris')


# Fanlar Mudarris - talaba
def fanlar_mudarris_talaba(request):
    admin = CustomUser.objects.get(id=request.user.id)
    fanlar = FanMudarrisTalaba.objects.select_related('mudarris').all()
    context = {
        'admin' : admin,
        'fanlar' : fanlar
    }
    return render(request, 'admin_templates/fanlar_mudarris_talaba.html', context)


@require_http_methods(["GET", "POST"])
def fan_mudarris_talaba_kiritish(request):
    if request.method == 'GET':
        admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
        mudarrislar = Mudarris.objects.select_related('admin').all()
        talabalar = Talaba.objects.all()
        context = {
            'admin' : admin,
            'mudarrislar' : mudarrislar,
            'talabalar' : talabalar,
        }
        return render(request, 'admin_templates/fan_mudarris_talaba_kiritish.html', context)
    if request.method == 'POST':
        ism = request.POST.get('ism')
        mudarris_id = request.POST.get('mudarris')
        talabalar = request.POST.getlist('talabalar')
        tugash_vaqti = request.POST.get('tugash_vaqti')
        try:
            mudarris = Mudarris.objects.select_related('admin').get(admin=mudarris_id)
            fan = FanMudarrisTalaba.objects.create(ism=ism, mudarris=mudarris, tugash_vaqti=tugash_vaqti)
            for i in talabalar:
                fan.talaba.add(Talaba.objects.get(id=i))
            
            messages.success(request, 'Fan kiritildi')
            return redirect('fanlar_mudarris_talaba')
        except:
            messages.error(request, 'Fanni kiritishda qandaydur muommo yuz berdi')
            return redirect('fanlar_mudarris_talaba')


def fan_mudarris_talaba_profil(request, id):
    admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
    fan = FanMudarrisTalaba.objects.select_related('mudarris').prefetch_related('talaba').get(id=id)
    talabalar_soni = fan.talaba.count()
    context = {
        'admin' : admin,
        'fan' : fan,
        'talabalar_soni' : talabalar_soni
    }
    return render(request, 'admin_templates/fan_mudarris_talaba_profil.html', context)


@require_http_methods(["GET", "POST"])
def fan_mudarris_talaba_profil_tahrirlash(request, id):
     if request.method == 'GET':
        admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
        fan = FanMudarrisTalaba.objects.select_related('mudarris').get(id=id)
        mudarrislar = Mudarris.objects.all()
        context = {
            'admin' : admin,
            'fan' : fan,
            'mudarrislar' : mudarrislar,
        }
        return render(request, 'admin_templates/fan_mudarris_talaba_profil_tahrirlash.html', context)
     if request.method == 'POST':
        ism = request.POST.get('ism')
        mudarris_id = request.POST.get('mudarris')
        tugash_vaqti = request.POST.get('tugash_vaqti')
        try:
            fan = FanMudarrisTalaba.objects.get(id=id)
            mudarris = Mudarris.objects.get(id=mudarris_id)
            fan.ism = ism
            fan.mudarris = mudarris
            if tugash_vaqti != None and tugash_vaqti != '':
                fan.tugash_vaqti = tugash_vaqti
            fan.save()
            messages.success(request, 'Fan yangilandi')
            return HttpResponseRedirect(reverse('fan_mudarris_talaba_profil', kwargs={'id': id}))
        except:
            messages.error(request, 'Fanni yangilashda muommo yuz berdi')
            return HttpResponseRedirect(reverse('fan_mudarris_talaba_profil', kwargs={'id': id}))


def fan_mudarris_talaba_profil_talabalar(request, id):
    admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
    fan = FanMudarrisTalaba.objects.select_related('mudarris').prefetch_related('talaba').get(id=id)
    talabalar = fan.talaba.all()
    context = {
        'admin' : admin,
        'fan' : fan,
        'talabalar' : talabalar
    }
    return render(request, 'admin_templates/fan_mudarris_talaba_profil_talabalar.html', context)


@require_http_methods(["GET", "POST"])
def fan_mudarris_talaba_profil_talabalar_kiritish(request, id):
    if request.method == 'GET':
        admin = CustomUser.objects.select_related('admin').get(id=request.user.id)
        fan = FanMudarrisTalaba.objects.prefetch_related('mudarris').get(id=id)
        talabalar = []
        for i in Talaba.objects.all():
            if i not in fan.talaba.all():
                talabalar.append(i)
        context = {
            'admin' : admin,
            'fan' : fan,
            'talabalar' : talabalar
            
        }
        return render(request, 'admin_templates/fan_mudarris_talaba_profil_talabalar_kiritish.html', context)
    if request.method == 'POST':
        talabalar = request.POST.getlist('talabalar')
        try:
            fan = FanMudarrisTalaba.objects.prefetch_related('talaba').get(id=id)
            for i in talabalar:
                fan.talaba.add(Talaba.objects.get(id=i))
            messages.success(request, 'Fanga talaba/lar kiritildi')
            return HttpResponseRedirect(reverse('fan_mudarris_talaba_profil_talabalar', kwargs={'id': id}))
        except:
            messages.error(request, 'Fanga talaba kiritishda qandaydur muommo yuz berdi')
            return HttpResponseRedirect(reverse('fan_mudarris_talaba_profil_talabalar', kwargs={'id': id}))


def fan_mudarris_talaba_profil_talabalar_uchirish(request, fanId, talabaId):
    fan = FanMudarrisTalaba.objects.prefetch_related('talaba').get(id=fanId)
    talaba = Talaba.objects.get(id=talabaId)
    try:
        fan.talaba.remove(talaba)
        messages.success(request, f'Fan "{fan.ism}"dan talaba "{talaba.ism}" o\'chirildi')
        return HttpResponseRedirect(reverse('fan_mudarris_talaba_profil_talabalar', kwargs={'id': fanId}))
    except:
        messages.error(request, f'Fan "{fan.ism}"dan talaba "{talaba.ism}" o\'chirildi')
        return HttpResponseRedirect(reverse('fan_mudarris_talaba_profil_talabalar', kwargs={'id': fanId}))


def fan_mudarris_talaba_uchirish(request, id):
    fan = FanMudarrisTalaba.objects.get(id=id)
    try:
        fan.delete()
        messages.success(request, 'Fan o\'chirildi')
        return redirect('fanlar_mudarris_talaba')
    except:
        messages.error(request, 'Fanni o\'chirishda qandaydir muommo ro\'y berdi')
        return redirect('fanlar_mudarris_talaba')



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


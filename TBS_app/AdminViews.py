from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.files.storage import FileSystemStorage  # To upload Profile Picture

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
            # try:
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
            # except:
            #     messages.error(request, "Afsuski admin profil yangilanmadi")
            #     return redirect('admin_profil')
        else:
            return redirect('admin_profil')


def admin_profile_suratni_uchirish(request):
    admin = Admin.objects.get(admin=request.user.id)
    try:
        admin.delete_picture()
        messages.success(request, "Admin profil surati muvaffaqiyatli o'chirildi")
        return redirect('admin_profil')
    except:
        messages.error(request, "Afsuski admin profil surati o'chirilmadi")
        return redirect('admin_profil')


# others
@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email)
    if user_obj.exists():
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)
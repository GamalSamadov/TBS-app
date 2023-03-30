from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from TBS_app.EmailBackEnd import EmailBackEnd


def loginPage(request):
    return render(request, 'login_updated.html')


def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h3>Bu jarayonni amalga oshirishga ruxsat yo`q!</h3>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get(
            'email'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            user_type = user.user_type
            # return HttpResponse("Email: "+request.POST.get('email')+ " Password: "+request.POST.get('password'))
            if user_type == '1':
                return redirect('admin_asosiy')

            elif user_type == '2':
                # return HttpResponse("Staff Login")
                return redirect('ustoz_asosiy')

            elif user_type == '3':
                # return HttpResponse("Student Login")
                return redirect('mudarris_asosiy')
            else:
                messages.error(request, "Noto`g`ri kirish!")
                return redirect('login')
        else:
            messages.error(request, "Kirish ma'lumotlari noto`g`ri!")
            # return HttpResponseRedirect("/")
            return redirect('login')


def get_user_details(request):
    if request.user != None:
        return HttpResponse("User: "+request.user.email+" User Type: "+request.user.user_type)
    else:
        return HttpResponse("Iltimos kirish qiling!")


def chiqish(request):
    logout(request)
    return HttpResponseRedirect('/')

def error_404(request, exception):
    return render(request, '404.html')


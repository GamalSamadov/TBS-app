from django.shortcuts import render, redirect


def mudarris_asosiy(request):
    return render(request, 'mudarris_template/asosiy.html')


def mudarris_kiritish(request):
    return render(request, 'mudarris_template/asosiy.html')
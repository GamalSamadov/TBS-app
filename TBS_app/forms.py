from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from .models import *


class AdminProfileForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AdminProfileForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update(
            {'placeholder': 'Diqqat! Faqat o\'zgartirmoqchi bo\'lsangiz bu yerga yozing.'})

    username = forms.CharField(label="Foydalanuvchi nomi", disabled=True, required=False, max_length=50, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    email = forms.CharField(label="Elektron pochta", disabled=True, required=False, max_length=50, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    first_name = forms.CharField(label="Ism", required=False, max_length=50, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Familya", required=False, max_length=50, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    password = forms.CharField(label="Parol", required=False, max_length=50, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    password_hint = forms.CharField(label="Parolga ishora", required=False, max_length=50, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    

class UstozKiritishForm(forms.Form):
    email = forms.EmailField(label='Elektron pochta', max_length=50, widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    username = forms.CharField(label="Foydalanuvchi nomi", max_length=50, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    parol = forms.CharField(label="Parol", max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control", }))
    parolga_ishora = forms.CharField(label="Parolga ishora", max_length=50, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    ism = forms.CharField(label="Ism", required=False, max_length=50, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    familya = forms.CharField(label="Familya", required=False, max_length=50, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    adres = forms.CharField(label="Adres", required=False, max_length=50, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    jins_list = (
        ('Erkak', 'Erkak'),
        ('Ayol', 'Ayol')
    )
    jins = forms.ChoiceField(label="Jins", required=False, choices=jins_list, widget=forms.Select(
        attrs={"class": "form-control"}))
    profil_surati = forms.FileField(label="Profil surati", required=False, widget=forms.FileInput(
        attrs={"class": "form-control", 'name' : 'profil_surati',}))
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
    profile_pic = forms.FileField(label="Profil surati", required=False, widget=forms.FileInput(
        attrs={"class": "form-control"}))


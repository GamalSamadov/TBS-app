from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from phone_field import PhoneField

# Overriding the Default Django Auth User and adding One More Field (user_type)
class CustomUser(AbstractUser):
    user_type_data = ((1, "Admin"), (2, "Ustoz"), (3, "Mudarris"))
    user_type = models.CharField(
        default=1, choices=user_type_data, max_length=10)


class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    password_hint = models.CharField(max_length=50, null=True)
    profile_pic = models.FileField(null=True, upload_to='admin/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Ustoz(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    adres = models.TextField(null=True)
    telefon_raqami = PhoneField(blank=True, help_text='Telefon raqami')
    telefon_raqami_tasdiqlangan = models.BooleanField(default=False)
    telefon_raqami_otp = models.CharField(max_length=6, null=True)
    jins = models.CharField(max_length=50, null=True)
    parolga_ishora = models.CharField(max_length=50, null=True)
    profil_surati = models.FileField(
        null=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Hujra(models.Model):
    id = models.AutoField(primary_key=True)
    ism = models.CharField(max_length=255)
    adres = models.TextField()
    ustoz = models.ForeignKey(Ustoz, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Mudarris(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    adres = models.TextField(null=True)
    telefon_raqami = PhoneField(blank=True, help_text='Telefon raqami', null=True)
    telefon_raqami_tasdiqlangan = models.BooleanField(default=False)
    telefon_raqami_otp = models.CharField(max_length=6, null=True)
    jins = models.CharField(max_length=50, null=True)
    parolga_ishora = models.CharField(max_length=50, null=True)
    profil_surati = models.ImageField(
        null=True)  
    pasport_surati = models.FileField(null=True)
    hujra = models.ForeignKey(
        Hujra, on_delete=models.CASCADE, default=1, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Talaba(models.Model):
    id = models.AutoField(primary_key=True)
    ism = models.CharField(max_length=255)
    familya = models.CharField(max_length=255)
    adres = models.TextField(null=True)
    jins = models.CharField(max_length=50)
    profil_surati = models.FileField(null=True)
    pasport_surati = models.FileField(null=True)
    hujra = models.ForeignKey(
        Hujra, on_delete=models.CASCADE, default=1, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class FanUstozTalaba(models.Model):
    id = models.AutoField(primary_key=True)
    ism = models.CharField(max_length=255, null=True)
    ustoz = models.ForeignKey(Ustoz, on_delete=models.CASCADE, null=True)
    talaba = models.ManyToManyField(Talaba)
    tugash_vaqti = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class FanUstozMudarris(models.Model):
    id = models.AutoField(primary_key=True)
    ism = models.CharField(max_length=255, null=True)
    ustoz = models.ForeignKey(Ustoz, on_delete=models.CASCADE, null=True)
    mudarris = models.ManyToManyField(Mudarris)
    tugash_vaqti = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class FanMudarrisTalaba(models.Model):
    id = models.AutoField(primary_key=True)
    ism = models.CharField(max_length=255, null=True)
    mudarris = models.ForeignKey(Mudarris, on_delete=models.CASCADE, null=True)
    talaba = models.ManyToManyField(Talaba)
    tugash_vaqti = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class KundalikBahoUstozTalaba(models.Model):
    id = models.AutoField(primary_key=True)
    fan = models.ForeignKey(FanUstozTalaba, on_delete=models.CASCADE, null=True)
    baho = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class KundalikBahoUstozMudarris(models.Model):
    id = models.AutoField(primary_key=True)
    fan = models.ForeignKey(FanUstozMudarris, on_delete=models.CASCADE, null=True)
    baho = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class KundalikBahoMudarrisTalaba(models.Model):
    id = models.AutoField(primary_key=True)
    fan = models.ForeignKey(FanMudarrisTalaba, on_delete=models.CASCADE, null=True)
    baho = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class ImtihonBahoUstozTalaba(models.Model):
    id = models.AutoField(primary_key=True)
    fan = models.ForeignKey(FanUstozTalaba, on_delete=models.CASCADE, null=True)
    ustozga_baho = models.FloatField(default=0)
    umuniy_baho = models.FloatField(default=0)
    izoh = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class ImtihonBahoUstozMudarris(models.Model):
    id = models.AutoField(primary_key=True)
    fan = models.ForeignKey(FanUstozMudarris, on_delete=models.CASCADE, null=True)
    ustozga_baho = models.FloatField(default=0)
    umuniy_baho = models.FloatField(default=0)
    izoh = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class ImtihonBahoMudarrisTalaba(models.Model):
    id = models.AutoField(primary_key=True)
    fan = models.ForeignKey(FanMudarrisTalaba, on_delete=models.CASCADE, null=True)
    ustozga_baho = models.FloatField(default=0)
    umuniy_baho = models.FloatField(default=0)
    izoh = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


# Creating Django Signals
# It's like trigger in database. It will run only when Data is Added in CustomUser model
@ receiver(post_save, sender=CustomUser)
# Now Creating a Function which will automatically insert data in HOD, Staff or Student
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        # Check the user_type and insert the data in respective tables
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        if instance.user_type == 2:
            Ustoz.objects.create(admin=instance)
        if instance.user_type == 3:
            Mudarris.objects.create(admin=instance, hujra=Hujra.objects.first(), parolga_ishora='', jins='', profil_surati='', pasport_surati='')

@ receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.ustoz.save()
    if instance.user_type == 3:
        instance.mudarris.save()

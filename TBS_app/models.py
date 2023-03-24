from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Overriding the Default Django Auth User and adding One More Field (user_type)
class CustomUser(AbstractUser):
    user_type_data = ((1, "Admin"), (2, "Ustoz"), (3, "Mudarris"))
    user_type = models.CharField(
        default=1, choices=user_type_data, max_length=10)


class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    password_hint = models.CharField(max_length=50, null=True)
    profile_pic = models.FileField(null=True, upload_to='admin/profile_pic/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def delete_picture(self):
        self.profile_pic.delete()
        self.profile_pic = None
        


class Ustoz(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    gender = models.CharField(max_length=50, null=True)
    password_hint = models.CharField(max_length=50, null=True)
    profile_pic = models.ImageField(
        null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Kurs(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    # def __str__(self):
    #     return self.course_name


class Fan(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)
    # need to give defauult course
    course_id = models.ForeignKey(
        Kurs, on_delete=models.CASCADE, default=1)
    ustoz_id = models.ForeignKey(Ustoz, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Mudarris(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=50)
    profile_pic = models.FileField(null=True)
    address = models.TextField()
    course_id = models.ForeignKey(
        Kurs, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Talaba(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=50)
    profile_pic = models.FileField(null=True)
    address = models.TextField()
    course_id = models.ForeignKey(
        Kurs, on_delete=models.DO_NOTHING, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class MudarrisKundalikBaho(models.Model):
    id = models.AutoField(primary_key=True)
    mudarris = models.ForeignKey(Mudarris, on_delete=models.CASCADE)
    fan = models.ForeignKey(Fan, on_delete=models.CASCADE)
    baho = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class TalabaKundalikBaho(models.Model):
    id = models.AutoField(primary_key=True)
    talaba = models.ForeignKey(Talaba, on_delete=models.CASCADE)
    fan = models.ForeignKey(Fan, on_delete=models.CASCADE)
    baho = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
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
            Mudarris.objects.create(admin=instance, course_id=Kurs.objects.first(),
                                    address="", profile_pic="", gender="")

@ receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.ustoz.save()
    if instance.user_type == 3:
        instance.mudarris.save()

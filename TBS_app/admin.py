from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
class UserModel(UserAdmin):
    pass


admin.site.register(CustomUser, UserModel)

admin.site.register(Admin)
admin.site.register(Ustoz)
admin.site.register(Kurs)
admin.site.register(Fan)
admin.site.register(Mudarris)

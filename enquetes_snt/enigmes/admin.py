from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Enigme, Enquete, Resultat, Image, Fichier
from enseignants.models import User

admin.site.register(Enigme)
admin.site.register(Enquete)
admin.site.register(Resultat)
admin.site.register(Image)
admin.site.register(Fichier)
#admin.site.register(User)

class MyUserAdmin(UserAdmin):
    list_display = ('id', 'last_name', 'first_name', 'email', 'username', 'is_active', 'date_joined', 'last_login', 'is_staff')
    search_fields = ('email', 'username', 'last_name', 'first_name')
    readonly_fields = ('id', 'date_joined', 'last_login')

admin.site.register(User, MyUserAdmin)

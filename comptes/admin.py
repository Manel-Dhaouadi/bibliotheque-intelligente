from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur, Profile

@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'est_actif', 'date_inscription']
    list_filter = ['role', 'est_actif', 'date_inscription']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('telephone', 'adresse', 'role', 'est_actif')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('email', 'telephone', 'adresse', 'role')
        }),
    )

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['utilisateur', 'date_naissance']
    search_fields = ['utilisateur__username']
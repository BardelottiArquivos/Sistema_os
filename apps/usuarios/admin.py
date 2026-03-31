from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'tipo', 'ativo')
    list_filter = ('tipo', 'ativo', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {
            'fields': ('tipo', 'telefone', 'matricula', 'foto', 'data_contratacao', 'ativo')
        }),
    )

admin.site.register(Usuario, UsuarioAdmin)

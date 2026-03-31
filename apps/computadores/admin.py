from django.contrib import admin
from .models import Computador

@admin.register(Computador)
class ComputadorAdmin(admin.ModelAdmin):
    list_display = ('nome_identificacao', 'cliente', 'tipo', 'fabricante', 'status', 'numero_serie')
    list_filter = ('tipo', 'status', 'fabricante')
    search_fields = ('nome_identificacao', 'numero_serie', 'patrimonio')

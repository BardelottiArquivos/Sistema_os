from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome_razao_social', 'tipo', 'cpf_cnpj', 'telefone', 'cidade', 'ativo')
    list_filter = ('tipo', 'ativo', 'cidade')
    search_fields = ('nome_razao_social', 'cpf_cnpj', 'email')
    list_editable = ('ativo',)

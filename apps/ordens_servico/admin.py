from django.contrib import admin
from .models import OrdemServico, ItemPeca

class ItemPecaInline(admin.TabularInline):
    model = ItemPeca
    extra = 1

@admin.register(OrdemServico)
class OrdemServicoAdmin(admin.ModelAdmin):
    list_display = ('numero_os', 'cliente', 'tecnico_responsavel', 'status', 'prioridade', 'data_abertura')
    list_filter = ('status', 'prioridade', 'data_abertura')
    search_fields = ('numero_os', 'cliente__nome_razao_social', 'titulo')
    readonly_fields = ('numero_os', 'valor_total')
    inlines = [ItemPecaInline]

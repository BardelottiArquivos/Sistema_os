# from django.shortcuts import render, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from datetime import datetime, timedelta
# from .services import RelatorioOSService


# @login_required
# def dashboard_relatorios(request):
#     context = {
#         'hoje': datetime.now().date(),
#         'ultimo_mes': (datetime.now() - timedelta(days=30)).date(),
#     }
#     return render(request, 'relatorios/dashboard.html', context)


# @login_required
# def relatorio_os_pdf(request, os_id):
#     from apps.ordens_servico.models import OrdemServico
#     ordem = get_object_or_404(OrdemServico, id=os_id)
#     return RelatorioOSService.gerar_relatorio_os(ordem)


# @login_required
# def relatorio_periodo_pdf(request):
#     from apps.ordens_servico.models import OrdemServico
    
#     data_inicio_str = request.GET.get('data_inicio')
#     data_fim_str = request.GET.get('data_fim')
#     status = request.GET.get('status')
    
#     if data_inicio_str:
#         data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d').date()
#     else:
#         data_inicio = datetime.now().date() - timedelta(days=30)
    
#     if data_fim_str:
#         data_fim = datetime.strptime(data_fim_str, '%Y-%m-%d').date()
#     else:
#         data_fim = datetime.now().date()
    
#     return RelatorioOSService.gerar_relatorio_periodo(data_inicio, data_fim, status)

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template
from django.db.models import Count, Sum, Q
from datetime import datetime, timedelta
from io import BytesIO
import xhtml2pdf.pisa as pisa
import json
from .services import RelatorioOSService

from apps.ordens_servico.models import OrdemServico
from apps.clientes.models import Cliente
from apps.computadores.models import Computador
from apps.usuarios.models import Usuario


@login_required
def dashboard_relatorios(request):
    """Dashboard de relatórios com estatísticas"""
    
    # Dados gerais
    total_os = OrdemServico.objects.count()
    total_clientes = Cliente.objects.count()
    total_computadores = Computador.objects.count()
    total_tecnicos = Usuario.objects.filter(tipo='tecnico').count()
    
    # OS por status
    os_por_status = OrdemServico.objects.values('status').annotate(total=Count('id'))
    
    # OS por prioridade
    os_por_prioridade = OrdemServico.objects.values('prioridade').annotate(total=Count('id'))
    
    # Faturamento total
    faturamento_total = OrdemServico.objects.aggregate(total=Sum('valor_total'))['total'] or 0
    
    # Faturamento por mês (últimos 6 meses)
    meses = []
    valores = []
    for i in range(5, -1, -1):
        data_inicio = datetime.now().replace(day=1) - timedelta(days=30*i)
        mes_ano = data_inicio.strftime('%b/%Y')
        total_mes = OrdemServico.objects.filter(
            data_abertura__year=data_inicio.year,
            data_abertura__month=data_inicio.month
        ).aggregate(total=Sum('valor_total'))['total'] or 0
        meses.append(mes_ano)
        valores.append(float(total_mes))
    
    # OS recentes
    os_recentes = OrdemServico.objects.all().order_by('-data_abertura')[:10]
    
    context = {
        'total_os': total_os,
        'total_clientes': total_clientes,
        'total_computadores': total_computadores,
        'total_tecnicos': total_tecnicos,
        'faturamento_total': faturamento_total,
        'os_por_status': os_por_status,
        'os_por_prioridade': os_por_prioridade,
        'meses': json.dumps(meses),
        'valores': json.dumps(valores),
        'os_recentes': os_recentes,
        'status_cores': {
            'aberta': 'secondary',
            'em_andamento': 'warning',
            'aguardando_peca': 'info',
            'aguardando_cliente': 'info',
            'concluida': 'success',
            'paga': 'primary',
            'cancelada': 'danger',
        },
        'prioridade_cores': {
            'baixa': 'secondary',
            'normal': 'info',
            'alta': 'warning',
            'urgente': 'danger',
        },
        'hoje': datetime.now().date(),
        'ultimo_mes': (datetime.now() - timedelta(days=30)).date(),
    }
    
    return render(request, 'relatorios/dashboard.html', context)


@login_required
def relatorio_os_pdf(request, os_id):
    """Gera PDF de uma OS específica"""
    ordem = get_object_or_404(OrdemServico, id=os_id)
    return RelatorioOSService.gerar_relatorio_os(ordem)


@login_required
def relatorio_periodo_pdf(request):
    """Gera PDF de OS por período"""
    data_inicio_str = request.GET.get('data_inicio')
    data_fim_str = request.GET.get('data_fim')
    status = request.GET.get('status')
    
    if data_inicio_str:
        data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d').date()
    else:
        data_inicio = datetime.now().date() - timedelta(days=30)
    
    if data_fim_str:
        data_fim = datetime.strptime(data_fim_str, '%Y-%m-%d').date()
    else:
        data_fim = datetime.now().date()
    
    return RelatorioOSService.gerar_relatorio_periodo(data_inicio, data_fim, status)


@login_required
def relatorio_gerencial_pdf(request):
    """Gera relatório gerencial completo em PDF"""
    from django.db.models import Count, Sum
    
    # Dados para o relatório
    total_os = OrdemServico.objects.count()
    total_clientes = Cliente.objects.count()
    total_computadores = Computador.objects.count()
    faturamento_total = OrdemServico.objects.aggregate(total=Sum('valor_total'))['total'] or 0
    
    # OS por status
    os_por_status = OrdemServico.objects.values('status').annotate(total=Count('id'))
    
    # OS por técnico
    os_por_tecnico = OrdemServico.objects.values(
        'tecnico_responsavel__username',
        'tecnico_responsavel__first_name'
    ).annotate(total=Count('id')).order_by('-total')[:5]
    
    # OS por mês (últimos 6 meses)
    meses = []
    valores = []
    for i in range(5, -1, -1):
        data_inicio = datetime.now().replace(day=1) - timedelta(days=30*i)
        mes_ano = data_inicio.strftime('%b/%Y')
        total_mes = OrdemServico.objects.filter(
            data_abertura__year=data_inicio.year,
            data_abertura__month=data_inicio.month
        ).aggregate(total=Sum('valor_total'))['total'] or 0
        meses.append(mes_ano)
        valores.append(float(total_mes))
    
    context = {
        'total_os': total_os,
        'total_clientes': total_clientes,
        'total_computadores': total_computadores,
        'faturamento_total': faturamento_total,
        'os_por_status': os_por_status,
        'os_por_tecnico': os_por_tecnico,
        'meses': meses,
        'valores': valores,
        'data_emissao': datetime.now(),
        'status_dict': dict(OrdemServico.STATUS),
        'prioridade_dict': dict(OrdemServico.PRIORIDADE),
    }
    
    return RelatorioService.gerar_pdf('relatorios/relatorio_gerencial.html', context, 'relatorio_gerencial.pdf')
    
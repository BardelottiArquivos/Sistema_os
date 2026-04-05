from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from .services import RelatorioOSService


@login_required
def dashboard_relatorios(request):
    context = {
        'hoje': datetime.now().date(),
        'ultimo_mes': (datetime.now() - timedelta(days=30)).date(),
    }
    return render(request, 'relatorios/dashboard.html', context)


@login_required
def relatorio_os_pdf(request, os_id):
    from apps.ordens_servico.models import OrdemServico
    ordem = get_object_or_404(OrdemServico, id=os_id)
    return RelatorioOSService.gerar_relatorio_os(ordem)


@login_required
def relatorio_periodo_pdf(request):
    from apps.ordens_servico.models import OrdemServico
    
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
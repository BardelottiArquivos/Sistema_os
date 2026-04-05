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
#     # Importar dentro da função para evitar circularidade
#     from apps.ordens_servico.models import OrdemServico
#     ordem = get_object_or_404(OrdemServico, id=os_id)
#     return RelatorioOSService.gerar_relatorio_os(ordem)


# @login_required
# def relatorio_periodo_pdf(request):
#     # Importar dentro da função para evitar circularidade
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

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from apps.ordens_servico.models import OrdemServico


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    
    return render(request, 'usuarios/login.html')


@login_required
def dashboard(request):
    context = {
        'total_os': OrdemServico.objects.count(),
        'os_abertas': OrdemServico.objects.filter(status='aberta').count(),
        'os_andamento': OrdemServico.objects.filter(status='em_andamento').count(),
        'os_concluidas': OrdemServico.objects.filter(status='concluida').count(),
        'ultimas_os': OrdemServico.objects.all().order_by('-data_abertura')[:10],
    }
    return render(request, 'dashboard.html', context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


def criar_admin(request):
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@email.com',
            password='25252525',
            matricula='ADMIN001'
        )
        return JsonResponse({'status': 'Admin criado com sucesso!'})
    return JsonResponse({'status': 'Admin já existe'})
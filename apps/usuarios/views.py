from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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

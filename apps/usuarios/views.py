from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from apps.ordens_servico.models import OrdemServico

# ----------------------------------------------------------------------------
# CRUD de Usuários (Admin)
# ----------------------------------------------------------------------------
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Usuario


class UsuarioListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Usuario
    template_name = 'usuarios/usuario_list.html'
    context_object_name = 'usuarios'
    paginate_by = 10
    
    def get_queryset(self):
        return Usuario.objects.all().order_by('-date_joined')
    
    def test_func(self):
        return self.request.user.tipo == 'admin' or self.request.user.is_superuser


class UsuarioCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Usuario
    template_name = 'usuarios/usuario_form.html'
    fields = ['username', 'first_name', 'last_name', 'email', 'tipo', 'telefone', 'matricula', 'ativo']
    success_url = reverse_lazy('usuario_list')
    
    def test_func(self):
        return self.request.user.tipo == 'admin' or self.request.user.is_superuser
    
    def form_valid(self, form):
        form.instance.set_password('123456')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['senha_padrao'] = '123456'
        return context


class UsuarioUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Usuario
    template_name = 'usuarios/usuario_form.html'
    fields = ['first_name', 'last_name', 'email', 'tipo', 'telefone', 'matricula', 'ativo']
    success_url = reverse_lazy('usuario_list')
    
    def test_func(self):
        return self.request.user.tipo == 'admin' or self.request.user.is_superuser


class UsuarioDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Usuario
    template_name = 'usuarios/usuario_confirm_delete.html'
    success_url = reverse_lazy('usuario_list')
    
    def test_func(self):
        return self.request.user.tipo == 'admin' or self.request.user.is_superuser
    
    def get_queryset(self):
        # Impedir que o usuário exclua a si mesmo
        return Usuario.objects.exclude(id=self.request.user.id)
    
    def delete(self, request, *args, **kwargs):
        """Desativa o usuário em vez de excluir (soft delete)"""
        self.object = self.get_object()
        self.object.ativo = False
        self.object.save()
        messages.success(request, f'Usuário {self.object.username} foi desativado.')
        return redirect(self.success_url)


# ----------------------------------------------------------------------------
# VIEWS DE AUTENTICAÇÃO E DASHBOARD
# ----------------------------------------------------------------------------

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
    """Exibe o dashboard com gráficos e estatísticas"""
    
    # ============================================
    # 1. CARDS DE RESUMO
    # ============================================
    total_os = OrdemServico.objects.count()
    total_os_abertas = OrdemServico.objects.filter(status='aberta').count()
    total_os_andamento = OrdemServico.objects.filter(status='em_andamento').count()
    total_os_concluidas = OrdemServico.objects.filter(status='concluida').count()
    
    # ============================================
    # 2. GRÁFICO: OS POR STATUS
    # ============================================
    os_por_status = OrdemServico.objects.values('status').annotate(total=Count('id'))
    
    # Converter para listas que o Chart.js entende
    status_labels = [item['status'] for item in os_por_status]
    status_data = [item['total'] for item in os_por_status]
    
    # Dicionário para mapear status para nome legível no gráfico
    status_nomes = dict(OrdemServico.STATUS)
    
    # ============================================
    # 3. GRÁFICO: OS POR PRIORIDADE
    # ============================================
    os_por_prioridade = OrdemServico.objects.values('prioridade').annotate(total=Count('id'))
    
    prioridade_labels = [item['prioridade'] for item in os_por_prioridade]
    prioridade_data = [item['total'] for item in os_por_prioridade]
    
    # Dicionário para mapear prioridade para nome legível
    prioridade_nomes = dict(OrdemServico.PRIORIDADE)
    
    # ============================================
    # 4. GRÁFICO: FATURAMENTO MENSAL (últimos 6 meses)
    # ============================================
    faturamento_mensal = OrdemServico.objects \
        .annotate(mes=TruncMonth('data_abertura')) \
        .values('mes') \
        .annotate(total_mes=Sum('valor_total')) \
        .order_by('-mes')[:6]
    
    # Preparar dados para o gráfico (em ordem cronológica crescente)
    meses_labels = [item['mes'].strftime('%b/%Y') for item in faturamento_mensal][::-1]
    faturamento_data = [float(item['total_mes']) for item in faturamento_mensal][::-1]
    
    # ============================================
    # 5. ÚLTIMAS ORDENS DE SERVIÇO
    # ============================================
    ultimas_os = OrdemServico.objects.all().order_by('-data_abertura')[:10]
    
    # ============================================
    # CONTEXTO PARA O TEMPLATE
    # ============================================
    context = {
        # Cards
        'total_os': total_os,
        'total_os_abertas': total_os_abertas,
        'total_os_andamento': total_os_andamento,
        'total_os_concluidas': total_os_concluidas,
        
        # Gráfico de Status
        'status_labels_json': status_labels,
        'status_data_json': status_data,
        'status_nomes': status_nomes,
        
        # Gráfico de Prioridade
        'prioridade_labels_json': prioridade_labels,
        'prioridade_data_json': prioridade_data,
        'prioridade_nomes': prioridade_nomes,
        
        # Gráfico de Faturamento
        'faturamento_labels_json': meses_labels,
        'faturamento_data_json': faturamento_data,
        
        # Últimas OS
        'ultimas_os': ultimas_os,
    }
    
    return render(request, 'dashboard.html', context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


# ----------------------------------------------------------------------------
# FUNÇÃO TEMPORÁRIA PARA CRIAR ADMIN
# ----------------------------------------------------------------------------
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
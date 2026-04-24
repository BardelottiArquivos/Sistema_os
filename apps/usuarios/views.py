from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from apps.ordens_servico.models import OrdemServico

# ----------------------------------------------------------------------------
# Esta sendo adcionado para criar usuário
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


class UsuarioUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Usuario
    template_name = 'usuarios/usuario_form.html'
    fields = ['first_name', 'last_name', 'email', 'tipo', 'telefone', 'matricula', 'ativo']
    success_url = reverse_lazy('usuario_list')
    
    def test_func(self):
        return self.request.user.tipo == 'admin' or self.request.user.is_superuser


#class UsuarioDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#    model = Usuario
#    template_name = 'usuarios/usuario_confirm_delete.html'
#    success_url = reverse_lazy('usuario_list')
#    
#    def test_func(self):
#        return self.request.user.tipo == 'admin' or self.request.user.is_superuser
#    
#    def get_queryset(self):
#        return Usuario.objects.exclude(id=self.request.user.id)

class UsuarioDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Usuario
    template_name = 'usuarios/usuario_confirm_delete.html'
    success_url = reverse_lazy('usuario_list')
    
    def test_func(self):
        return self.request.user.tipo == 'admin' or self.request.user.is_superuser
    
    def get_queryset(self):
        return Usuario.objects.exclude(id=self.request.user.id)
    
    def delete(self, request, *args, **kwargs):
        """Método personalizado para tratar erros na exclusão"""
        self.object = self.get_object()
        
        # Verificar se o usuário tem OS vinculadas
        from apps.ordens_servico.models import OrdemServico
        
        # Verificar como técnico
        if hasattr(self.object, 'ordens_tecnico'):
            os_count = self.object.ordens_tecnico.count()
            if os_count > 0:
                messages.error(
                    request, 
                    f'Não é possível excluir {self.object.username}. '
                    f'Este usuário possui {os_count} ordem(ns) de serviço vinculada(s).'
                )
                return redirect('usuario_list')
        
        try:
            # Tentar excluir
            self.object.delete()
            messages.success(request, f'Usuário {self.object.username} excluído com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao excluir usuário: {str(e)}')
        
        return redirect(self.success_url)

# -----------------------------------------------------------

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


# ⚠️ FUNÇÃO TEMPORÁRIA PARA CRIAR ADMIN - USE UMA VEZ E DEPOIS REMOVA
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
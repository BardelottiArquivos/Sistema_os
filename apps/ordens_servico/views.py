# from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
# from django.urls import reverse_lazy
# from django.contrib.auth.mixins import LoginRequiredMixin
# from .models import OrdemServico

# class OSListView(LoginRequiredMixin, ListView):
#     model = OrdemServico
#     template_name = 'ordens_servico/os_list.html'
#     context_object_name = 'ordens'
#     paginate_by = 10

# class OSCreateView(LoginRequiredMixin, CreateView):
#     model = OrdemServico
#     template_name = 'ordens_servico/os_form.html'
#     fields = '__all__'
#     success_url = reverse_lazy('os_list')

# class OSDetailView(LoginRequiredMixin, DetailView):
#     model = OrdemServico
#     template_name = 'ordens_servico/os_detail.html'
#     context_object_name = 'os'

# class OSUpdateView(LoginRequiredMixin, UpdateView):
#     model = OrdemServico
#     template_name = 'ordens_servico/os_form.html'
#     fields = '__all__'
#     success_url = reverse_lazy('os_list')

# class OSDeleteView(LoginRequiredMixin, DeleteView):
#     model = OrdemServico
#     template_name = 'ordens_servico/os_confirm_delete.html'
#     success_url = reverse_lazy('os_list')

from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from .models import OrdemServico
from apps.usuarios.models import Usuario


# ============================================
# LISTAGEM DE ORDENS DE SERVIÇO
# ============================================

class OSListView(LoginRequiredMixin, ListView):
    model = OrdemServico
    template_name = 'ordens_servico/os_list.html'
    context_object_name = 'ordens'
    paginate_by = 10
    
    def get_queryset(self):
        user = self.request.user
        queryset = OrdemServico.objects.all()
        
        # Técnico vê apenas suas OS
        if user.tipo == 'tecnico' and not user.is_superuser:
            queryset = queryset.filter(tecnico_responsavel=user)
        
        # Filtrar por status (salvar o valor para usar no contexto)
        self.status_filtro = self.request.GET.get('status', '')
        if self.status_filtro:
            queryset = queryset.filter(status=self.status_filtro)
        
        return queryset.order_by('-data_abertura')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_atual'] = self.status_filtro
        context['status_opcoes'] = OrdemServico.STATUS
        return context


# ============================================
# CRIAÇÃO DE ORDEM DE SERVIÇO
# ============================================

class OSCreateView(LoginRequiredMixin, CreateView):
    model = OrdemServico
    template_name = 'ordens_servico/os_form.html'
    fields = ['cliente', 'computador', 'tecnico_responsavel', 'titulo', 
              'descricao_problema', 'observacoes', 'prioridade', 'data_previsao', 
              'valor_mao_obra', 'valor_pecas', 'desconto']
    success_url = reverse_lazy('os_list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Mostrar apenas usuários do tipo técnico
        form.fields['tecnico_responsavel'].queryset = Usuario.objects.filter(tipo='tecnico')
        form.fields['tecnico_responsavel'].empty_label = "Selecione um técnico"
        form.fields['computador'].required = False
        return form
    
    def form_valid(self, form):
        messages.success(self.request, 'Ordem de Serviço criada com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao criar Ordem de Serviço. Verifique os dados.')
        return super().form_invalid(form)


# ============================================
# DETALHES DA ORDEM DE SERVIÇO
# ============================================

class OSDetailView(LoginRequiredMixin, DetailView):
    model = OrdemServico
    template_name = 'ordens_servico/os_detail.html'
    context_object_name = 'os'


# ============================================
# EDIÇÃO DE ORDEM DE SERVIÇO
# ============================================

class OSUpdateView(LoginRequiredMixin, UpdateView):
    model = OrdemServico
    template_name = 'ordens_servico/os_form.html'
    fields = ['cliente', 'computador', 'tecnico_responsavel', 'titulo', 
              'descricao_problema', 'observacoes', 'solucao_aplicada',
              'prioridade', 'status', 'data_previsao', 'data_inicio', 'data_conclusao',
              'valor_mao_obra', 'valor_pecas', 'desconto']
    success_url = reverse_lazy('os_list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['tecnico_responsavel'].queryset = Usuario.objects.filter(tipo='tecnico')
        form.fields['tecnico_responsavel'].empty_label = "Selecione um técnico"
        form.fields['computador'].required = False
        return form


# ============================================
# EXCLUSÃO DE ORDEM DE SERVIÇO
# ============================================

class OSDeleteView(LoginRequiredMixin, DeleteView):
    model = OrdemServico
    template_name = 'ordens_servico/os_confirm_delete.html'
    success_url = reverse_lazy('os_list')
    context_object_name = 'object'  # ← Importante!


# ============================================
# MUDANÇA DE STATUS DA ORDEM DE SERVIÇO
# ============================================

@login_required
def mudar_status(request, os_id, novo_status):
    """Muda o status da ordem de serviço"""
    os = get_object_or_404(OrdemServico, id=os_id)
    
    # Verificar permissão
    user = request.user
    if user.tipo not in ['admin', 'gerente', 'tecnico'] and not user.is_superuser:
        messages.error(request, 'Você não tem permissão para alterar status.')
        return redirect('os_detail', pk=os_id)
    
    # Técnico só pode alterar suas OS
    if user.tipo == 'tecnico' and os.tecnico_responsavel != user:
        messages.error(request, 'Você só pode alterar suas próprias ordens de serviço.')
        return redirect('os_detail', pk=os_id)
    
    # Validar status
    status_validos = [s[0] for s in OrdemServico.STATUS]
    if novo_status not in status_validos:
        messages.error(request, 'Status inválido.')
        return redirect('os_detail', pk=os_id)
    
    # Salvar status anterior para mensagem
    status_anterior = os.status
    
    # Atualizar status
    os.status = novo_status
    
    # Atualizar datas automaticamente
    if novo_status == 'em_andamento' and not os.data_inicio:
        os.data_inicio = timezone.now()
    elif novo_status == 'concluida' and not os.data_conclusao:
        os.data_conclusao = timezone.now()
    
    os.save()
    
    # Mensagem de sucesso
    status_dict = dict(OrdemServico.STATUS)
    messages.success(
        request, 
        f'Status alterado de "{status_dict.get(status_anterior, status_anterior)}" para "{os.get_status_display()}"'
    )
    return redirect('os_detail', pk=os_id)


# ============================================
# API PARA BUSCAR OS PELO NÚMERO (RELATÓRIOS)
# ============================================

def buscar_os_por_numero(request):
    """API para buscar OS pelo número (ex: 2025/0001)"""
    numero = request.GET.get('numero')
    if not numero:
        return JsonResponse({'error': 'Número não informado'}, status=400)
    
    try:
        os = OrdemServico.objects.get(numero_os=numero)
        return JsonResponse({'id': os.id})
    except OrdemServico.DoesNotExist:
        return JsonResponse({'error': 'OS não encontrada'}, status=404)
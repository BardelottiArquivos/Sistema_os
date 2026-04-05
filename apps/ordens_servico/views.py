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
from .models import OrdemServico
from apps.usuarios.models import Usuario
from django.http import JsonResponse


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
        
        return queryset.order_by('-data_abertura')


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
        form.fields['computador'].required = False
        return form
    
    def form_valid(self, form):
        messages.success(self.request, 'Ordem de Serviço criada com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao criar Ordem de Serviço. Verifique os dados.')
        return super().form_invalid(form)


class OSDetailView(LoginRequiredMixin, DetailView):
    model = OrdemServico
    template_name = 'ordens_servico/os_detail.html'
    context_object_name = 'os'


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
        form.fields['computador'].required = False
        return form


class OSDeleteView(LoginRequiredMixin, DeleteView):
    model = OrdemServico
    template_name = 'ordens_servico/os_confirm_delete.html'
    success_url = reverse_lazy('os_list')

# API para buscar OS pelo número (ex. 2024/0001)
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
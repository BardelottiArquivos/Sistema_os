from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import OrdemServico

class OSListView(LoginRequiredMixin, ListView):
    model = OrdemServico
    template_name = 'ordens_servico/os_list.html'
    context_object_name = 'ordens'
    paginate_by = 10

class OSCreateView(LoginRequiredMixin, CreateView):
    model = OrdemServico
    template_name = 'ordens_servico/os_form.html'
    fields = '__all__'
    success_url = reverse_lazy('os_list')

class OSDetailView(LoginRequiredMixin, DetailView):
    model = OrdemServico
    template_name = 'ordens_servico/os_detail.html'
    context_object_name = 'os'

class OSUpdateView(LoginRequiredMixin, UpdateView):
    model = OrdemServico
    template_name = 'ordens_servico/os_form.html'
    fields = '__all__'
    success_url = reverse_lazy('os_list')

class OSDeleteView(LoginRequiredMixin, DeleteView):
    model = OrdemServico
    template_name = 'ordens_servico/os_confirm_delete.html'
    success_url = reverse_lazy('os_list')

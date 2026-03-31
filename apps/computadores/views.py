from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Computador

class ComputadorListView(LoginRequiredMixin, ListView):
    model = Computador
    template_name = 'computadores/computador_list.html'
    context_object_name = 'computadores'
    paginate_by = 10

class ComputadorCreateView(LoginRequiredMixin, CreateView):
    model = Computador
    template_name = 'computadores/computador_form.html'
    fields = '__all__'
    success_url = reverse_lazy('computador_list')

class ComputadorDetailView(LoginRequiredMixin, DetailView):
    model = Computador
    template_name = 'computadores/computador_detail.html'
    context_object_name = 'computador'

class ComputadorUpdateView(LoginRequiredMixin, UpdateView):
    model = Computador
    template_name = 'computadores/computador_form.html'
    fields = '__all__'
    success_url = reverse_lazy('computador_list')

class ComputadorDeleteView(LoginRequiredMixin, DeleteView):
    model = Computador
    template_name = 'computadores/computador_confirm_delete.html'
    success_url = reverse_lazy('computador_list')

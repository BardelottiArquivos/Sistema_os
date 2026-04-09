from django.urls import path
from . import views

app_name = 'relatorios'

urlpatterns = [
    path('', views.dashboard_relatorios, name='dashboard'),
    path('os/<int:os_id>/pdf/', views.relatorio_os_pdf, name='os_pdf'),
    path('periodo/pdf/', views.relatorio_periodo_pdf, name='periodo_pdf'),
]
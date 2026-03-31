from django.urls import path
from . import views
from .views_api import consultar_cep

urlpatterns = [
    path('', views.ClienteListView.as_view(), name='cliente_list'),
    path('novo/', views.ClienteCreateView.as_view(), name='cliente_create'),
    path('<int:pk>/', views.ClienteDetailView.as_view(), name='cliente_detail'),
    path('<int:pk>/editar/', views.ClienteUpdateView.as_view(), name='cliente_update'),
    path('<int:pk>/excluir/', views.ClienteDeleteView.as_view(), name='cliente_delete'),
    path('api/consultar-cep/', consultar_cep, name='consultar_cep'),
]

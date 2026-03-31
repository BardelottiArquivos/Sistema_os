from django.urls import path
from . import views

urlpatterns = [
    path('', views.ComputadorListView.as_view(), name='computador_list'),
    path('novo/', views.ComputadorCreateView.as_view(), name='computador_create'),
    path('<int:pk>/', views.ComputadorDetailView.as_view(), name='computador_detail'),
    path('<int:pk>/editar/', views.ComputadorUpdateView.as_view(), name='computador_update'),
    path('<int:pk>/excluir/', views.ComputadorDeleteView.as_view(), name='computador_delete'),
]

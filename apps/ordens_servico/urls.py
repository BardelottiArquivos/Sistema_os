from django.urls import path
from . import views

urlpatterns = [
    path('', views.OSListView.as_view(), name='os_list'),
    path('nova/', views.OSCreateView.as_view(), name='os_create'),
    path('<int:pk>/', views.OSDetailView.as_view(), name='os_detail'),
    path('<int:pk>/editar/', views.OSUpdateView.as_view(), name='os_update'),
    path('<int:pk>/excluir/', views.OSDeleteView.as_view(), name='os_delete'),
    path('status/<int:os_id>/<str:novo_status>/', views.mudar_status, name='mudar_status'),  # ← ADICIONAR ESTA LINHA
]

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # CRUD de usuários
    path('lista/', views.UsuarioListView.as_view(), name='usuario_list'),
    path('novo/', views.UsuarioCreateView.as_view(), name='usuario_create'),
    path('<int:pk>/editar/', views.UsuarioUpdateView.as_view(), name='usuario_update'),
    path('<int:pk>/excluir/', views.UsuarioDeleteView.as_view(), name='usuario_delete'),
]
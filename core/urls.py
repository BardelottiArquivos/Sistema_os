"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.usuarios.views import login_view, dashboard, logout_view, criar_admin
from apps.ordens_servico.views import buscar_os_por_numero

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    
    # URLs temporárias (remover depois)
    path('criar-admin/', criar_admin, name='criar_admin'),
    
   
    # Apps
    # primeira linha adicionadapara usuario
    path('usuarios/', include('apps.usuarios.urls')),
    path('clientes/', include('apps.clientes.urls')),
    path('computadores/', include('apps.computadores.urls')),
    path('ordens/', include('apps.ordens_servico.urls')),
    path('relatorios/', include('apps.relatorios.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



urlpatterns = [
    # ... outras URLs ...
    path('api/buscar-os/', buscar_os_por_numero, name='buscar_os'),
]
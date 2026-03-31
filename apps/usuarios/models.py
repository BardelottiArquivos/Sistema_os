from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    TIPO_USUARIO = (
        ('admin', 'Administrador'),
        ('gerente', 'Gerente'),
        ('tecnico', 'Técnico'),
    )
    
    tipo = models.CharField(max_length=10, choices=TIPO_USUARIO, default='tecnico')
    telefone = models.CharField(max_length=20, blank=True)
    matricula = models.CharField(max_length=20, unique=True)
    foto = models.ImageField(upload_to='usuarios/', null=True, blank=True)
    data_contratacao = models.DateField(null=True, blank=True)
    ativo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
    
    def __str__(self):
        return f"{self.get_full_name()} - {self.get_tipo_display()}"

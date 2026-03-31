from django.db import models
from apps.clientes.models import Cliente

class Computador(models.Model):
    TIPO_COMPUTADOR = (
        ('desktop', 'Desktop'),
        ('notebook', 'Notebook'),
        ('servidor', 'Servidor'),
        ('all_in_one', 'All in One'),
    )
    
    STATUS = (
        ('ativo', 'Em Uso'),
        ('inativo', 'Inativo'),
        ('manutencao', 'Em Manutenção'),
        ('baixado', 'Baixado'),
    )
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='computadores')
    tipo = models.CharField(max_length=20, choices=TIPO_COMPUTADOR)
    numero_serie = models.CharField(max_length=100, unique=True)
    patrimonio = models.CharField(max_length=50, blank=True)
    nome_identificacao = models.CharField(max_length=100)
    fabricante = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    processador = models.CharField(max_length=200)
    memoria_ram = models.CharField(max_length=50)
    armazenamento = models.CharField(max_length=200)
    sistema_operacional = models.CharField(max_length=100)
    possui_monitor = models.BooleanField(default=False)
    possui_teclado = models.BooleanField(default=False)
    possui_mouse = models.BooleanField(default=False)
    observacoes_hardware = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='ativo')
    data_aquisicao = models.DateField(null=True, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    ultima_manutencao = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Computador'
        verbose_name_plural = 'Computadores'
        ordering = ['cliente', 'nome_identificacao']
    
    def __str__(self):
        return f"{self.nome_identificacao} - {self.cliente.nome_razao_social}"

from django.db import models
from django.contrib.auth import get_user_model
from apps.clientes.models import Cliente
from apps.computadores.models import Computador
from datetime import datetime

Usuario = get_user_model()

class OrdemServico(models.Model):
    PRIORIDADE = (
        ('baixa', 'Baixa'),
        ('normal', 'Normal'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    )
    
    STATUS = (
        ('aberta', 'Aberta'),
        ('em_andamento', 'Em Andamento'),
        ('aguardando_peca', 'Aguardando Peça'),
        ('aguardando_cliente', 'Aguardando Cliente'),
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada'),
        ('paga', 'Paga'), # Adcionado para controle financeiro
    )
    
    numero_os = models.CharField(max_length=20, unique=True, editable=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    computador = models.ForeignKey(Computador, on_delete=models.PROTECT, null=True, blank=True)
    tecnico_responsavel = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='ordens_tecnico')
    gerente_aprovador = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='ordens_aprovadas', null=True, blank=True)
    titulo = models.CharField(max_length=200)
    descricao_problema = models.TextField()
    observacoes = models.TextField(blank=True)
    solucao_aplicada = models.TextField(blank=True)
    prioridade = models.CharField(max_length=20, choices=PRIORIDADE, default='normal')
    status = models.CharField(max_length=20, choices=STATUS, default='aberta')
    data_abertura = models.DateTimeField(auto_now_add=True)
    data_previsao = models.DateField(null=True, blank=True)
    data_inicio = models.DateTimeField(null=True, blank=True)
    data_conclusao = models.DateTimeField(null=True, blank=True)
    valor_mao_obra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_pecas = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        verbose_name = 'Ordem de Serviço'
        verbose_name_plural = 'Ordens de Serviço'
        ordering = ['-data_abertura']
    
    def __str__(self):
        return f"OS #{self.numero_os} - {self.cliente.nome_razao_social}"
    
    def save(self, *args, **kwargs):
        if not self.numero_os:
            ano = self.data_abertura.year if self.data_abertura else datetime.now().year
            ultima_os = OrdemServico.objects.filter(
                numero_os__startswith=str(ano)
            ).order_by('numero_os').last()
            
            if ultima_os:
                ultimo_numero = int(ultima_os.numero_os.split('/')[-1])
                novo_numero = ultimo_numero + 1
            else:
                novo_numero = 1
            
            self.numero_os = f"{ano}/{str(novo_numero).zfill(4)}"
        
        self.valor_total = self.valor_mao_obra + self.valor_pecas - self.desconto
        super().save(*args, **kwargs)


class ItemPeca(models.Model):
    ordem_servico = models.ForeignKey(OrdemServico, on_delete=models.CASCADE, related_name='itens')
    descricao = models.CharField(max_length=200)
    quantidade = models.IntegerField(default=1)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    
    def save(self, *args, **kwargs):
        self.valor_total = self.quantidade * self.valor_unitario
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.descricao} - {self.quantidade}x"

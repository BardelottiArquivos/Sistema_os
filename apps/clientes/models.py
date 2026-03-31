from django.db import models
from django.core.validators import RegexValidator

class Cliente(models.Model):
    TIPO_CLIENTE = (
        ('fisica', 'Pessoa Física'),
        ('juridica', 'Pessoa Jurídica'),
    )
    
    tipo = models.CharField(max_length=10, choices=TIPO_CLIENTE)
    nome_razao_social = models.CharField('Nome/Razão Social', max_length=200)
    cpf_cnpj = models.CharField('CPF/CNPJ', max_length=20, unique=True)
    rg_ie = models.CharField('RG/IE', max_length=20, blank=True)
    
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    celular = models.CharField(max_length=20, blank=True)
    
    cep = models.CharField(max_length=9, validators=[RegexValidator(r'^\d{5}-?\d{3}$')])
    logradouro = models.CharField(max_length=200)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    
    observacoes = models.TextField(blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nome_razao_social']
    
    def __str__(self):
        return self.nome_razao_social

from django.db import models
from django.utils import timezone

# Create your models here.

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
    endereco = models.TextField()
    dataCadastro = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nome

class Departamento(models.Model):
    nome = models.CharField(max_length=100)
    responsavel = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    horarioFuncionamento = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Atendente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='atendentes')
    nivelAcesso = models.IntegerField()
    dataContratacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nome

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    tempoResposta = models.IntegerField(help_text="Tempo de resposta em horas")
    departamentoResponsavel = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='categorias')

    def __str__(self):
        return self.nome

class Chamado(models.Model):
    STATUS_CHOICES = [
        ('aberto', 'Aberto'),
        ('em_andamento', 'Em Andamento'),
        ('aguardando', 'Aguardando Resposta'),
        ('resolvido', 'Resolvido'),
        ('fechado', 'Fechado'),
    ]
    
    PRIORIDADE_CHOICES = [
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta'),
        ('critica', 'Crítica'),
    ]
    
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberto')
    prioridade = models.CharField(max_length=20, choices=PRIORIDADE_CHOICES, default='media')
    dataAbertura = models.DateTimeField(default=timezone.now)
    dataFechamento = models.DateTimeField(null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='chamados')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='chamados')
    atendente = models.ForeignKey(Atendente, on_delete=models.SET_NULL, null=True, blank=True, related_name='chamados')

    def __str__(self):
        return self.titulo

class Solucao(models.Model):
    descricao = models.TextField()
    passos = models.TextField()
    dataCriacao = models.DateTimeField(default=timezone.now)
    autor = models.CharField(max_length=100)
    chamado = models.ForeignKey(Chamado, on_delete=models.CASCADE, related_name='solucoes')

    def __str__(self):
        return f"Solução para {self.chamado.titulo}"

class Avaliacao(models.Model):
    TIPO_CHOICES = [
        ('atendimento', 'Avaliação do Atendimento'),
        ('solucao', 'Avaliação da Solução'),
    ]
    
    nota = models.IntegerField()
    comentario = models.TextField(blank=True)
    dataAvaliacao = models.DateTimeField(default=timezone.now)
    tipoAvaliacao = models.CharField(max_length=20, choices=TIPO_CHOICES)
    chamado = models.OneToOneField(Chamado, on_delete=models.CASCADE, related_name='avaliacao')

    def __str__(self):
        return f"Avaliação de {self.chamado.titulo}"

class Historico(models.Model):
    acao = models.CharField(max_length=100)
    dataAcao = models.DateTimeField(default=timezone.now)
    usuario = models.CharField(max_length=100)
    detalhes = models.TextField()
    chamado = models.ForeignKey(Chamado, on_delete=models.CASCADE, related_name='historicos')

    def __str__(self):
        return f"{self.acao} - {self.chamado.titulo}"

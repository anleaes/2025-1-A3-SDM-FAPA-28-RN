from django.contrib import admin
from .models import (
    Cliente, 
    Atendente, 
    Chamado, 
    Categoria, 
    Avaliacao, 
    Solucao, 
    Historico, 
    Departamento
)

# Register your models here.
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'dataCadastro')
    search_fields = ('nome', 'email')
    list_filter = ('dataCadastro',)

@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'responsavel', 'email', 'telefone')
    search_fields = ('nome', 'responsavel')

@admin.register(Atendente)
class AtendenteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'departamento', 'nivelAcesso', 'dataContratacao')
    search_fields = ('nome', 'email')
    list_filter = ('departamento', 'nivelAcesso', 'dataContratacao')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tempoResposta', 'departamentoResponsavel')
    search_fields = ('nome',)
    list_filter = ('departamentoResponsavel',)

@admin.register(Chamado)
class ChamadoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'cliente', 'status', 'prioridade', 'categoria', 'atendente', 'dataAbertura')
    search_fields = ('titulo', 'descricao')
    list_filter = ('status', 'prioridade', 'categoria', 'dataAbertura')

@admin.register(Solucao)
class SolucaoAdmin(admin.ModelAdmin):
    list_display = ('chamado', 'autor', 'dataCriacao')
    search_fields = ('descricao', 'autor')
    list_filter = ('dataCriacao',)

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('chamado', 'nota', 'tipoAvaliacao', 'dataAvaliacao')
    search_fields = ('comentario',)
    list_filter = ('nota', 'tipoAvaliacao')

@admin.register(Historico)
class HistoricoAdmin(admin.ModelAdmin):
    list_display = ('acao', 'chamado', 'usuario', 'dataAcao')
    search_fields = ('acao', 'detalhes', 'usuario')
    list_filter = ('dataAcao',)

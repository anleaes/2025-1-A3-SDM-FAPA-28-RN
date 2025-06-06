from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone

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

from .serializers import (
    ClienteSerializer,
    AtendenteSerializer,
    ChamadoSerializer,
    CategoriaSerializer,
    AvaliacaoSerializer,
    SolucaoSerializer,
    HistoricoSerializer,
    DepartamentoSerializer
)

from .historico import (
    registrar_abertura_chamado,
    registrar_atualizacao_status,
    registrar_atribuicao_atendente,
    registrar_solucao,
    registrar_avaliacao,
    registrar_fechamento
)

from . import estatisticas

# Create your views here.
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    
    @action(detail=True, methods=['get'])
    def chamados(self, request, pk=None):
        """
        Retorna todos os chamados de um cliente
        """
        cliente = self.get_object()
        chamados = Chamado.objects.filter(cliente=cliente)
        serializer = ChamadoSerializer(chamados, many=True)
        return Response(serializer.data)

class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    
    @action(detail=True, methods=['get'])
    def atendentes(self, request, pk=None):
        """
        Retorna todos os atendentes de um departamento
        """
        departamento = self.get_object()
        atendentes = Atendente.objects.filter(departamento=departamento)
        serializer = AtendenteSerializer(atendentes, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def categorias(self, request, pk=None):
        """
        Retorna todas as categorias associadas a um departamento
        """
        departamento = self.get_object()
        categorias = Categoria.objects.filter(departamentoResponsavel=departamento)
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)

class AtendenteViewSet(viewsets.ModelViewSet):
    queryset = Atendente.objects.all()
    serializer_class = AtendenteSerializer
    
    @action(detail=True, methods=['get'])
    def chamados(self, request, pk=None):
        """
        Retorna todos os chamados atendidos por um atendente
        """
        atendente = self.get_object()
        chamados = Chamado.objects.filter(atendente=atendente)
        serializer = ChamadoSerializer(chamados, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def atender_chamado(self, request, pk=None):
        """
        Atendente assume um chamado
        """
        atendente = self.get_object()
        chamado_id = request.data.get('chamado_id')
        
        try:
            chamado = Chamado.objects.get(pk=chamado_id)
            chamado.atendente = atendente
            chamado.status = 'em_andamento'
            chamado.save()
            
            # Registrar no histórico
            registrar_atribuicao_atendente(chamado, atendente, atendente.nome)
            
            return Response({'status': 'Chamado atribuído com sucesso'})
        except Chamado.DoesNotExist:
            return Response(
                {'erro': 'Chamado não encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    
    @action(detail=True, methods=['get'])
    def chamados(self, request, pk=None):
        """
        Retorna todos os chamados de uma categoria
        """
        categoria = self.get_object()
        chamados = Chamado.objects.filter(categoria=categoria)
        serializer = ChamadoSerializer(chamados, many=True)
        return Response(serializer.data)

class ChamadoViewSet(viewsets.ModelViewSet):
    queryset = Chamado.objects.all()
    serializer_class = ChamadoSerializer
    
    def perform_create(self, serializer):
        """
        Ao criar um chamado, registra no histórico
        """
        chamado = serializer.save()
        # Registrar a abertura do chamado no histórico
        registrar_abertura_chamado(chamado, chamado.cliente.nome)
    
    @action(detail=True, methods=['post'])
    def atualizar_status(self, request, pk=None):
        """
        Atualiza o status de um chamado
        """
        chamado = self.get_object()
        status_anterior = chamado.status
        status_novo = request.data.get('status')
        usuario = request.data.get('usuario', 'Sistema')
        
        if status_novo not in [choice[0] for choice in Chamado.STATUS_CHOICES]:
            return Response(
                {'erro': 'Status inválido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        chamado.status = status_novo
        
        # Se estiver fechando o chamado, registra a data
        if status_novo == 'fechado':
            chamado.dataFechamento = timezone.now()
            chamado.save()
            registrar_fechamento(chamado, usuario)
        else:
            chamado.save()
            registrar_atualizacao_status(chamado, status_anterior, status_novo, usuario)
        
        return Response({'status': 'Status atualizado com sucesso'})
    
    @action(detail=True, methods=['get'])
    def solucoes(self, request, pk=None):
        """
        Retorna todas as soluções de um chamado
        """
        chamado = self.get_object()
        solucoes = Solucao.objects.filter(chamado=chamado)
        serializer = SolucaoSerializer(solucoes, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def historico(self, request, pk=None):
        """
        Retorna todo o histórico de um chamado
        """
        chamado = self.get_object()
        historicos = Historico.objects.filter(chamado=chamado).order_by('-dataAcao')
        serializer = HistoricoSerializer(historicos, many=True)
        return Response(serializer.data)

class SolucaoViewSet(viewsets.ModelViewSet):
    queryset = Solucao.objects.all()
    serializer_class = SolucaoSerializer
    
    def perform_create(self, serializer):
        """
        Ao criar uma solução, atualiza o status do chamado e cria um histórico
        """
        solucao = serializer.save()
        chamado = solucao.chamado
        
        # Atualiza o status do chamado para resolvido
        status_anterior = chamado.status
        chamado.status = 'resolvido'
        chamado.save()
        
        # Registrar a solução no histórico
        registrar_solucao(chamado, solucao, solucao.autor)
        registrar_atualizacao_status(chamado, status_anterior, 'resolvido', solucao.autor)

class AvaliacaoViewSet(viewsets.ModelViewSet):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer
    
    def perform_create(self, serializer):
        """
        Ao criar uma avaliação, cria um histórico
        """
        avaliacao = serializer.save()
        chamado = avaliacao.chamado
        
        # Registrar a avaliação no histórico
        registrar_avaliacao(chamado, avaliacao, chamado.cliente.nome)

class HistoricoViewSet(viewsets.ModelViewSet):
    queryset = Historico.objects.all()
    serializer_class = HistoricoSerializer
    
    def get_queryset(self):
        """
        Opcionalmente filtra o conjunto de resultados com base em parâmetros de consulta
        """
        queryset = Historico.objects.all().order_by('-dataAcao')
        chamado_id = self.request.query_params.get('chamado', None)
        
        if chamado_id is not None:
            queryset = queryset.filter(chamado__id=chamado_id)
            
        return queryset

# API para estatísticas
class EstatisticasView(APIView):
    """
    View para obter estatísticas do sistema
    """
    def get(self, request, format=None):
        """
        Retorna um resumo das estatísticas
        """
        return Response(estatisticas.resumo_estatisticas())
    
    @action(detail=False, methods=['get'])
    def por_status(self, request):
        """
        Retorna a contagem de chamados por status
        """
        return Response(estatisticas.chamados_por_status())
    
    @action(detail=False, methods=['get'])
    def por_prioridade(self, request):
        """
        Retorna a contagem de chamados por prioridade
        """
        return Response(estatisticas.chamados_por_prioridade())
    
    @action(detail=False, methods=['get'])
    def por_categoria(self, request):
        """
        Retorna a contagem de chamados por categoria
        """
        return Response(estatisticas.chamados_por_categoria())
    
    @action(detail=False, methods=['get'])
    def por_departamento(self, request):
        """
        Retorna a contagem de chamados por departamento
        """
        return Response(estatisticas.chamados_por_departamento())
    
    @action(detail=False, methods=['get'])
    def avaliacao_media(self, request):
        """
        Retorna a média geral das avaliações
        """
        return Response(estatisticas.media_avaliacao_geral())
    
    @action(detail=False, methods=['get'])
    def avaliacao_por_atendente(self, request):
        """
        Retorna a média das avaliações por atendente
        """
        return Response(estatisticas.media_avaliacao_por_atendente())
    
    @action(detail=False, methods=['get'])
    def tempo_resolucao(self, request):
        """
        Retorna o tempo médio de resolução
        """
        return Response({'tempo_medio_horas': estatisticas.media_tempo_resolucao()})
    
    @action(detail=False, methods=['get'])
    def desempenho_atendentes(self, request):
        """
        Retorna estatísticas de desempenho dos atendentes
        """
        return Response(estatisticas.desempenho_atendentes())

# API Views para estatísticas individuais
@api_view(['GET'])
def estatisticas_resumo(request):
    """
    Retorna um resumo das estatísticas
    """
    return Response(estatisticas.resumo_estatisticas())

@api_view(['GET'])
def estatisticas_por_status(request):
    """
    Retorna a contagem de chamados por status
    """
    return Response(estatisticas.chamados_por_status())

@api_view(['GET'])
def estatisticas_por_prioridade(request):
    """
    Retorna a contagem de chamados por prioridade
    """
    return Response(estatisticas.chamados_por_prioridade())

@api_view(['GET'])
def estatisticas_por_categoria(request):
    """
    Retorna a contagem de chamados por categoria
    """
    return Response(estatisticas.chamados_por_categoria())

@api_view(['GET'])
def estatisticas_por_departamento(request):
    """
    Retorna a contagem de chamados por departamento
    """
    return Response(estatisticas.chamados_por_departamento())

@api_view(['GET'])
def avaliacao_media(request):
    """
    Retorna a média geral das avaliações
    """
    return Response(estatisticas.media_avaliacao_geral())

@api_view(['GET'])
def avaliacao_por_atendente(request):
    """
    Retorna a média das avaliações por atendente
    """
    return Response(estatisticas.media_avaliacao_por_atendente())

@api_view(['GET'])
def tempo_resolucao(request):
    """
    Retorna o tempo médio de resolução
    """
    return Response({'tempo_medio_horas': estatisticas.media_tempo_resolucao()})

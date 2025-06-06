from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ClienteViewSet,
    AtendenteViewSet,
    ChamadoViewSet,
    CategoriaViewSet,
    AvaliacaoViewSet,
    SolucaoViewSet,
    HistoricoViewSet,
    DepartamentoViewSet,
    EstatisticasView,
    estatisticas_resumo,
    estatisticas_por_status,
    estatisticas_por_prioridade,
    estatisticas_por_categoria,
    estatisticas_por_departamento,
    avaliacao_media,
    avaliacao_por_atendente,
    tempo_resolucao
)

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'atendentes', AtendenteViewSet)
router.register(r'chamados', ChamadoViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'avaliacoes', AvaliacaoViewSet)
router.register(r'solucoes', SolucaoViewSet)
router.register(r'historicos', HistoricoViewSet)
router.register(r'departamentos', DepartamentoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    # Rotas para estatísticas
    path('estatisticas/', EstatisticasView.as_view(), name='estatisticas'),
    path('estatisticas/resumo/', estatisticas_resumo, name='estatisticas-resumo'),
    path('estatisticas/por-status/', estatisticas_por_status, name='estatisticas-por-status'),
    path('estatisticas/por-prioridade/', estatisticas_por_prioridade, name='estatisticas-por-prioridade'),
    path('estatisticas/por-categoria/', estatisticas_por_categoria, name='estatisticas-por-categoria'),
    path('estatisticas/por-departamento/', estatisticas_por_departamento, name='estatisticas-por-departamento'),
    path('estatisticas/avaliacao-media/', avaliacao_media, name='avaliacao-media'),
    path('estatisticas/avaliacao-por-atendente/', avaliacao_por_atendente, name='avaliacao-por-atendente'),
    path('estatisticas/tempo-resolucao/', tempo_resolucao, name='tempo-resolucao'),
] 
from django.db.models import Avg, Count, F, Q, Sum
from django.utils import timezone
from datetime import timedelta
from .models import Chamado, Avaliacao, Categoria, Departamento, Atendente

def chamados_por_status():
    """
    Retorna a contagem de chamados por status
    """
    return Chamado.objects.values('status').annotate(total=Count('id')).order_by('status')

def chamados_por_prioridade():
    """
    Retorna a contagem de chamados por prioridade
    """
    return Chamado.objects.values('prioridade').annotate(total=Count('id')).order_by('prioridade')

def chamados_por_categoria():
    """
    Retorna a contagem de chamados por categoria
    """
    return Chamado.objects.values('categoria__nome').annotate(
        total=Count('id'),
        categoria_nome=F('categoria__nome')
    ).order_by('categoria__nome')

def chamados_por_departamento():
    """
    Retorna a contagem de chamados por departamento responsável
    """
    return Chamado.objects.values('categoria__departamentoResponsavel__nome').annotate(
        total=Count('id'),
        departamento_nome=F('categoria__departamentoResponsavel__nome')
    ).order_by('categoria__departamentoResponsavel__nome')

def media_avaliacao_geral():
    """
    Retorna a média geral das avaliações
    """
    return Avaliacao.objects.aggregate(media=Avg('nota'))

def media_avaliacao_por_tipo():
    """
    Retorna a média das avaliações por tipo
    """
    return Avaliacao.objects.values('tipoAvaliacao').annotate(
        media=Avg('nota')
    ).order_by('tipoAvaliacao')

def media_avaliacao_por_atendente():
    """
    Retorna a média das avaliações por atendente
    """
    return Avaliacao.objects.values('chamado__atendente__nome').annotate(
        media=Avg('nota'),
        atendente_nome=F('chamado__atendente__nome'),
        total_avaliacoes=Count('id')
    ).order_by('-media')

def media_tempo_resolucao():
    """
    Retorna o tempo médio de resolução dos chamados (em horas)
    """
    chamados_fechados = Chamado.objects.filter(
        status='fechado', 
        dataFechamento__isnull=False
    )
    
    total_horas = 0
    total_chamados = 0
    
    for chamado in chamados_fechados:
        # Calcula a diferença em horas
        delta = chamado.dataFechamento - chamado.dataAbertura
        horas = delta.total_seconds() / 3600
        total_horas += horas
        total_chamados += 1
    
    if total_chamados > 0:
        return total_horas / total_chamados
    return 0

def chamados_abertos_periodo(dias=30):
    """
    Retorna a quantidade de chamados abertos no período especificado
    """
    data_inicio = timezone.now() - timedelta(days=dias)
    return Chamado.objects.filter(dataAbertura__gte=data_inicio).count()

def chamados_fechados_periodo(dias=30):
    """
    Retorna a quantidade de chamados fechados no período especificado
    """
    data_inicio = timezone.now() - timedelta(days=dias)
    return Chamado.objects.filter(
        dataFechamento__isnull=False,
        dataFechamento__gte=data_inicio
    ).count()

def desempenho_atendentes():
    """
    Retorna estatísticas de desempenho dos atendentes
    """
    return Atendente.objects.annotate(
        total_chamados=Count('chamados'),
        chamados_resolvidos=Count('chamados', filter=Q(chamados__status='resolvido') | Q(chamados__status='fechado')),
        avaliacao_media=Avg('chamados__avaliacao__nota')
    ).values('id', 'nome', 'departamento__nome', 'total_chamados', 'chamados_resolvidos', 'avaliacao_media')

def resumo_estatisticas():
    """
    Retorna um resumo geral das estatísticas
    """
    total_chamados = Chamado.objects.count()
    chamados_abertos = Chamado.objects.filter(status='aberto').count()
    chamados_andamento = Chamado.objects.filter(status='em_andamento').count()
    chamados_resolvidos = Chamado.objects.filter(status='resolvido').count()
    chamados_fechados = Chamado.objects.filter(status='fechado').count()
    
    avaliacao_media = Avaliacao.objects.aggregate(media=Avg('nota'))['media'] or 0
    
    return {
        'total_chamados': total_chamados,
        'chamados_abertos': chamados_abertos,
        'chamados_andamento': chamados_andamento,
        'chamados_resolvidos': chamados_resolvidos,
        'chamados_fechados': chamados_fechados,
        'avaliacao_media': avaliacao_media,
        'tempo_medio_resolucao': media_tempo_resolucao()
    } 
from .models import Historico, Chamado

def registrar_acao(chamado, acao, usuario, detalhes):
    """
    Registra uma ação no histórico de um chamado
    
    Args:
        chamado: Objeto do modelo Chamado ou ID do chamado
        acao: String descrevendo a ação realizada
        usuario: Nome do usuário que realizou a ação
        detalhes: Detalhes adicionais sobre a ação
    """
    if isinstance(chamado, int):
        try:
            chamado = Chamado.objects.get(pk=chamado)
        except Chamado.DoesNotExist:
            return None
    
    return Historico.objects.create(
        chamado=chamado,
        acao=acao,
        usuario=usuario,
        detalhes=detalhes
    )

def obter_historico_chamado(chamado_id):
    """
    Retorna o histórico completo de um chamado, ordenado por data
    
    Args:
        chamado_id: ID do chamado
    
    Returns:
        QuerySet com os registros do histórico
    """
    return Historico.objects.filter(chamado_id=chamado_id).order_by('dataAcao')

def registrar_abertura_chamado(chamado, usuario):
    """
    Registra a abertura de um novo chamado
    """
    return registrar_acao(
        chamado=chamado,
        acao="Abertura de chamado",
        usuario=usuario,
        detalhes=f"Chamado aberto por {usuario}"
    )

def registrar_atualizacao_status(chamado, status_anterior, status_novo, usuario):
    """
    Registra a atualização de status de um chamado
    """
    return registrar_acao(
        chamado=chamado,
        acao="Atualização de status",
        usuario=usuario,
        detalhes=f"Status alterado de {status_anterior} para {status_novo}"
    )

def registrar_atribuicao_atendente(chamado, atendente, usuario):
    """
    Registra a atribuição de um atendente a um chamado
    """
    return registrar_acao(
        chamado=chamado,
        acao="Atribuição de atendente",
        usuario=usuario,
        detalhes=f"Chamado atribuído ao atendente {atendente.nome}"
    )

def registrar_solucao(chamado, solucao, usuario):
    """
    Registra a adição de uma solução a um chamado
    """
    return registrar_acao(
        chamado=chamado,
        acao="Solução registrada",
        usuario=usuario,
        detalhes=f"Solução registrada por {usuario}"
    )

def registrar_avaliacao(chamado, avaliacao, usuario):
    """
    Registra a avaliação de um chamado
    """
    return registrar_acao(
        chamado=chamado,
        acao="Avaliação registrada",
        usuario=usuario,
        detalhes=f"Avaliação com nota {avaliacao.nota} registrada"
    )

def registrar_fechamento(chamado, usuario):
    """
    Registra o fechamento de um chamado
    """
    return registrar_acao(
        chamado=chamado,
        acao="Fechamento de chamado",
        usuario=usuario,
        detalhes=f"Chamado fechado por {usuario}"
    ) 
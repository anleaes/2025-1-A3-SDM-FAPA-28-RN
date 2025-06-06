# Sistema de Atendimento ao Cliente
## Projeto de API REST com Django e Django REST Framework

### Desenvolvido por: guihzzy

---

## Agenda

1. Visão Geral do Projeto
2. Diagrama de Classes
3. Arquitetura
4. Modelos Implementados
5. API REST
6. Funcionalidades Especiais
7. Demonstração
8. Próximos Passos

---

## 1. Visão Geral do Projeto

- **Objetivo**: Sistema completo de atendimento ao cliente
- **Funcionalidades principais**:
  - Gerenciamento de chamados técnicos
  - Registro de clientes e atendentes
  - Categorização de problemas
  - Fluxo completo de atendimento
  - Avaliação de atendimento
  - Histórico detalhado

---

## 2. Diagrama de Classes

- **8 Classes Principais**:
  - Cliente
  - Atendente
  - Departamento
  - Categoria
  - Chamado
  - Solução
  - Avaliação
  - Histórico

- **Relacionamentos**:
  - Um-para-Muitos (Cliente → Chamados)
  - Muitos-para-Muitos (implementados via relações intermediárias)

---

## 3. Arquitetura

- **Backend**: Django 5.2 + Django REST Framework
- **Banco de Dados**: SQLite (desenvolvimento)
- **Padrão**: MVC (Model-View-Controller)
- **Organização**:
  - Models: Estrutura de dados
  - Views: Endpoints da API
  - Serializers: Conversão de dados
  - URLs: Rotas de acesso

---

## 4. Modelos Implementados

### Cliente
- Dados pessoais e contato
- Histórico de chamados

### Atendente
- Vinculado a um departamento
- Nível de acesso
- Chamados atendidos

### Chamado
- Status (aberto, em andamento, resolvido, fechado)
- Prioridade (baixa, média, alta, crítica)
- Vinculado a cliente, categoria e atendente

---

## 5. API REST

### Endpoints Principais
- `/api/clientes/`
- `/api/atendentes/`
- `/api/chamados/`
- `/api/categorias/`
- `/api/solucoes/`
- `/api/avaliacoes/`
- `/api/historicos/`

### Estatísticas
- `/api/estatisticas/`
- Múltiplos endpoints para relatórios específicos

---

## 6. Funcionalidades Especiais

### Módulo de Histórico
- Registro automático de todas as ações
- Rastreabilidade completa do atendimento

### Estatísticas Avançadas
- Desempenho por atendente
- Tempo médio de resolução
- Avaliações por departamento

### Fluxo de Trabalho Automatizado
- Registro de histórico
- Atualização de status
- Notificações

---

## 7. Demonstração

### Acesso ao Sistema
- URL: http://127.0.0.1:8000/admin/
- Credenciais: admin / admin

### API Navegável
- URL: http://127.0.0.1:8000/api/
- Endpoints interativos com documentação

### Exemplos de Uso
- Criação de chamados
- Atribuição a atendentes
- Resolução e avaliação

---

## 8. Próximos Passos

### Frontend em React Native
- Interfaces para clientes e atendentes
- Suporte offline
- Notificações push

### Melhorias na API
- Autenticação JWT
- Permissões granulares
- Otimizações de desempenho

### Infraestrutura
- Migração para PostgreSQL
- Implantação em nuvem
- CI/CD

---

## Perguntas?

Obrigado pela atenção!

### Desenvolvido por: guihzzy

---

## Apêndice: Detalhes Técnicos

### Modelos
```python
class Chamado(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    prioridade = models.CharField(max_length=20, choices=PRIORIDADE_CHOICES)
    # ... outros campos
```

### Endpoints
```python
@action(detail=True, methods=['post'])
def atualizar_status(self, request, pk=None):
    chamado = self.get_object()
    status_novo = request.data.get('status')
    # ... lógica de atualização
    return Response({'status': 'Status atualizado com sucesso'})
``` 
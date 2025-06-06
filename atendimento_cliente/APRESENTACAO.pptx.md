# Sistema de Atendimento ao Cliente

### Aplicativo de Serviço de Atendimento ao Cliente
#### API REST com Django e Django REST Framework

#### Desenvolvido por: guihzzy

---

# Agenda

1. Visão Geral do Projeto
2. Diagrama de Classes
3. Arquitetura
4. Modelos Implementados
5. API REST
6. Funcionalidades Especiais
7. Demonstração
8. Próximos Passos

---

# 1. Visão Geral do Projeto

### Objetivo
Sistema completo para gerenciamento de chamados de atendimento ao cliente

### Funcionalidades Principais
- Gerenciamento de chamados técnicos
- Registro de clientes e atendentes
- Categorização de problemas
- Fluxo completo de atendimento
- Avaliação de serviço
- Histórico detalhado de ações

---

# Requisitos do Projeto

### Características Implementadas
- 8 classes com mínimo de 4 atributos cada
- Relacionamentos "Um para Muitos"
- Relacionamentos "Muitos para Muitos"
- Conceito similar a "Carrinho de compras" (fluxo de chamados)
- API REST com Django e Django REST Framework
- Persistência em banco de dados
- Versionamento com Git (branches por feature)

---

# 2. Diagrama de Classes

### 8 Classes Principais

- **Cliente**: Usuário que abre chamados
- **Atendente**: Funcionário que atende chamados
- **Departamento**: Setor responsável pelo atendimento
- **Categoria**: Tipo de problema/solicitação
- **Chamado**: Solicitação aberta pelo cliente
- **Solução**: Resolução aplicada ao chamado
- **Avaliação**: Feedback do cliente sobre o atendimento
- **Histórico**: Registro de todas as ações realizadas

---

# Relacionamentos do Sistema

### Principais Relações
- **Cliente** → **Chamados**: Um cliente pode ter múltiplos chamados
- **Departamento** → **Atendentes**: Um departamento possui vários atendentes
- **Departamento** → **Categorias**: Um departamento gerencia várias categorias
- **Categoria** → **Chamados**: Uma categoria classifica vários chamados
- **Chamado** → **Soluções**: Um chamado pode ter várias soluções
- **Chamado** → **Avaliação**: Um chamado pode ter uma avaliação
- **Chamado** → **Históricos**: Um chamado possui registro completo de ações

---

# 3. Arquitetura

### Tecnologias
- **Backend**: Django 5.2 + Django REST Framework
- **Banco de Dados**: SQLite (desenvolvimento)
- **Padrão**: MVC (Model-View-Controller)
- **Linguagem**: Python

### Organização do Código
- **Models**: Estrutura de dados (ORM)
- **Views**: Endpoints da API (ViewSets)
- **Serializers**: Conversão JSON ↔ Python
- **URLs**: Rotas de acesso à API

---

# Estrutura do Projeto

```
atendimento_cliente/
├── api/                  # Aplicação principal
│   ├── management/       # Comandos personalizados
│   ├── migrations/       # Migrações do banco de dados
│   ├── admin.py          # Configuração do admin
│   ├── estatisticas.py   # Funções para estatísticas
│   ├── historico.py      # Funções para registro de histórico
│   ├── models.py         # Modelos de dados
│   ├── serializers.py    # Serializadores para API
│   ├── urls.py           # Rotas da API
│   └── views.py          # Views e endpoints
├── core/                 # Configurações do projeto
└── manage.py             # Script de gerenciamento
```

---

# 4. Modelos Implementados

### Cliente
```python
class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
    endereco = models.TextField()
    dataCadastro = models.DateTimeField(default=timezone.now)
```

### Atendente
```python
class Atendente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    nivelAcesso = models.IntegerField()
    dataContratacao = models.DateTimeField(default=timezone.now)
```

---

# Modelos Implementados (cont.)

### Chamado
```python
class Chamado(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    prioridade = models.CharField(max_length=20, choices=PRIORIDADE_CHOICES)
    dataAbertura = models.DateTimeField(default=timezone.now)
    dataFechamento = models.DateTimeField(null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    atendente = models.ForeignKey(Atendente, on_delete=models.SET_NULL, null=True)
```

---

# Modelos Implementados (cont.)

### Ciclo de Vida de um Chamado

1. **Abertura**: Cliente abre um chamado (status: aberto)
2. **Atribuição**: Atendente assume o chamado (status: em_andamento)
3. **Resolução**: Atendente registra solução (status: resolvido)
4. **Avaliação**: Cliente avalia o atendimento
5. **Fechamento**: Chamado é encerrado (status: fechado)

---

# 5. API REST

### Endpoints Principais

- `/api/clientes/`: Gerenciamento de clientes
- `/api/atendentes/`: Gerenciamento de atendentes
- `/api/departamentos/`: Gerenciamento de departamentos
- `/api/categorias/`: Gerenciamento de categorias
- `/api/chamados/`: Gerenciamento de chamados
- `/api/solucoes/`: Gerenciamento de soluções
- `/api/avaliacoes/`: Gerenciamento de avaliações
- `/api/historicos/`: Consulta de históricos

---

# API REST - Ações Especiais

### Ações Customizadas
- `/api/chamados/{id}/atualizar_status/`: Atualiza status do chamado
- `/api/chamados/{id}/solucoes/`: Lista soluções de um chamado
- `/api/chamados/{id}/historico/`: Lista histórico de um chamado
- `/api/atendentes/{id}/atender_chamado/`: Atendente assume chamado
- `/api/clientes/{id}/chamados/`: Lista chamados de um cliente

### Estatísticas
- `/api/estatisticas/`: Resumo geral de estatísticas
- `/api/estatisticas/por-status/`: Contagem por status
- `/api/estatisticas/avaliacao-media/`: Média de avaliações

---

# 6. Funcionalidades Especiais

### Módulo de Histórico
- Registro automático de todas as ações realizadas
- Rastreabilidade completa do atendimento
- Auditoria de mudanças

### Exemplo de código
```python
# Registro de atribuição de atendente
def registrar_atribuicao_atendente(chamado, atendente, usuario):
    return registrar_acao(
        chamado=chamado,
        acao="Atribuição de atendente",
        usuario=usuario,
        detalhes=f"Chamado atribuído ao atendente {atendente.nome}"
    )
```

---

# Funcionalidades Especiais (cont.)

### Estatísticas Avançadas
- Desempenho por atendente
- Tempo médio de resolução por categoria
- Distribuição de chamados por departamento
- Avaliações médias por tipo de atendimento

### Fluxo de Trabalho Automatizado
- Registro de histórico automático
- Atualização de status com validações
- Cálculo de métricas em tempo real

---

# 7. Demonstração

### Acesso ao Sistema Administrativo
- URL: http://127.0.0.1:8000/admin/
- Usuário: admin
- Senha: admin

### API Navegável
- URL: http://127.0.0.1:8000/api/
- Endpoints interativos com documentação
- Possibilidade de testar todos os endpoints

---

# Demonstração - Fluxo de Atendimento

### Exemplo Prático
1. Cliente abre um chamado via API
2. Sistema registra o chamado e cria histórico
3. Atendente assume o chamado
4. Atendente registra solução
5. Cliente avalia o atendimento
6. Chamado é fechado automaticamente
7. Estatísticas são atualizadas

---

# 8. Próximos Passos

### Frontend em React Native
- Interfaces para clientes e atendentes
- Suporte offline
- Notificações push

### Melhorias na API
- Autenticação JWT
- Permissões granulares
- Filtros avançados

### Infraestrutura
- Migração para PostgreSQL
- Implantação em nuvem
- CI/CD para testes e deploy

---

# Metodologia de Desenvolvimento

### Branches Git por Funcionalidade
- Branch para Models
- Branch para Views
- Branch para URLs
- Branch para Serializers

### Comandos Personalizados
- `populate_db`: Popula o banco com dados de exemplo
- Facilita testes e demonstrações

---

# Conclusão

### Projeto Completo
- Implementação de todas as 8 classes do diagrama
- API REST funcional e bem estruturada
- Documentação completa

### Diferenciais
- Módulo de histórico detalhado
- Sistema de estatísticas avançadas
- Fluxo de trabalho automatizado

---

# Obrigado!

### Perguntas?

#### Projeto desenvolvido por: guihzzy

---

# Apêndice: Exemplos de Código

### Endpoint para Atualizar Status
```python
@action(detail=True, methods=['post'])
def atualizar_status(self, request, pk=None):
    chamado = self.get_object()
    status_anterior = chamado.status
    status_novo = request.data.get('status')
    usuario = request.data.get('usuario', 'Sistema')
    
    chamado.status = status_novo
    
    if status_novo == 'fechado':
        chamado.dataFechamento = timezone.now()
    
    chamado.save()
    registrar_atualizacao_status(chamado, status_anterior, status_novo, usuario)
    
    return Response({'status': 'Status atualizado com sucesso'})
``` 
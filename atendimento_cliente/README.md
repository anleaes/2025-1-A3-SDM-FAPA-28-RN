# Documentação do Sistema de Atendimento ao Cliente

### Desenvolvido por: guihzzy

## 1. Visão Geral

Este projeto implementa um sistema completo de atendimento ao cliente usando Django e Django REST Framework. O sistema permite gerenciar chamados de suporte, clientes, atendentes e todo o fluxo de atendimento, desde a abertura até a resolução e avaliação.

## 2. Estrutura do Projeto

O projeto está organizado da seguinte forma:

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
│   ├── settings.py       # Configurações do Django
│   ├── urls.py           # Rotas principais
│   ├── wsgi.py           # Configuração WSGI
│   └── asgi.py           # Configuração ASGI
└── manage.py             # Script de gerenciamento
```

## 3. Modelos de Dados

O sistema é composto por 8 modelos principais que representam as entidades do negócio:

### 3.1 Cliente
Representa os usuários que abrem chamados no sistema.

**Atributos:**
- `id`: Identificador único
- `nome`: Nome completo do cliente
- `email`: Email para contato (único)
- `telefone`: Número de telefone
- `endereco`: Endereço completo
- `dataCadastro`: Data de cadastro no sistema

### 3.2 Departamento
Representa as diferentes áreas da empresa responsáveis pelo atendimento.

**Atributos:**
- `id`: Identificador único
- `nome`: Nome do departamento
- `responsavel`: Nome do responsável pelo departamento
- `email`: Email de contato do departamento
- `telefone`: Telefone do departamento
- `horarioFuncionamento`: Horário de funcionamento

### 3.3 Atendente
Representa os funcionários que atendem os chamados.

**Atributos:**
- `id`: Identificador único
- `nome`: Nome do atendente
- `email`: Email para contato (único)
- `departamento`: Departamento ao qual pertence (chave estrangeira)
- `nivelAcesso`: Nível de acesso do atendente
- `dataContratacao`: Data de contratação

### 3.4 Categoria
Representa os tipos de chamados que podem ser abertos.

**Atributos:**
- `id`: Identificador único
- `nome`: Nome da categoria
- `descricao`: Descrição detalhada
- `tempoResposta`: Tempo esperado para resposta (em horas)
- `departamentoResponsavel`: Departamento responsável (chave estrangeira)

### 3.5 Chamado
Representa um chamado aberto por um cliente.

**Atributos:**
- `id`: Identificador único
- `titulo`: Título do chamado
- `descricao`: Descrição detalhada do problema
- `status`: Status atual (aberto, em_andamento, aguardando, resolvido, fechado)
- `prioridade`: Nível de prioridade (baixa, media, alta, critica)
- `dataAbertura`: Data de abertura do chamado
- `dataFechamento`: Data de fechamento (se aplicável)
- `cliente`: Cliente que abriu o chamado (chave estrangeira)
- `categoria`: Categoria do chamado (chave estrangeira)
- `atendente`: Atendente responsável (chave estrangeira, opcional)

### 3.6 Solucao
Representa a solução aplicada a um chamado.

**Atributos:**
- `id`: Identificador único
- `descricao`: Descrição da solução
- `passos`: Passos detalhados para resolução
- `dataCriacao`: Data de registro da solução
- `autor`: Nome do autor da solução
- `chamado`: Chamado relacionado (chave estrangeira)

### 3.7 Avaliacao
Representa a avaliação do cliente sobre o atendimento/solução.

**Atributos:**
- `id`: Identificador único
- `nota`: Nota de avaliação (1 a 5)
- `comentario`: Comentário opcional
- `dataAvaliacao`: Data da avaliação
- `tipoAvaliacao`: Tipo (atendimento ou solucao)
- `chamado`: Chamado avaliado (chave estrangeira)

### 3.8 Historico
Registra todas as ações realizadas em um chamado.

**Atributos:**
- `id`: Identificador único
- `acao`: Descrição da ação realizada
- `dataAcao`: Data e hora da ação
- `usuario`: Usuário que realizou a ação
- `detalhes`: Detalhes adicionais
- `chamado`: Chamado relacionado (chave estrangeira)

## 4. API REST

A API REST fornece acesso completo a todas as funcionalidades do sistema.

### 4.1 Endpoints Principais

#### Clientes
- `GET /api/clientes/`: Lista todos os clientes
- `POST /api/clientes/`: Cria um novo cliente
- `GET /api/clientes/{id}/`: Detalhes de um cliente
- `PUT /api/clientes/{id}/`: Atualiza um cliente
- `DELETE /api/clientes/{id}/`: Remove um cliente
- `GET /api/clientes/{id}/chamados/`: Lista chamados de um cliente

#### Atendentes
- `GET /api/atendentes/`: Lista todos os atendentes
- `POST /api/atendentes/`: Cria um novo atendente
- `GET /api/atendentes/{id}/`: Detalhes de um atendente
- `PUT /api/atendentes/{id}/`: Atualiza um atendente
- `DELETE /api/atendentes/{id}/`: Remove um atendente
- `GET /api/atendentes/{id}/chamados/`: Lista chamados de um atendente
- `POST /api/atendentes/{id}/atender_chamado/`: Atendente assume um chamado

#### Departamentos
- `GET /api/departamentos/`: Lista todos os departamentos
- `POST /api/departamentos/`: Cria um novo departamento
- `GET /api/departamentos/{id}/`: Detalhes de um departamento
- `PUT /api/departamentos/{id}/`: Atualiza um departamento
- `DELETE /api/departamentos/{id}/`: Remove um departamento
- `GET /api/departamentos/{id}/atendentes/`: Lista atendentes de um departamento
- `GET /api/departamentos/{id}/categorias/`: Lista categorias de um departamento

#### Categorias
- `GET /api/categorias/`: Lista todas as categorias
- `POST /api/categorias/`: Cria uma nova categoria
- `GET /api/categorias/{id}/`: Detalhes de uma categoria
- `PUT /api/categorias/{id}/`: Atualiza uma categoria
- `DELETE /api/categorias/{id}/`: Remove uma categoria
- `GET /api/categorias/{id}/chamados/`: Lista chamados de uma categoria

#### Chamados
- `GET /api/chamados/`: Lista todos os chamados
- `POST /api/chamados/`: Cria um novo chamado
- `GET /api/chamados/{id}/`: Detalhes de um chamado
- `PUT /api/chamados/{id}/`: Atualiza um chamado
- `DELETE /api/chamados/{id}/`: Remove um chamado
- `POST /api/chamados/{id}/atualizar_status/`: Atualiza o status de um chamado
- `GET /api/chamados/{id}/solucoes/`: Lista soluções de um chamado
- `GET /api/chamados/{id}/historico/`: Lista histórico de um chamado

#### Soluções
- `GET /api/solucoes/`: Lista todas as soluções
- `POST /api/solucoes/`: Cria uma nova solução
- `GET /api/solucoes/{id}/`: Detalhes de uma solução
- `PUT /api/solucoes/{id}/`: Atualiza uma solução
- `DELETE /api/solucoes/{id}/`: Remove uma solução

#### Avaliações
- `GET /api/avaliacoes/`: Lista todas as avaliações
- `POST /api/avaliacoes/`: Cria uma nova avaliação
- `GET /api/avaliacoes/{id}/`: Detalhes de uma avaliação
- `PUT /api/avaliacoes/{id}/`: Atualiza uma avaliação
- `DELETE /api/avaliacoes/{id}/`: Remove uma avaliação

#### Histórico
- `GET /api/historicos/`: Lista todos os registros de histórico
- `GET /api/historicos/{id}/`: Detalhes de um registro de histórico
- `GET /api/historicos/?chamado={id}`: Filtra histórico por chamado

### 4.2 Endpoints de Estatísticas

- `GET /api/estatisticas/`: Resumo geral das estatísticas
- `GET /api/estatisticas/resumo/`: Resumo detalhado
- `GET /api/estatisticas/por-status/`: Contagem de chamados por status
- `GET /api/estatisticas/por-prioridade/`: Contagem de chamados por prioridade
- `GET /api/estatisticas/por-categoria/`: Contagem de chamados por categoria
- `GET /api/estatisticas/por-departamento/`: Contagem de chamados por departamento
- `GET /api/estatisticas/avaliacao-media/`: Média geral das avaliações
- `GET /api/estatisticas/avaliacao-por-atendente/`: Média das avaliações por atendente
- `GET /api/estatisticas/tempo-resolucao/`: Tempo médio de resolução

## 5. Módulos Utilitários

### 5.1 Módulo de Histórico

O módulo `historico.py` fornece funções para registrar todas as ações realizadas nos chamados:

- `registrar_acao()`: Registra uma ação genérica
- `registrar_abertura_chamado()`: Registra a abertura de um chamado
- `registrar_atualizacao_status()`: Registra a atualização de status
- `registrar_atribuicao_atendente()`: Registra a atribuição de um atendente
- `registrar_solucao()`: Registra o registro de uma solução
- `registrar_avaliacao()`: Registra a avaliação de um chamado
- `registrar_fechamento()`: Registra o fechamento de um chamado

### 5.2 Módulo de Estatísticas

O módulo `estatisticas.py` fornece funções para gerar relatórios e análises:

- `chamados_por_status()`: Contagem de chamados por status
- `chamados_por_prioridade()`: Contagem de chamados por prioridade
- `chamados_por_categoria()`: Contagem de chamados por categoria
- `chamados_por_departamento()`: Contagem de chamados por departamento
- `media_avaliacao_geral()`: Média geral das avaliações
- `media_avaliacao_por_tipo()`: Média das avaliações por tipo
- `media_avaliacao_por_atendente()`: Média das avaliações por atendente
- `media_tempo_resolucao()`: Tempo médio de resolução dos chamados
- `desempenho_atendentes()`: Estatísticas de desempenho dos atendentes
- `resumo_estatisticas()`: Resumo geral das estatísticas

## 6. Comandos Personalizados

### 6.1 Povoamento do Banco de Dados

O comando `populate_db` popula o banco de dados com dados de exemplo:

```bash
python manage.py populate_db
```

Este comando cria:
- 3 departamentos
- 4 atendentes
- 4 categorias
- 5 clientes
- 8 chamados com diferentes status
- Soluções e avaliações para alguns chamados
- Registros de histórico para todas as ações

## 7. Fluxo de Trabalho

### 7.1 Ciclo de Vida de um Chamado

1. **Abertura**: Cliente abre um chamado, escolhendo uma categoria
2. **Atribuição**: Um atendente assume o chamado (status muda para "em_andamento")
3. **Resolução**: Atendente registra uma solução (status muda para "resolvido")
4. **Avaliação**: Cliente avalia o atendimento/solução
5. **Fechamento**: Chamado é fechado (status muda para "fechado")

### 7.2 Relacionamentos Principais

- Um cliente pode ter vários chamados
- Um departamento pode ter vários atendentes
- Um departamento pode ser responsável por várias categorias
- Um chamado pertence a uma categoria e pode ter várias soluções
- Um chamado tem um histórico completo de ações

## 8. Autenticação e Segurança

O sistema utiliza a autenticação padrão do Django. Para acessar a interface administrativa:

- **URL**: http://127.0.0.1:8000/admin/
- **Usuário**: admin
- **Senha**: admin

A API utiliza autenticação básica através do endpoint:
- `api-auth/`: Fornece login/logout para a API

## 9. Tecnologias Utilizadas

- **Backend**: Django 5.2, Django REST Framework
- **Banco de Dados**: SQLite (padrão)
- **Linguagem**: Python

## 10. Próximos Passos

Para expandir o projeto, considere:

1. Implementação do frontend em React Native
2. Adição de autenticação JWT para a API
3. Implementação de permissões mais granulares
4. Adição de funcionalidades como notificações e relatórios avançados
5. Implementação de testes automatizados
6. Configuração para deploy em produção

## 11. Como Executar o Projeto

1. Certifique-se de ter Python instalado
2. Clone o repositório
3. Instale as dependências: `pip install django djangorestframework`
4. Execute as migrações: `python manage.py migrate`
5. Crie um superusuário: `python manage.py createsuperuser`
6. Popule o banco com dados de exemplo: `python manage.py populate_db`
7. Inicie o servidor: `python manage.py runserver`
8. Acesse: http://127.0.0.1:8000/api/ ou http://127.0.0.1:8000/admin/

---

Este documento serve como referência para entender a estrutura e funcionamento do Sistema de Atendimento ao Cliente, implementado de acordo com o diagrama de classes fornecido. 
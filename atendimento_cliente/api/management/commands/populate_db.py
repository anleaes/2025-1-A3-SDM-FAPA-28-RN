from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import Cliente, Atendente, Chamado, Categoria, Avaliacao, Solucao, Historico, Departamento
from api.historico import registrar_abertura_chamado, registrar_atribuicao_atendente, registrar_atualizacao_status, registrar_solucao, registrar_avaliacao
import random
from datetime import timedelta

class Command(BaseCommand):
    help = 'Popula o banco de dados com dados de exemplo'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populando banco de dados...')
        
        # Limpar dados existentes
        self.stdout.write('Removendo dados existentes...')
        Historico.objects.all().delete()
        Avaliacao.objects.all().delete()
        Solucao.objects.all().delete()
        Chamado.objects.all().delete()
        Categoria.objects.all().delete()
        Atendente.objects.all().delete()
        Departamento.objects.all().delete()
        Cliente.objects.all().delete()
        
        # Criar departamentos
        self.stdout.write('Criando departamentos...')
        departamentos = []
        
        departamentos.append(Departamento.objects.create(
            nome='Suporte Técnico',
            responsavel='Carlos Silva',
            email='suporte@empresa.com',
            telefone='(11) 3333-1111',
            horarioFuncionamento='Segunda a Sexta, 8h às 18h'
        ))
        
        departamentos.append(Departamento.objects.create(
            nome='Financeiro',
            responsavel='Maria Oliveira',
            email='financeiro@empresa.com',
            telefone='(11) 3333-2222',
            horarioFuncionamento='Segunda a Sexta, 9h às 17h'
        ))
        
        departamentos.append(Departamento.objects.create(
            nome='Comercial',
            responsavel='João Pereira',
            email='comercial@empresa.com',
            telefone='(11) 3333-3333',
            horarioFuncionamento='Segunda a Sábado, 8h às 20h'
        ))
        
        # Criar atendentes
        self.stdout.write('Criando atendentes...')
        atendentes = []
        
        atendentes.append(Atendente.objects.create(
            nome='Pedro Souza',
            email='pedro@empresa.com',
            departamento=departamentos[0],
            nivelAcesso=2,
            dataContratacao=timezone.now() - timedelta(days=365)
        ))
        
        atendentes.append(Atendente.objects.create(
            nome='Ana Lima',
            email='ana@empresa.com',
            departamento=departamentos[0],
            nivelAcesso=1,
            dataContratacao=timezone.now() - timedelta(days=180)
        ))
        
        atendentes.append(Atendente.objects.create(
            nome='Roberto Santos',
            email='roberto@empresa.com',
            departamento=departamentos[1],
            nivelAcesso=2,
            dataContratacao=timezone.now() - timedelta(days=730)
        ))
        
        atendentes.append(Atendente.objects.create(
            nome='Julia Costa',
            email='julia@empresa.com',
            departamento=departamentos[2],
            nivelAcesso=1,
            dataContratacao=timezone.now() - timedelta(days=90)
        ))
        
        # Criar categorias
        self.stdout.write('Criando categorias...')
        categorias = []
        
        categorias.append(Categoria.objects.create(
            nome='Problema Técnico',
            descricao='Problemas relacionados a falhas técnicas nos sistemas',
            tempoResposta=4,
            departamentoResponsavel=departamentos[0]
        ))
        
        categorias.append(Categoria.objects.create(
            nome='Dúvida sobre produto',
            descricao='Dúvidas sobre o funcionamento dos produtos',
            tempoResposta=8,
            departamentoResponsavel=departamentos[2]
        ))
        
        categorias.append(Categoria.objects.create(
            nome='Problema de cobrança',
            descricao='Problemas relacionados a cobranças e pagamentos',
            tempoResposta=24,
            departamentoResponsavel=departamentos[1]
        ))
        
        categorias.append(Categoria.objects.create(
            nome='Bug no sistema',
            descricao='Erros e falhas no funcionamento do sistema',
            tempoResposta=2,
            departamentoResponsavel=departamentos[0]
        ))
        
        # Criar clientes
        self.stdout.write('Criando clientes...')
        clientes = []
        
        clientes.append(Cliente.objects.create(
            nome='Marcos Oliveira',
            email='marcos@cliente.com',
            telefone='(11) 99999-1111',
            endereco='Rua das Flores, 123, São Paulo - SP',
            dataCadastro=timezone.now() - timedelta(days=100)
        ))
        
        clientes.append(Cliente.objects.create(
            nome='Carla Silva',
            email='carla@cliente.com',
            telefone='(11) 99999-2222',
            endereco='Av. Paulista, 1000, São Paulo - SP',
            dataCadastro=timezone.now() - timedelta(days=200)
        ))
        
        clientes.append(Cliente.objects.create(
            nome='Fernando Reis',
            email='fernando@cliente.com',
            telefone='(11) 99999-3333',
            endereco='Rua Augusta, 500, São Paulo - SP',
            dataCadastro=timezone.now() - timedelta(days=150)
        ))
        
        clientes.append(Cliente.objects.create(
            nome='Luciana Martins',
            email='luciana@cliente.com',
            telefone='(11) 99999-4444',
            endereco='Rua Oscar Freire, 200, São Paulo - SP',
            dataCadastro=timezone.now() - timedelta(days=50)
        ))
        
        clientes.append(Cliente.objects.create(
            nome='Ricardo Almeida',
            email='ricardo@cliente.com',
            telefone='(11) 99999-5555',
            endereco='Av. Brasil, 100, Rio de Janeiro - RJ',
            dataCadastro=timezone.now() - timedelta(days=80)
        ))
        
        # Criar chamados
        self.stdout.write('Criando chamados...')
        chamados = []
        
        # Chamado 1 - Aberto
        chamado1 = Chamado.objects.create(
            titulo='Não consigo acessar minha conta',
            descricao='Estou tentando acessar minha conta no sistema, mas aparece erro de autenticação.',
            status='aberto',
            prioridade='media',
            dataAbertura=timezone.now() - timedelta(hours=5),
            cliente=clientes[0],
            categoria=categorias[0]
        )
        registrar_abertura_chamado(chamado1, chamado1.cliente.nome)
        chamados.append(chamado1)
        
        # Chamado 2 - Em andamento
        chamado2 = Chamado.objects.create(
            titulo='Problema com a fatura',
            descricao='Minha fatura veio com um valor incorreto, maior do que deveria ser.',
            status='em_andamento',
            prioridade='alta',
            dataAbertura=timezone.now() - timedelta(days=2, hours=3),
            cliente=clientes[1],
            categoria=categorias[2],
            atendente=atendentes[2]
        )
        registrar_abertura_chamado(chamado2, chamado2.cliente.nome)
        registrar_atribuicao_atendente(chamado2, atendentes[2], 'Sistema')
        registrar_atualizacao_status(chamado2, 'aberto', 'em_andamento', atendentes[2].nome)
        chamados.append(chamado2)
        
        # Chamado 3 - Resolvido
        chamado3 = Chamado.objects.create(
            titulo='Dúvida sobre funcionalidade',
            descricao='Não estou conseguindo encontrar onde fica a opção de exportar relatórios.',
            status='resolvido',
            prioridade='baixa',
            dataAbertura=timezone.now() - timedelta(days=5),
            cliente=clientes[2],
            categoria=categorias[1],
            atendente=atendentes[3]
        )
        registrar_abertura_chamado(chamado3, chamado3.cliente.nome)
        registrar_atribuicao_atendente(chamado3, atendentes[3], 'Sistema')
        registrar_atualizacao_status(chamado3, 'aberto', 'em_andamento', atendentes[3].nome)
        
        solucao3 = Solucao.objects.create(
            descricao='Foi mostrado ao cliente como acessar a funcionalidade',
            passos='1. Acessar o menu Relatórios\n2. Clicar em Exportar\n3. Selecionar o formato desejado',
            dataCriacao=timezone.now() - timedelta(days=4),
            autor=atendentes[3].nome,
            chamado=chamado3
        )
        registrar_solucao(chamado3, solucao3, atendentes[3].nome)
        registrar_atualizacao_status(chamado3, 'em_andamento', 'resolvido', atendentes[3].nome)
        
        avaliacao3 = Avaliacao.objects.create(
            nota=5,
            comentario='Atendente muito atencioso e resolveu meu problema rapidamente.',
            dataAvaliacao=timezone.now() - timedelta(days=3),
            tipoAvaliacao='atendimento',
            chamado=chamado3
        )
        registrar_avaliacao(chamado3, avaliacao3, chamado3.cliente.nome)
        chamados.append(chamado3)
        
        # Chamado 4 - Fechado
        chamado4 = Chamado.objects.create(
            titulo='Bug no cadastro de produtos',
            descricao='Ao tentar cadastrar um novo produto, o sistema trava na validação.',
            status='fechado',
            prioridade='critica',
            dataAbertura=timezone.now() - timedelta(days=10),
            dataFechamento=timezone.now() - timedelta(days=7),
            cliente=clientes[3],
            categoria=categorias[3],
            atendente=atendentes[0]
        )
        registrar_abertura_chamado(chamado4, chamado4.cliente.nome)
        registrar_atribuicao_atendente(chamado4, atendentes[0], 'Sistema')
        registrar_atualizacao_status(chamado4, 'aberto', 'em_andamento', atendentes[0].nome)
        
        solucao4 = Solucao.objects.create(
            descricao='Corrigido bug na validação do formulário',
            passos='1. Identificado o problema na validação\n2. Corrigido o código de validação\n3. Realizado testes para garantir o funcionamento',
            dataCriacao=timezone.now() - timedelta(days=8),
            autor=atendentes[0].nome,
            chamado=chamado4
        )
        registrar_solucao(chamado4, solucao4, atendentes[0].nome)
        registrar_atualizacao_status(chamado4, 'em_andamento', 'resolvido', atendentes[0].nome)
        registrar_atualizacao_status(chamado4, 'resolvido', 'fechado', 'Sistema')
        
        avaliacao4 = Avaliacao.objects.create(
            nota=4,
            comentario='Problema resolvido, mas demorou um pouco.',
            dataAvaliacao=timezone.now() - timedelta(days=7),
            tipoAvaliacao='solucao',
            chamado=chamado4
        )
        registrar_avaliacao(chamado4, avaliacao4, chamado4.cliente.nome)
        chamados.append(chamado4)
        
        # Chamado 5 - Em andamento
        chamado5 = Chamado.objects.create(
            titulo='Sistema lento ao gerar relatórios',
            descricao='O sistema está demorando muito para gerar relatórios de vendas mensais.',
            status='em_andamento',
            prioridade='media',
            dataAbertura=timezone.now() - timedelta(days=1, hours=12),
            cliente=clientes[4],
            categoria=categorias[0],
            atendente=atendentes[1]
        )
        registrar_abertura_chamado(chamado5, chamado5.cliente.nome)
        registrar_atribuicao_atendente(chamado5, atendentes[1], 'Sistema')
        registrar_atualizacao_status(chamado5, 'aberto', 'em_andamento', atendentes[1].nome)
        chamados.append(chamado5)
        
        # Chamado 6 - Aberto
        chamado6 = Chamado.objects.create(
            titulo='Dúvida sobre novo produto',
            descricao='Gostaria de saber mais detalhes sobre a nova versão do produto que foi anunciada.',
            status='aberto',
            prioridade='baixa',
            dataAbertura=timezone.now() - timedelta(hours=1),
            cliente=clientes[2],
            categoria=categorias[1]
        )
        registrar_abertura_chamado(chamado6, chamado6.cliente.nome)
        chamados.append(chamado6)
        
        # Chamado 7 - Resolvido
        chamado7 = Chamado.objects.create(
            titulo='Problema com pagamento',
            descricao='Realizei o pagamento da mensalidade, mas o sistema ainda mostra como pendente.',
            status='resolvido',
            prioridade='alta',
            dataAbertura=timezone.now() - timedelta(days=3, hours=8),
            cliente=clientes[0],
            categoria=categorias[2],
            atendente=atendentes[2]
        )
        registrar_abertura_chamado(chamado7, chamado7.cliente.nome)
        registrar_atribuicao_atendente(chamado7, atendentes[2], 'Sistema')
        registrar_atualizacao_status(chamado7, 'aberto', 'em_andamento', atendentes[2].nome)
        
        solucao7 = Solucao.objects.create(
            descricao='Regularizado status do pagamento no sistema',
            passos='1. Verificado o pagamento no gateway\n2. Confirmado recebimento\n3. Atualizado status no sistema',
            dataCriacao=timezone.now() - timedelta(days=2),
            autor=atendentes[2].nome,
            chamado=chamado7
        )
        registrar_solucao(chamado7, solucao7, atendentes[2].nome)
        registrar_atualizacao_status(chamado7, 'em_andamento', 'resolvido', atendentes[2].nome)
        chamados.append(chamado7)
        
        # Chamado 8 - Fechado
        chamado8 = Chamado.objects.create(
            titulo='Erro ao atualizar cadastro',
            descricao='Não consigo atualizar meu endereço no cadastro, aparece uma mensagem de erro.',
            status='fechado',
            prioridade='media',
            dataAbertura=timezone.now() - timedelta(days=15),
            dataFechamento=timezone.now() - timedelta(days=12),
            cliente=clientes[1],
            categoria=categorias[3],
            atendente=atendentes[0]
        )
        registrar_abertura_chamado(chamado8, chamado8.cliente.nome)
        registrar_atribuicao_atendente(chamado8, atendentes[0], 'Sistema')
        registrar_atualizacao_status(chamado8, 'aberto', 'em_andamento', atendentes[0].nome)
        
        solucao8 = Solucao.objects.create(
            descricao='Corrigido problema na validação de CEP',
            passos='1. Identificado erro na validação de CEP\n2. Corrigido algoritmo de validação\n3. Testado em diferentes cenários',
            dataCriacao=timezone.now() - timedelta(days=13),
            autor=atendentes[0].nome,
            chamado=chamado8
        )
        registrar_solucao(chamado8, solucao8, atendentes[0].nome)
        registrar_atualizacao_status(chamado8, 'em_andamento', 'resolvido', atendentes[0].nome)
        registrar_atualizacao_status(chamado8, 'resolvido', 'fechado', 'Sistema')
        
        avaliacao8 = Avaliacao.objects.create(
            nota=3,
            comentario='Problema resolvido, mas o sistema ainda está um pouco confuso.',
            dataAvaliacao=timezone.now() - timedelta(days=12),
            tipoAvaliacao='solucao',
            chamado=chamado8
        )
        registrar_avaliacao(chamado8, avaliacao8, chamado8.cliente.nome)
        chamados.append(chamado8)
        
        # Finalização
        self.stdout.write(self.style.SUCCESS(f'Banco de dados populado com sucesso!'))
        self.stdout.write(f'Criados {len(departamentos)} departamentos')
        self.stdout.write(f'Criados {len(atendentes)} atendentes')
        self.stdout.write(f'Criadas {len(categorias)} categorias')
        self.stdout.write(f'Criados {len(clientes)} clientes')
        self.stdout.write(f'Criados {len(chamados)} chamados') 
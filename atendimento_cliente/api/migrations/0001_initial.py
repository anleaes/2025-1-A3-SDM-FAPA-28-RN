# Generated by Django 5.2.2 on 2025-06-06 18:38

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Atendente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('nivelAcesso', models.IntegerField()),
                ('dataContratacao', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField()),
                ('tempoResposta', models.IntegerField(help_text='Tempo de resposta em horas')),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('telefone', models.CharField(max_length=20)),
                ('endereco', models.TextField()),
                ('dataCadastro', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('responsavel', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('telefone', models.CharField(max_length=20)),
                ('horarioFuncionamento', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Chamado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('descricao', models.TextField()),
                ('status', models.CharField(choices=[('aberto', 'Aberto'), ('em_andamento', 'Em Andamento'), ('aguardando', 'Aguardando Resposta'), ('resolvido', 'Resolvido'), ('fechado', 'Fechado')], default='aberto', max_length=20)),
                ('prioridade', models.CharField(choices=[('baixa', 'Baixa'), ('media', 'Média'), ('alta', 'Alta'), ('critica', 'Crítica')], default='media', max_length=20)),
                ('dataAbertura', models.DateTimeField(default=django.utils.timezone.now)),
                ('dataFechamento', models.DateTimeField(blank=True, null=True)),
                ('atendente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chamados', to='api.atendente')),
                ('categoria', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chamados', to='api.categoria')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chamados', to='api.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Avaliacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota', models.IntegerField()),
                ('comentario', models.TextField(blank=True)),
                ('dataAvaliacao', models.DateTimeField(default=django.utils.timezone.now)),
                ('tipoAvaliacao', models.CharField(choices=[('atendimento', 'Avaliação do Atendimento'), ('solucao', 'Avaliação da Solução')], max_length=20)),
                ('chamado', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='avaliacao', to='api.chamado')),
            ],
        ),
        migrations.AddField(
            model_name='categoria',
            name='departamentoResponsavel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categorias', to='api.departamento'),
        ),
        migrations.AddField(
            model_name='atendente',
            name='departamento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='atendentes', to='api.departamento'),
        ),
        migrations.CreateModel(
            name='Historico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acao', models.CharField(max_length=100)),
                ('dataAcao', models.DateTimeField(default=django.utils.timezone.now)),
                ('usuario', models.CharField(max_length=100)),
                ('detalhes', models.TextField()),
                ('chamado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historicos', to='api.chamado')),
            ],
        ),
        migrations.CreateModel(
            name='Solucao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.TextField()),
                ('passos', models.TextField()),
                ('dataCriacao', models.DateTimeField(default=django.utils.timezone.now)),
                ('autor', models.CharField(max_length=100)),
                ('chamado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solucoes', to='api.chamado')),
            ],
        ),
    ]

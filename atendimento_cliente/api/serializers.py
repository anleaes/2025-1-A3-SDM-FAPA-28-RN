from rest_framework import serializers
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

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = '__all__'

class AtendenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atendente
        fields = '__all__'
        
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['departamento'] = DepartamentoSerializer(instance.departamento).data
        return response

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'
        
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['departamentoResponsavel'] = DepartamentoSerializer(instance.departamentoResponsavel).data
        return response

class SolucaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solucao
        fields = '__all__'

class AvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaliacao
        fields = '__all__'

class HistoricoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historico
        fields = '__all__'

class ChamadoSerializer(serializers.ModelSerializer):
    solucoes = SolucaoSerializer(many=True, read_only=True)
    historicos = HistoricoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Chamado
        fields = '__all__'
        
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['cliente'] = ClienteSerializer(instance.cliente).data
        if instance.categoria:
            response['categoria'] = CategoriaSerializer(instance.categoria).data
        if instance.atendente:
            response['atendente'] = AtendenteSerializer(instance.atendente).data
        try:
            avaliacao = instance.avaliacao
            response['avaliacao'] = AvaliacaoSerializer(avaliacao).data
        except Avaliacao.DoesNotExist:
            pass
        
        return response 
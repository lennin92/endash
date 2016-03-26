from dashboard.models import Medicion, Nodo
from rest_framework import serializers


class NodoSerializer(serializers.ModelSerializer):
    demandas = serializers.ListField(
        child=serializers.FloatField()
    )
    class Meta:
        model = Nodo
        fields = ('id', 'url', 'padre', 'nombre',
                  'descripcion', 'hijos', 'fotografia', 'demandas')


class MedicionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Medicion
        fields =('nodo', 'fecha_hora', 'energia_activa',
                 'energia_aparente', 'demanda')
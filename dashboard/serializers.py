from dashboard.models import Medicion, Nodo, DemandaNodo
from rest_framework import serializers


class DemandaNodoSerializer(serializers.ModelSerializer):
    fecha_inicio = serializers.DateField()
    fecha_fin = serializers.DateField()
    demanda = serializers.FloatField()

class NodoSerializer(serializers.ModelSerializer):
    demandas = serializers.ListField(
        child=DemandaNodoSerializer()
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
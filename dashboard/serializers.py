from dashboard.models import Medicion, Nodo, DemandaNodo
from rest_framework import serializers


class DemandaNodoSerializer(serializers.Serializer):
    fecha_inicio = serializers.DateTimeField()
    fecha_fin = serializers.DateTimeField()
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
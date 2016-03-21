from dashboard.models import Medicion, Nodo
from rest_framework import serializers


class NodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nodo
        fields = ('url', 'padre', 'nombre', 'descripcion')


class MedicionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Medicion
        fields =('nodo', 'fecha_hora', 'energia_activa',
                 'energia_aparente', 'demanda')
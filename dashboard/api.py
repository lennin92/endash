from dashboard.models import Medicion, Nodo
from rest_framework import viewsets
from dashboard.serializers import MedicionSerializer, NodoSerializer


class NodoViewSet(viewsets.ModelViewSet):
    queryset = Nodo.objects.all()
    serializer_class = NodoSerializer


class MedicionViewSet(viewsets.ModelViewSet):
    queryset = Medicion.objects.all()
    serializer_class = MedicionSerializer
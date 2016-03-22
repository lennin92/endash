from dashboard.models import Medicion, Nodo
from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from dashboard.serializers import MedicionSerializer, NodoSerializer


class NodoViewSet(viewsets.ModelViewSet):
    queryset = Nodo.objects.all()
    serializer_class = NodoSerializer

    # Query only parents nodes
    @list_route()
    def padres(self, request):
        padres = Nodo.objects.filter(padre=None)
        page = self.paginate_queryset(padres)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(padres, many=True)
        return Response(serializer.data)

    # Query childs
    @detail_route(methods=['get'])
    def hijos(self, request, pk=None):
        padre = self.get_object()
        hijos = Nodo.objects.filter(padre=padre)
        page = self.paginate_queryset(hijos)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(hijos, many=True)
        return Response(serializer.data)

class MedicionViewSet(viewsets.ModelViewSet):
    queryset = Medicion.objects.all()
    serializer_class = MedicionSerializer


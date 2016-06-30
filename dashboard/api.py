from dashboard.models import Measure, Node
from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework.permissions import BasePermission
from dashboard.serializers import MedicionSerializer, NodoSerializer
import datetime
from django.db.models import Max


class ReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['get', 'GET']:
            return True


class NodeViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = NodoSerializer

    # Query only parents nodes
    @list_route(permission_classes=[ReadOnly])
    def parents(self, request): pass

    # Query childs
    @detail_route(methods=['get'], permission_classes=[ReadOnly])
    def childs(self, request, pk=None): pass


class MeasureViewSet(viewsets.ModelViewSet):
    queryset = Measure.objects.all()
    serializer_class = MedicionSerializer

    def get_queryset(self):
        begin = self.request.query_params.get('begin', None)
        end = self.request.query_params.get('end', None)
        nodo = self.request.query_params.get('nodo', None)
        if end is None: end = datetime.datetime.now()
        if begin is None: begin = end + datetime.timedelta(-30)
        if nodo is None: queryset = Medicion.objects.filter(fecha_hora__range=(begin,end)).order_by('fecha_hora')
        else: queryset = Medicion.objects.filter(fecha_hora__range=(begin,end), nodo=nodo).order_by('fecha_hora')
        return queryset

    @detail_route(methods=['get'], permission_classes=[ReadOnly])
    def max(self, request, pk=None):
        fh = Medicion.objects.filter(nodo_id=pk).aggregate(Max('fecha_hora'))['fecha_hora__max']
        qs = Medicion.objects.filter(fecha_hora=fh, nodo_id=pk)[0]
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=False)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=False)
        return Response(serializer.data)

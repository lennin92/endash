from dashboard.models import Medicion, Nodo
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

class NodoViewSet(viewsets.ModelViewSet):
    queryset = Nodo.objects.all()
    serializer_class = NodoSerializer

    # Query only parents nodes
    @list_route(permission_classes=[ReadOnly])
    def padres(self, request):
        padres = Nodo.objects.filter(padre=None)
        page = self.paginate_queryset(padres)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(padres, many=True)
        return Response(serializer.data)

    # Query childs
    @detail_route(methods=['get'], permission_classes=[ReadOnly])
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

    def get_queryset(self):
        begin = self.request.query_params.get('begin', None)
        end = self.request.query_params.get('end', None)
        nodo = self.request.query_params.get('nodo', None)
        if end is None: end = datetime.datetime.now()
        if begin is None: begin = end + datetime.timedelta(-30)
        if nodo is None: queryset = Medicion.objects.filter(fecha_hora__range=(begin,end)).order_by('fecha_hora')
        else: queryset = Medicion.objects.filter(fecha_hora__range=(begin,end), nodo=nodo).order_by('fecha_hora')
        return queryset

    # Query childs
    @detail_route(methods=['get'], permission_classes=[ReadOnly])
    def max(self, request, pk=None):
        nodo = self.request.query_params.get('nodo', None)
        if nodo is None:
            fh = Medicion.objects.all().aggregate(Max('fecha_hora'))['fecha_hora__max']
            qs = Medicion.objects.filter(fecha_hora=fh)[0]
        else:
            fh = Medicion.objects.filter(nodo_id=nodo).aggregate(Max('fecha_hora'))['fecha_hora__max']
            qs = Medicion.objects.filter(fecha_hora=fh, nodo_id=nodo)[0]
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=False)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=False)
        return Response(serializer.data)


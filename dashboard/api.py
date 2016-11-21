# -*- coding: utf-8 -*-

from dashboard.models import Measure, Node
from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework.permissions import BasePermission
import datetime
from django.db.models import Max
from dashboard.serializers import NodeSerializer


class ReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['get', 'GET']:
            return True


class NodoViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer

    # Query only parents nodes
    @list_route(permission_classes=[ReadOnly])
    def parents(self, request):
        parents = Node.objects.filter(parent=None)
        page = self.paginate_queryset(parents)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(parents, many=True)
        return Response(serializer.data)

    # Query only parents nodes
    @detail_route(permission_classes=[ReadOnly], methods=['get'])
    def childs(self, request, pk=None):
        childs = Node.objects.filter(parent_id=pk)
        page = self.paginate_queryset(childs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(childs, many=True)
        return Response(serializer.data)

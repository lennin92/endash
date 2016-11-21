# -*- coding: utf-8 -*-
from dashboard.models import Node, Measure, Year, Month, Day, Time
from dashboard.serializers import NodeSerializer, MeasureSerializer
from rest_framework import viewsets, permissions, response as resp
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.conf.urls import url
from django.views.generic import TemplateView
from django.shortcuts import render
from django.conf import settings
from rest_framework.decorators import list_route
import json


class IndexView(TemplateView):
    template_name = 'main.html'
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return render(
            request,
            template_name=self.template_name,
            context={'API_KEY': settings.GEOPOSITION_GOOGLE_MAPS_API_KEY}
        )


class NodeViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def list(self, request, *args, **kwargs):
        queryset = Node.objects.all()
        serializer = NodeSerializer(queryset, many=True)
        return resp.Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Node.objects.all()
        nodes = get_object_or_404(queryset, id=pk)
        serializer = NodeSerializer(nodes)
        return resp.Response(serializer.data)


class MeasuresViewSet(viewsets.ModelViewSet):
    queryset = Measure.objects.all()
    serializer_class = MeasureSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @list_route(methods=['get'])
    def node_detail(self, request, node=None):
        if 'begin' in request.GET:
            begin = request.GET['begin']
            if 'end' not in request.GET:
                return resp.Response(status=status.HTTP_400_BAD_REQUEST)
            end = request.GET['end']
            measures = Measure.objects.filter(node__id=node, datetime_str__range=(begin, end))
        else:
            measures = Measure.objects.filter(node__id=node)
        serializer = MeasureSerializer(measures, many=True)
        return resp.Response(serializer.data)






# Views
node_list = NodeViewSet.as_view({'get': 'list'})
node_detail = NodeViewSet.as_view({'get': 'retrieve'})
measure_list = MeasuresViewSet.as_view({'get': 'node_detail'})

# URLS

urls = [
    url(r'^nodes/$', node_list, name='node_list'),
    url(r'^nodes/(?P<pk>[0-9]+)/$', node_detail, name='node_detail'),
    url(r'^nodes/(?P<node>[0-9]+)/measures$', measure_list, name='measure_list'),
]
# -*- coding: utf-8 -*-
from dashboard.models import Node, Measure, TariffSchedule, Year, Month, Day, Time
from dashboard.serializers import NodeSerializer, MeasureSerializer, TariffScheduleSerializer
from rest_framework import viewsets, permissions, response as resp
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.conf.urls import url
from django.views.generic import TemplateView
from django.shortcuts import render
from django.conf import settings
from rest_framework.decorators import list_route, detail_route
from django.db.models import Max
from rest_framework.response import Response


class IndexView(TemplateView):
    template_name = 'main.html'
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return render(
            request,
            template_name=self.template_name,
            context={'API_KEY': settings.GEOPOSITION_GOOGLE_MAPS_API_KEY}
        )


class TariffScheduleViewSet(viewsets.ModelViewSet):
    queryset = TariffSchedule.objects.all()
    serializer_class = TariffScheduleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @detail_route(methods=['get'])
    def list(self, request, supplier, *args, **kwargs):
        queryset = TariffSchedule.objects.filter(supplier_id=supplier)
        serializer = TariffScheduleSerializer(queryset, many=True)
        return resp.Response(serializer.data)
    

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

    @list_route(methods=['get'])
    def node_detail(self, request, node=None):
        if 'begin' in request.GET:
            begin = request.GET['begin']
            if 'end' not in request.GET:
                return resp.Response(status=status.HTTP_400_BAD_REQUEST)
            end = request.GET['end']
            print(begin,end)
            measures = Measure.objects.filter(node__id=node, datetime_str__range=(begin, end))
        else:
            measures = Measure.objects.filter(node__id=node)
        serializer = MeasureSerializer(measures, many=True)
        return resp.Response(serializer.data)
    
    @detail_route(methods=['get'])
    def last(self, request, node=None):
        fh = Measure.objects.filter(node__id=node).aggregate(Max('datetime_str'))['datetime_str__max']
        qs = Measure.objects.filter(datetime_str=fh, node__id=node)[0]
        serializer = MeasureSerializer(qs, many=False)
        return resp.Response(serializer.data)
    
    @detail_route(methods=['post'])
    def create_measure(self, request, node=None):
        measure = Measure()
        measure.node = Node.objects.get(id=node)
        datetime_str = request.data['datetime_str']
        measure.year = Year.objects.get(year=datetime_str[0:4])
        measure.month = Month.objects.get(char_rep=datetime_str[5:7])
        measure.day = Day.objects.get(char_rep=datetime_str[8:10])
        measure.time = Time.objects.get(char_rep=datetime_str[11:16])
        measure.demand = request.data['demand']
        measure.active = request.data['active']
        measure.apparent = request.data['apparent']
        try:
            measure.save()
        except Exception as e:
            print("ERROR ON SAVING")
        return Response({'status': 'stored'})


# Views
node_list = NodeViewSet.as_view({'get': 'list'})
node_detail = NodeViewSet.as_view({'get': 'retrieve'})
measure_list = MeasuresViewSet.as_view({'get': 'node_detail', 'post':'create_measure'})
# measure_list2 = MeasuresViewSet.as_view({'post':'create_measure'})
measure_last = MeasuresViewSet.as_view({'get': 'last'})
tariffschedule_list = TariffScheduleViewSet.as_view({'get': 'list'})

# URLS

urls = [
    url(r'^nodes/$', node_list, name='node_list'),
    url(r'^nodes/(?P<pk>[0-9]+)/$', node_detail, name='node_detail'),
    url(r'^nodes/(?P<node>[0-9]+)/measures/$', measure_list, name='measure_list'),
    # url(r'^nodes/(?P<node>[0-9]+)/measures/add/$', measure_list2, name='measure_list2'),
    url(r'^nodes/(?P<node>[0-9]+)/measures/last/$', measure_last, name='measure_last'),
    url(r'^tariff_schedule/(?P<supplier>[0-9]+)/$', tariffschedule_list, name='tariffschedule_list'),
    #url(r'^tariff_schedule/$', tariffschedule_list, name='tariffschedule_list'),
]
# -*- coding: utf-8 -*-
from dashboard.models import Measure, Node, TariffSchedule
from rest_framework import serializers


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = (
                'id',
                'parent',
                'supplier',
                'name',
                'description',
                'photography',
                'location'
            )


class MeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measure
        fields = (
            'datetime_str',
            'active',
            'apparent',
            'demand',
            'year_id',
            'month_id',
            'day_id',
            'time_id'
        )


class TariffScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TariffSchedule
        fields = (
            'supplier',
            'valid_from',
            'valid_to',
            'fixed',
            'peak',
            'rest',
            'valley',
            'power'
        )

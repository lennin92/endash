# -*- coding: utf-8 -*-
from dashboard.models import Measure, Node, TariffSchedule, TariffValue, PowerFactorTariff
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
            'time_id',
            'node_id'
        )


class TariffValuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TariffValue
        fields = (
            'supplier',
            'valid_from',
            'valid_to',
            'tariff_values',
            'power_factor_tariff_values'
            'name',
            'consume_begins',
            'consume_ends',
            'is_fixed',
        )


class PowerFactorTariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = PowerFactorTariff
        fields = (
            'max_power_factor',
            'min_power_factor',
            'charge_value',
        )


class TariffScheduleSerializer(serializers.ModelSerializer):
    tariff_values = TariffValuesSerializer(many=True)
    power_factor_tariff_values = PowerFactorTariffSerializer(many=True)

    class Meta:
        model = TariffSchedule
        fields = (
            'supplier',
            'valid_from',
            'valid_to',
            'tariff_values',
            'power_factor_tariff_values'
        )

# -*- coding: utf-8 -*-
from dashboard.models import Measure, Node, TariffSchedule, TariffValue, PowerFactorTariff, Supplier
from rest_framework import serializers

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = (
                'id',
                'name',
                'logo'
            )

class NodeSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer(many=False)
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
            'name',
            'charge_value',
            'charge_loss_of_transformation',
            'consume_begins',
            'consume_ends',
            'is_fixed',
            'over_max_demand',
            'unit_of_measurement'
        )


class PowerFactorTariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = PowerFactorTariff
        fields = (
            'max_power_factor',
            'min_power_factor',
            'charge_value',
            'charge_value_to_max'
        )


class TariffScheduleSerializer(serializers.ModelSerializer):
    tariff_values = TariffValuesSerializer(many=True)
    power_factor_tariff_values = PowerFactorTariffSerializer(many=True)
    supplier = SupplierSerializer(many=False)

    class Meta:
        model = TariffSchedule
        fields = (
            'supplier',
            'valid_from',
            'valid_to',
            'tariff_values',
            'power_factor_tariff_values'
        )

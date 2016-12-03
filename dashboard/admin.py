# -*- coding: utf-8 -*-
from django.contrib import admin
from dashboard.models import Node, Month, Day, Year, Time, Measure, \
    TariffSchedule, Supplier, TariffValue, TariffVariable, PowerFactorTariff


class NodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'parent', 'name', )


class MonthAdmin(admin.ModelAdmin):
    list_display = ('id', 'char_rep','month', )


class DayAdmin(admin.ModelAdmin):
    list_display = ('id', 'char_rep', 'day', )


class YearAdmin(admin.ModelAdmin):
    list_display = ('id', 'char_rep', 'year', )


class TimeAdmin(admin.ModelAdmin):
    list_display = ('id', 'char_rep', 'hour', 'mins', )


class MeasureAdmin(admin.ModelAdmin):
    list_display = ('id', 'datetime_str',
                 'active', 'apparent', 'demand', )
    exclude = ('datetime_str',)


class TariffVariablesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'consume_begins', 'consume_ends', 'is_fixed')


class TariffValuesAdmin(admin.ModelAdmin):
    list_display = ('id', 'variable', 'charge_value', 'charge_loss_of_transformation')


class PowerFactorTariffAdmin(admin.ModelAdmin):
    list_display = ('id', 'max_power_factor', 'min_power_factor', 'charge_value')


class TariffScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'supplier', 'valid_from', 'valid_to')


class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'logo')


admin.site.register(Node, NodeAdmin)
admin.site.register(Month, MonthAdmin)
admin.site.register(Day, DayAdmin)
admin.site.register(Year, YearAdmin)
admin.site.register(Time, TimeAdmin)
admin.site.register(Measure, MeasureAdmin)
admin.site.register(TariffSchedule, TariffScheduleAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(TariffValue, TariffValuesAdmin)
admin.site.register(TariffVariable, TariffVariablesAdmin)
admin.site.register(PowerFactorTariff, PowerFactorTariffAdmin)
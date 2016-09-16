from django.contrib import admin
from dashboard.models import Node, Month, Day, Year, Hour, Measure


class NodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'parent', 'name')


class MonthAdmin(admin.ModelAdmin):
    list_display('id', 'month')


class DayAdmin(admin.ModelAdmin):
    list_display('id', 'day')


class YearAdmin(admin.ModelAdmin):
    list_display('id', 'year')


class HourAdmin(admin.ModelAdmin):
    list_display('id', 'hour', 'mins')


class MeasureAdmin(admin.ModelAdmin):
    list_display('id', 'datetime_str_rep',
                 'active', 'apparent', 'demand')


admin.site.register(Node, NodoAdmin)
admin.site.register(Mont, NodoAdmin)
admin.site.register(Day, NodoAdmin)
admin.site.register(Year, NodoAdmin)
admin.site.register(Hour, NodoAdmin)
admin.site.register(Measure, MeasureAdmin)
from django.contrib import admin
from dashboard.models import Node, Month, Day, Year, Time, Measure


class NodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'parent', 'name', )


class MonthAdmin(admin.ModelAdmin):
    list_display = ('id', 'month', )


class DayAdmin(admin.ModelAdmin):
    list_display = ('id', 'day', )


class YearAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', )


class TimeAdmin(admin.ModelAdmin):
    list_display = ('id', 'hour', 'mins', )


class MeasureAdmin(admin.ModelAdmin):
    list_display = ('id', 'datetime_str_rep',
                 'active', 'apparent', 'demand', )


admin.site.register(Node, NodeAdmin)
admin.site.register(Month, MonthAdmin)
admin.site.register(Day, DayAdmin)
admin.site.register(Year, YearAdmin)
admin.site.register(Time, TimeAdmin)
admin.site.register(Measure, MeasureAdmin)
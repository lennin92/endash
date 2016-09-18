from django.contrib import admin
from dashboard.models import Node, Month, Day, Year, Time, Measure


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
    list_display = ('id', 'datetime_str_rep',
                 'active', 'apparent', 'demand', )


admin.site.register(Node, NodeAdmin)
admin.site.register(Month, MonthAdmin)
admin.site.register(Day, DayAdmin)
admin.site.register(Year, YearAdmin)
admin.site.register(Time, TimeAdmin)
admin.site.register(Measure, MeasureAdmin)
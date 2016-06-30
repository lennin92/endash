from django.contrib import admin
from dashboard.models import Measure, Node


class NodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'parent', 'name')

admin.site.register(Node, NodoAdmin)


class MeasureAdmin(admin.ModelAdmin):
    list_display = ('id', 'node', 'datetime',
                    'active', 'apparent' ,'demand')

admin.site.register(Measure, MeasureAdmin)

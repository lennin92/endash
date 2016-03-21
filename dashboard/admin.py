from django.contrib import admin
from dashboard.models import Medicion, Nodo
# Register your models here.


class NodoAdmin(admin.ModelAdmin):
    list_display = ('id', 'padre', 'nombre')

admin.site.register(Nodo, NodoAdmin)

class MedicionAdmin(admin.ModelAdmin):
    list_display = ('id', 'nodo', 'fecha_hora', 'demanda')

admin.site.register(Medicion)
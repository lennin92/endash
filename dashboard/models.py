from __future__ import unicode_literals

from django.db import models
from django.db.models import Max
import datetime

import logging

def get_imagen_nodo_dir(obj, filename):
    return 'nodo_%s/%s' % (obj.id, filename)


def create_valid_date(y, m, d, h=0, mm=0):
    try:
        if not (y % 4 == 0 and y % 100 != 0 or y % 400 == 0) and m == 2 and d > 28:
            return datetime.datetime(y, 2, 28, h, mm)
        else:
            return datetime.datetime(y, m, d, h, mm)
    except Exception as e:
        logging.error("Error al crear la fecha %d/%d/%d %d:%d"%(d, m, y, h, mm))



class DemandaNodo:
    fecha_inicio = None
    fecha_fin = None
    demanda = 0


class Nodo(models.Model):
    padre = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='hijos')
    nombre = models.CharField(max_length=20)
    descripcion = models.TextField()
    fotografia = models.ImageField(upload_to=get_imagen_nodo_dir, blank=True, null=True)

    @property
    def demandas(self):
        a = []
        end = datetime.datetime.now()
        end = create_valid_date(end.year, end.month, end.day, 23, 59)
        begin = create_valid_date(end.year, end.month, 1)
        dn = DemandaNodo()
        dn.fecha_inicio = begin
        dn.fecha_fin = end
        dn.demanda = Medicion.objects.filter(
                fecha_hora__range=(begin, end),
                nodo=self
        ).aggregate(Max('demanda'))['demanda__max']
        a.append(dn)

        end = create_valid_date(end.year, end.month - 1, end.day, 23, 59)
        begin = create_valid_date(end.year, end.month, 1)
        dn = DemandaNodo()
        dn.fecha_inicio = begin
        dn.fecha_fin = end
        dn.demanda = Medicion.objects.filter(
                fecha_hora__range=(begin, end),
                nodo=self
        ).aggregate(Max('demanda'))['demanda__max']
        a.append(dn)

        end = create_valid_date(end.year, end.month - 1, end.day, 23, 59)
        begin = create_valid_date(end.year, end.month, 1)
        dn = DemandaNodo()
        dn.fecha_inicio = begin
        dn.fecha_fin = end
        dn.demanda = Medicion.objects.filter(
                fecha_hora__range=(begin, end),
                nodo=self
        ).aggregate(Max('demanda'))['demanda__max']
        a.append(dn)

        return a

    def __str__(self):
        lg = 10
        if len(self.descripcion) < 15: lg = len(self.descripcion)
        return '[NODO %s] %s: %s' % (self.id, self.nombre, self.descripcion[:lg] + ' ...')

    class Meta:
        verbose_name = "Nodo"
        verbose_name_plural = "Nodos"


class Medicion(models.Model):
    nodo = models.ForeignKey('Nodo')
    fecha_hora = models.DateTimeField()
    energia_activa = models.IntegerField()
    energia_aparente = models.IntegerField()
    demanda = models.FloatField()

    class Meta:
        verbose_name = "Medicion"
        verbose_name_plural = "Mediciones"

    def __str__(self):
        return '[NODO %s] %s %s' % (self.nodo.id, str(self.fecha_hora), str(self.demanda))

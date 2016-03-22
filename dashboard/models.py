from __future__ import unicode_literals

from django.db import models


def get_imagen_nodo_dir(obj, filename):
    return 'nodo_%s/%s'%(obj.id, filename)


class Nodo(models.Model):
    padre = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='dependientes')
    nombre = models.CharField(max_length=20)
    descripcion = models.TextField()
    fotografia = models.ImageField(upload_to=get_imagen_nodo_dir)

    def __str__(self):
        lg=15
        if len(self.descripcion)<15: lg=len(self.descripcion)
        return '[NODO %s] %s: %s'%(self.id, self.nombre, self.descripcion[:lg]+' ...')


class Medicion(models.Model):
    nodo = models.ForeignKey('Nodo')
    fecha_hora = models.DateTimeField()
    energia_activa = models.IntegerField()
    energia_aparente = models.IntegerField()
    demanda = models.FloatField()

    def __str__(self):
        return '[NODO %s] %s %s'%(self.nodo.id, str(self.fecha_hora), str(self.demanda))

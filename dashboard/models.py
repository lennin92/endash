from django.contrib.gis.db import models
from django.db.models import Max
import datetime, logging


def get_imagen_nodo_dir(obj, filename):
    return 'nodo_%s/%s' % (obj.id, filename)


class Node(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='hijos')
    name = models.CharField(max_length=20)
    description = models.TextField()
    photography = models.ImageField(upload_to=get_imagen_nodo_dir, blank=True, null=True)
    coordinates = models.PointField(blank=True, null=True)


class Year(models.Model):
    year = models.IntegerField()
    char_rep = models.CharField(max_length=2)


class Month(models.Model):
    month = models.CharField(max_length=15)
    char_rep = models.CharField(max_length=2)
    integer_rep = models.IntegerField()


class Day(models.Model):
    day = models.IntegerField()
    char_rep = models.CharField(max_length=2)
    integer_rep = models.IntegerField()


class Time(models.Model):
    HOURS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    MINS  = [0, 15, 30, 45]
    hour = models.IntegerField(blank=False, null=False, choices=HOURS)
    mins = models.IntegerField(blank=False, null=False, choices=MINS)
    char_rep = models.CharField(max_length=5)


class Measure(models.Model):
    node = models.ForeignKey('Node')
    year = models.ForeignKey('Year')
    month = models.ForeignKey('Month')
    day = models.ForeignKey('Day')
    time = models.ForeignKey('Time')
    active = models.IntegerField()
    apparent = models.IntegerField()
    demand = models.FloatField()

    def datetime_str_rep(self):
        return '%s/%s/%s %s'%(self.year.char_rep, self.month.char_rep,
                              self.day.char_rep, self.time.char_rep)
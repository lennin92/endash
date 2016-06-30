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
    char_rep = models.CharField(max_length=3)
    integer_rep = models.IntegerField()

    def char_rep(self):
        s = str(self.integer_rep)
        if len(s)==1: s="0"+s
        return s


class DayOfMonth(models.Model):
    month = models.ForeignKey('Month')
    day = models.IntegerField()

    def char_rep(self):
        s = str(self.day)
        if len(s)==1: s="0"+s
        return s + "/" + self.month.char_rep()


class Measure(models.Model):
    node = models.ForeignKey('Node')
    year = models.ForeignKey('Year')
    day_of_month = models.ForeignKey('DayOfMonth')
    active = models.IntegerField()
    apparent = models.IntegerField()
    demand = models.FloatField()

    def datetime(self):
        return self.day_of_month.char_rep() + "/" + self.year.char_rep()

    def datetime_int(self):
        y = str(self.year.year)
        m = self.day_of_month.month.char_rep()
        d = str(self.day_of_month.day)
        if len(d)==1: d="0"+d
        return int(y+m+d)

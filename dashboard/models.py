# -*- coding: utf-8 -*-

from django.contrib.gis.db import models
from geoposition.fields import GeopositionField
from django.core.validators import MaxValueValidator, MinValueValidator


def get_imagen_nodo_dir(obj, filename):
    return 'nodo_%s/%s' % (obj.id, filename)


class Supplier(models.Model):
    name = models.CharField(max_length=10)
    logo = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.name


class TariffVariable(models.Model):
    name = models.CharField(max_length=35)
    consume_begins = models.TimeField()
    consume_ends = models.TimeField()
    is_fixed = models.BooleanField(default=False)
    calculated_over_demand = models.BooleanField(default=False)
    calculated_over_demand = models.BooleanField(default=False)

    def __str__(self): return self.name


class TariffValue(models.Model):
    variable = models.ForeignKey('TariffVariable')
    charge_value = models.FloatField()
    charge_loss_of_transformation = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    def name(self): return self.variable.name

    def consume_begins(self): return self.variable.consume_begins

    def consume_ends(self): return self.variable.consume_ends

    def is_fixed(self): return self.variable.is_fixed


class PowerFactorTariff(models.Model):
    max_power_factor = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])
    min_power_factor = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])
    charge_value = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])


class TariffSchedule(models.Model):
    supplier = models.ForeignKey('Supplier')
    valid_from = models.DateField()
    valid_to = models.DateField(blank=True, null=True)
    tariff_values = models.ManyToManyField('TariffValue')
    power_factor_tariff_values = models.ManyToManyField('PowerFactorTariff')

    def __str__(self):
        return "Tariff Schedule %s FROM: %s TO: %s"%(self.supplier.name,
                    self.valid_from.strftime("%Y-%m-%d"),
                    self.valid_to.strftime("%Y-%m-%d"))


class Node(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='hijos')
    supplier = models.ForeignKey('Supplier', blank=True, null=True)
    name = models.CharField(max_length=20)
    description = models.TextField()
    photography = models.ImageField(upload_to=get_imagen_nodo_dir, blank=True, null=True)
    location = GeopositionField(blank=True, null=True)

    def __str__(self):
        return "[%d] %s"%(self.id, self.name)


class Year(models.Model):
    year = models.IntegerField()
    char_rep = models.CharField(max_length=2)

    def __str__(self):
        return self.char_rep


class Month(models.Model):
    month = models.CharField(max_length=15)
    char_rep = models.CharField(max_length=2)
    integer_rep = models.IntegerField()

    def __str__(self):
        return self.char_rep


class Day(models.Model):
    day = models.IntegerField()
    char_rep = models.CharField(max_length=2)
    integer_rep = models.IntegerField()

    def __str__(self):
        return self.char_rep


class Time(models.Model):
    HOURS = (
        (0, '0'), (1, '1'), (2, '2'), (3, '3'),
        (4, '4'), (5, '5'), (6, '6'), (7, '7'),
        (8, '8'), (9, '9'), (10, '10'), (11, '11'),
        (12, '12'), (13, '13'), (14, '14'), (15, '15'),
        (16, '16'), (17, '17'), (18, '18'), (19, '19'),
        (20, '20'), (21, '21'), (22, '22'), (23, '23'),
    )
    MINS  = (
        (0, '0'), (15, '15'), (30, '30'), (45, '45'),
    )
    hour = models.IntegerField(blank=False, null=False, choices=HOURS)
    mins = models.IntegerField(blank=False, null=False, choices=MINS)
    char_rep = models.CharField(max_length=5)

    def __str__(self):
        return self.char_rep


class Measure(models.Model):
    node = models.ForeignKey('Node')
    year = models.ForeignKey('Year')
    month = models.ForeignKey('Month')
    day = models.ForeignKey('Day')
    time = models.ForeignKey('Time')
    active = models.IntegerField()
    apparent = models.IntegerField()
    demand = models.FloatField()
    datetime_str = models.CharField(max_length=16, default=None)
    
    class Meta:
        unique_together = ("node", "year", "month", "day", "time")

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.datetime_str = '%s-%s-%s %s'%(
            self.year.year,
            self.month.char_rep,
            self.day.char_rep,
            self.time.char_rep
        )
        super(Measure, self).save(force_insert, force_update, *args, **kwargs)
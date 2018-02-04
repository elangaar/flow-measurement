from django.db import models
from django.http import HttpResponse
from django.core.urlresolvers import reverse

import sys

class Station(models.Model):
    name = models.CharField(max_length=30)
    longitude = models.FloatField()
    latitude = models.FloatField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('stations')


class Device(models.Model):
    name = models.CharField(max_length=30)
    serial_number = models.CharField(max_length=30)
    TYPES_OF_DEVICES = (
        ('gazomierz', 'Gazomierz'),
        ('sterownik', 'Sterownik'),
        ('regulator', 'Regulator'),
    )
    dev_type = models.CharField(max_length=20, choices=TYPES_OF_DEVICES)

    def __str__(self):
        return "{0}, {1}".format(self.name, self.serial_number)

    def get_absolute_url(self):
        return reverse('devices')


class Result(models.Model):
    measurement_time = models.DurationField()
    temperature = models.FloatField()
    pressure = models.FloatField()
    error = models.FloatField()
    station = models.ForeignKey('Station', on_delete=models.CASCADE)
    reference_device = models.ForeignKey('Device', related_name='reference_device', on_delete=models.CASCADE)
    measured_device = models.ForeignKey('Device', related_name='measured_device', on_delete=models.CASCADE)


class ResultDevice(models.Model):
    volume = models.FloatField()
    flowrate = models.FloatField()
    device = models.ForeignKey('Device', on_delete=models.CASCADE)

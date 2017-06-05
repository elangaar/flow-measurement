from django.db import models
from django.core.urlresolvers import reverse


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

    def get_absolute_url(self):
        return reverse('devices')


class Values(models.Model):
    temperature = models.FloatField()
    pressure = models.FloatField()
    gas_meter_volume = models.FloatField()
    controller_volume = models.FloatField()

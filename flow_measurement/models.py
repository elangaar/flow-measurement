from django.db import models


class Station(models.Model):
    name = models.CharField(max_length=30)
    longitude = models.FloatField()
    latitude = models.FloatField()

    def __str__(self):
        return self.name


class Device(models.Model):
    name = models.CharField(max_length=30)
    serial_number = models.CharField(max_length=30)
    TYPES_OF_DEVICES = (
        ('gazomierz', 'Gazomierz'),
        ('sterownik', 'Sterownik'),
        ('regulator', 'Regulator'),
    )
    dev_type = models.CharField(max_length=20, choices=TYPES_OF_DEVICES)

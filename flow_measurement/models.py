from django.db import models
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

UserModel = get_user_model()

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
        ('reference_dev', 'reference device'),
        ('measured_dev', 'measured device'),
        ('regulator', 'regulator'),
    )
    dev_type = models.CharField(max_length=20, choices=TYPES_OF_DEVICES)
    station = models.ForeignKey('Station', null=True, blank=True)

    def __str__(self):
        return "{0}, {1}".format(self.name, self.serial_number)

    def get_absolute_url(self):
        return reverse('devices')


class ResultDevice(models.Model):
    volume = models.FloatField()
    flowrate = models.FloatField()
    device = models.ForeignKey('Device', on_delete=models.CASCADE)

    def __str__(self):
        return "{0} - {1} - {2}".format(
            self.device, self.volume, self.flowrate)


class Result(models.Model):
    user = models.ForeignKey(UserModel)
    date = models.DateTimeField()
    measurement_time = models.DurationField()
    temperature = models.FloatField()
    pressure = models.FloatField()
    error = models.FloatField()
    station = models.ForeignKey('Station', on_delete=models.CASCADE)
    reference_device = models.ForeignKey(
        'Device', related_name='reference_device',
        on_delete=models.CASCADE)
    measured_device = models.ForeignKey(
        'Device', related_name='measured_device',
        on_delete=models.CASCADE)

    def __str__(self):
        return "{0} - {1} - {2} - {3}".format(
            self.date, self.station, self.measured_device, self.error)

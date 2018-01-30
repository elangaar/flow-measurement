from django.test import TestCase
from django.core.urlresolvers import reverse

from flow_measurement.models import Station, Device

class TestStation(TestCase):
    def setUp(self):
        self.name = 'Testowa stacja'
        self.longitude = 20.000
        self.latitude = 50.000
        self.station = Station(name=self.name, longitude=self.longitude, latitude=self.latitude)

    def test_str(self):
        self.assertEqual('{0}'.format(self.name), str(self.station))

    def test_get_absolute_url(self):
        self.assertEqual(reverse('stations'), self.station.get_absolute_url())


class TestDevice(TestCase):
    def setUp(self):
        self.name = 'Testowe urządzenie'
        self.serial_number = '2432fsldf'
        self.dev_type = 'gazomierz'

        self.device = Device(name=self.name, serial_number=self.serial_number, dev_type=self.dev_type)

    def test_str(self):
        self.assertEqual("{0}, {1}".format(self.name, self.serial_number), str(self.device))

    def test_get_absolute_url(self):
        self.assertEqual(reverse('devices'), self.device.get_absolute_url())

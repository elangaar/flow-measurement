from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.forms import FloatField
from django.urls import reverse

from flow import settings
from flow_measurement.models import Station, Device
from flow_measurement import views


class MainPageTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.user.set_password('password')
        self.user.save()

    def test_without_logging(self):
        response = self.client.get(reverse('main-page'))
        self.assertRedirects(response, '/accounts/login/?next=/main/')
        self.assertEqual(response.resolver_match.func.__name__, views.MainPage.as_view().__name__)

    def test_with_logging(self):
        self.client.login(username='test_user', password='password')
        response = self.client.get(reverse('main-page'))
        self.assertEqual(response.status_code, 200)

    def test_templates(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('main-page'))
        self.assertTemplateUsed(response, 'flow_measurement/main.html')
        self.assertTemplateUsed(response, 'base.html')


class MeasurementViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.user.set_password('password')
        self.user.save()
        self.station = Station.objects.create(name="TestStation", latitude=23.23, longitude=23.23).save()

    def test_without_logging(self):
        response = self.client.get(reverse('measurement'))
        self.assertRedirects(response, '/accounts/login/?next=/measurement/')

    def test_with_logging(self):
        self.client.login(username='test_user', password='password')
        response = self.client.get(reverse('measurement'))
        self.assertEqual(response.status_code, 200)

    def test_templates(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('measurement'))
        self.assertTemplateUsed(response, 'base_left_menu.html')
        self.assertTemplateUsed(response, 'flow_measurement/measurement.html')

    def test_context(self):
        self.client.login(username='test_user', password='password')
        response = self.client.get(reverse('measurement'))
        stations_qs = Station.objects.all()
        devices_qs = Device.objects.all()
        self.assertQuerysetEqual(response.context['stations'], map(repr, stations_qs))
        self.assertQuerysetEqual(response.context['devices'], map(repr, devices_qs))

    def test_fields(self):
        self.client.login(username='test_user', password='password')
        self.assertFieldOutput(FloatField, {'1.1': 1.1}, {'aaa': ['Wpisz liczbę.']}, empty_value=None)


class SettingsViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.user.set_password('password')
        self.user.save()

    def test_without_logging(self):
        response = self.client.get(reverse('settings'))
        self.assertRedirects(response, '/accounts/login/?next=/settings/')

    def test_with_logging(self):
        self.client.login(username='test_user', password='password')
        response = self.client.get(reverse('settings'))
        self.assertEqual(response.status_code, 200)

    def test_templates(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('settings'))
        self.assertTemplateUsed(response, 'base_left_menu.html')
        self.assertTemplateUsed(response, 'flow_measurement/settings.html')


class InfoViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.user.set_password('password')
        self.user.save()

    def test_without_logging(self):
        response = self.client.get(reverse('info'))
        self.assertEqual(response.status_code, 200)

    def test_with_logging(self):
        self.client.login(username='test_user', password='password')
        response = self.client.get(reverse('info'))
        self.assertEqual(response.status_code, 200)

    def test_templates(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('info'))
        self.assertTemplateUsed(response, 'base_left_menu.html')
        self.assertTemplateUsed(response, 'flow_measurement/info.html')


class StationListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.user.set_password('password')
        self.user.save()

    def test_without_login(self):
        response = self.client.get(reverse('stations'))
        self.assertRedirects(response, '/accounts/login/?next=/stations/')

    def test_with_login(self):
        self.client.login(username='test_user', password='password')
        response = self.client.get(reverse('stations'))
        self.assertEqual(response.status_code, 200)

    def test_with_no_records(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('stations'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, views.StationListView.as_view().__name__)

        self.assertEqual(len(response.context['station_list']), 0)
        self.assertContains(response, '<p> Brak stacji w bazie danych </p>')


    def test_with_one_record(self):
        self.client.force_login(self.user)
        test_station = Station(name='Stacja testowa', longitude=50.00, latitude=50.000)
        test_station.save()
        response = self.client.get(reverse('stations'))

        self.assertEqual(len(response.context['station_list']), 1)

        context_stations = list(response.context['station_list'])
        stations_from_db = [i for i in Station.objects.all()]
        self.assertEqual(context_stations, stations_from_db)
        self.assertEqual(context_stations[0], test_station)

        self.assertContains(response, test_station.name)
        self.assertContains(response, str(test_station.longitude).replace('.', ','))
        self.assertContains(response, str(test_station.latitude).replace('.', ','))

        self.assertNotContains(response, '<p> Brak stacji w bazie danych </p>')

    def test_templates(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('stations'))
        self.assertTemplateUsed(response, 'base_left_menu.html')
        self.assertTemplateUsed(response, 'flow_measurement/station_list.html')


class StationCreateViewTest(TestCase):
    def test_station_created(self):
        self.client.post(reverse('add-station'), {
            'name': 'test_station',
            'longitude': 30.000,
            'latitude': 30.000
        })
        self.assertEqual(Station.objects.last().name, 'test_station')
        self.assertEqual(Station.objects.last().longitude, 30.000)
        self.assertEqual(Station.objects.last().latitude, 30.000)


class DeviceListView(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.user.set_password('password')
        self.user.save()

    def test_without_login(self):
        response = self.client.get(reverse('devices'))
        self.assertRedirects(response, '/accounts/login/?next=/devices/')

    def test_login(self):
        self.client.login(username='test_user', password='password')
        response = self.client.get(reverse('devices'))
        self.assertEqual(response.status_code, 200)

    def test_with_no_records(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('devices'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, views.DeviceListView.as_view().__name__)

        self.assertTemplateUsed(response, 'base_left_menu.html')
        self.assertTemplateUsed(response, 'flow_measurement/device_list.html')

        self.assertEqual(len(response.context['device_list']), 0)
        self.assertContains(response, '<p> Brak urządzeń w bazie danych </p>')

    def test_with_one_record(self):
        self.client.force_login(self.user)
        test_device = Device(name='test_device', serial_number='jh4k32', dev_type='gazomierz')
        test_device.save()
        response = self.client.get(reverse('devices'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, views.DeviceListView.as_view().__name__)

        self.assertTemplateUsed(response, 'base_left_menu.html')
        self.assertTemplateUsed(response, 'flow_measurement/device_list.html')

        context_devices = list(response.context['device_list'])
        devices_from_db = [d for d in Device.objects.all()]
        self.assertEqual(context_devices, devices_from_db)

        self.assertEqual(context_devices, devices_from_db)
        self.assertEqual(context_devices[0], test_device)

        self.assertContains(response, test_device.name)
        self.assertContains(response, test_device.serial_number)

        self.assertNotContains(response, '<p> Brak urządzeń w bazie danych </p>')


class DeviceCreateView(TestCase):
    def test_device_created(self):
        self.client.post(reverse('add-device'), {
            'name': 'test_device',
            'serial_number': '2423ffsd',
            'dev_type': 'gazomierz'
        })
        self.assertEqual(Device.objects.last().name, 'test_device')
        self.assertEqual(Device.objects.last().serial_number, '2423ffsd')
        self.assertEqual(Device.objects.last().dev_type, 'gazomierz')

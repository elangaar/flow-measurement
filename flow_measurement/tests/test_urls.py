from django.test import TestCase
from django.core.urlresolvers import reverse


class TestUrls(TestCase):
    urls = 'flow.urls'

    def test_reverse(self):
        self.assertEqual('/', reverse('index'))
        self.assertEqual('/main/', reverse('main-page'))
        self.assertEqual('/measurement/', reverse('measurement'))
        self.assertEqual('/settings/', reverse('settings'))
        self.assertEqual('/stations/', reverse('stations'))
        self.assertEqual('/devices/add/', reverse('add-device'))
        self.assertEqual('/devices/', reverse('devices'))
        self.assertEqual('/parameters/', reverse('parameters'))
        self.assertEqual('/get_temp_press/', reverse('get-temp-press'))

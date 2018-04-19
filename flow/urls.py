"""flow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from allauth.account import views
from flow_measurement.views import parameters
from flow_measurement.views import get_temp_press
from flow_measurement.views import get_todays_date
from flow_measurement.views import save_results

from flow_measurement.views import MainPage, MeasurementView, SettingsView
from flow_measurement.views import InfoView
from flow_measurement.views import (
    StationListView, DeviceListView,
    StationCreateView, DeviceCreateView,
    StationDetailView,
    DeviceDeleteView, StationDeleteView
)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.login, name='index'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^main/', MainPage.as_view(), name='main-page'),
    url(r'^measurement/$', MeasurementView.as_view(), name='measurement'),
    url(r'^settings/$', SettingsView.as_view(), name='settings'),
    url(r'^info/$', InfoView.as_view(), name='info'),
    url(r'^stations/(?P<pk>\d+)/$', StationDetailView.as_view(), name='detail-station'),
    url(r'^stations/delete/(?P<pk>\d+)/$', StationDeleteView.as_view(), name='delete-station'),
    url(r'^stations/add/$', StationCreateView.as_view(), name='add-station'),
    url(r'^stations/$', StationListView.as_view(), name='stations'),
    url(r'^devices/delete/(?P<pk>\d+)/', DeviceDeleteView.as_view(), name='delete-device'),
    url(r'^devices/add/$', DeviceCreateView.as_view(), name='add-device'),
    url(r'^devices/$', DeviceListView.as_view(), name='devices'),

    url(r'^parameters/$', parameters, name='parameters'),
    url(r'^get_temp_press/$', get_temp_press, name='get-temp-press'),
    url(r'^get_todays_date/$', get_todays_date, name='todays-date'),
    url(r'^save_results/$', save_results, name='save-results'),
]

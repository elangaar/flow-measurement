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
from flow_measurement.views import MainPage, MeasurementView, SettingsView
from flow_measurement.views import InfoView
from flow_measurement.views import (
    StationListView, DeviceListView,
    StationCreateView, DeviceCreateView
)

urlpatterns = [
    url(r'^account/', include('allauth.account.urls', namespace='allauth-account')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.login, name='index'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^main/', MainPage.as_view(), name='main-page'),
    url(r'^measurement/', MeasurementView.as_view(), name='measurement'),
    url(r'^settings/', SettingsView.as_view(), name='settings'),
    url(r'^info/', InfoView.as_view(), name='info'),
    url(r'^stations/add/', StationCreateView.as_view(), name='add-station'),
    url(r'^stations/', StationListView.as_view(), name='stations'),
    url(r'^devices/add/', DeviceCreateView.as_view(), name='add-device'),
    url(r'^devices/', DeviceListView.as_view(), name='devices'),
    url(r'^parameters/', parameters, name='parameters'),
]

import datetime
import json
import logging
import requests
logging.basicConfig(level=logging.DEBUG)


from django.views.generic import TemplateView, ListView, CreateView
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render


from .models import Station, Device


class MainPage(TemplateView):
    template_name = 'flow_measurement/main.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MainPage, self).dispatch(*args, **kwargs)


class MeasurementView(TemplateView):
    template_name = 'flow_measurement/measurement.html'
    model = Station

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MeasurementView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MeasurementView, self).get_context_data(*kwargs)
        context['stations'] = Station.objects.all()
        context['reference_devices'] = Device.objects.filter(
            dev_type='reference_dev'
        )
        context['measured_devices'] = Device.objects.filter(
            dev_type='measured_dev'
        )
        return context


class SettingsView(TemplateView):
    template_name = 'flow_measurement/settings.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SettingsView, self).dispatch(*args, **kwargs)


class InfoView(TemplateView):
    template_name = 'flow_measurement/info.html'



class StationListView(ListView):
    model = Station

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StationListView, self).dispatch(*args, **kwargs)


class StationCreateView(CreateView):
    template_name = 'flow_measurement/forms/station_create_form.html'
    model = Station
    fields = '__all__'


class DeviceListView(ListView):
    model = Device

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DeviceListView, self).dispatch(*args, **kwargs)


class DeviceCreateView(CreateView):
    template_name = 'flow_measurement/forms/device_create_form.html'
    model = Device
    fields = '__all__'


def parameters(request):
    P_ST = 1013
    T_ST = 293
    if request.method == 'POST':
        try:
            station_id = request.POST.get('station')
            station = Station.objects.get(id=station_id)
            station_name = station.name
            ref_dev_id = request.POST.get('reference_device')
            ref_dev = Device.objects.get(id=ref_dev_id)
            meas_dev_id = request.POST.get('measured_device')
            meas_dev = Device.objects.get(id=meas_dev_id)
            # dev_name = dev.name + ', ' + dev.serial_number

            temperature = float(request.POST.get('temperature')) + 273
            pressure = float(request.POST.get('pressure'))
            meas_date = request.POST.get('measurement_date')
            meas_time = request.POST.get('measurement_time')
            ref_dev_volume = float(request.POST.get('refDevVolume'))
            meas_dev_volume = float(request.POST.get('measDevVolume'))
            coefficient = (P_ST * temperature)/(T_ST * pressure)
            tcv = ref_dev_volume * coefficient
            error = ((meas_dev_volume - tcv) / tcv) * 100
            json_data = {
                'station': station_name,
                'reference_device': ref_dev,
                'measured_device': meas_dev,
                'temperature': temperature,
                'pressure': pressure,
                'measurement_date': meas_date,
                'measurement_time': meas_time,
                'ref_dev_volume': ref_dev_volume,
                'meas_dev_volume': meas_dev_volume,
                'coefficient': coefficient,
                'theoretical_controller_volume': tcv,
                'error': error
            }
        except ValueError as e:
            message = str(e)
            return JsonResponse({"message": message})

        return render(request, 'flow_measurement/results.html', json_data)
    else:
        return HttpResponseRedirect(reverse('main-page'))


def get_temp_press(request):
    API_TOKEN = 'f82f1466e23527d47a9af5dc26373c43'
    API_URL_BASE = 'http://api.openweathermap.org/data/2.5/weather'
    headers = {
        'Content-Type': 'application/json',
    }

    if request.method == 'POST':
        station_id = request.POST.get('station')
        coordinates = json.loads(get_coordinates(station_id))
        lat = coordinates['lat']
        lon = coordinates['lon']
        url_parameters = {
            'lat': lat,
            'lon': lon,
            'appid': API_TOKEN
        }
        response = requests.get(API_URL_BASE, params=url_parameters, headers=headers)
        data = json.loads(response.content)
        temp_k = float(data['main']['temp']) - 273
        temp = '{:.1f}'.format(temp_k)
        press = data['main']['pressure']

        json_response = {"temperature": temp, "pressure": press}
        return JsonResponse(json_response)
    else:
        return HttpResponseRedirect(reverse('main-page'))

## niedostepne dla usera
def get_coordinates(station_id):
    station = Station.objects.get(id=station_id)
    coordinates = {
        'lat': station.latitude,
        'lon': station.longitude
    }
    json_data = json.dumps(coordinates)
    return json_data

## niedostepne dla usera
def get_todays_date(request):
    date = datetime.date.today()
    json_date = {
        'date': date
    }
    return JsonResponse(json_date)

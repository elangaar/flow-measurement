import datetime
import time
import json
import requests


from django.views.generic import TemplateView, ListView, CreateView
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from .models import Station, Device, Result, ResultDevice, StationDevice
from .forms import DeviceForm


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
        context = super(MeasurementView, self).get_context_data(**kwargs)
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
    form_class = DeviceForm

    def form_valid(self, form):
        if form.cleaned_data.get('station') is not None:
            form.save()
            device_name = form.cleaned_data.get('name')
            device = Device.objects.get(name=device_name)
            station = form.cleaned_data['station']
            start_date= datetime.date.today()
            sd = StationDevice.objects.create(device=device, station=station, start_date=start_date)
            sd.save()
        form.save()
        return super().form_valid(form)


def parameters(request):
    P_ST = 1013
    T_ST = 293
    if request.method == 'POST':
        try:
            station_id = request.POST.get('station')
            station = Station.objects.get(id=station_id)
            station_name = station.name
            ref_dev_id = request.POST.get('referenced_device')
            ref_dev = Device.objects.get(id=ref_dev_id)
            meas_dev_id = request.POST.get('measured_device')
            meas_dev = Device.objects.get(id=meas_dev_id)
            temperature = float(request.POST.get('temperature'))
            temp_k = temperature + 273
            pressure = float(request.POST.get('pressure'))
            meas_date = request.POST.get('measurement_date')
            meas_time = request.POST.get('measurement_time')
            ref_dev_volume = float(request.POST.get('refDevVolume'))
            meas_dev_volume = float(request.POST.get('measDevVolume'))
            coeff = (P_ST * temp_k)/(T_ST * pressure)
            tcv = ref_dev_volume * coeff
            flowrate_ref_dev = get_flowrate(ref_dev_volume, meas_time)
            flowrate_meas_dev = get_flowrate(meas_dev_volume, meas_time)
            coefficient = format(coeff, '.4f')
            error = format((((meas_dev_volume - tcv) / tcv) * 100), '.2f')
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
                'flowrate_ref_dev': flowrate_ref_dev,
                'flowrate_meas_dev': flowrate_meas_dev,
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


def save_results(request):
    P_ST = 1013
    T_ST = 293
    if request.method == 'POST':
        referenced_device_id = request.POST.get('referenced_device')
        referenced_device = Device.objects.get(id=referenced_device_id)
        measured_device_id = request.POST.get('measured_device')
        measured_device = Device.objects.get(id=measured_device_id)
        referenced_volume = request.POST.get('refDevVolume')
        measured_volume = request.POST.get('measDevVolume')
        temperature = float(request.POST.get('temperature'))
        temp_k = temperature + 273
        pressure = float(request.POST.get('pressure'))
        measurement_date = request.POST.get('measurement_date')
        measurement_time = request.POST.get('measurement_time')
        referenced_volume = float(request.POST.get('refDevVolume'))
        measured_volume = float(request.POST.get('measDevVolume'))
        coeff = (P_ST * temp_k)/(T_ST * pressure)
        tcv = referenced_volume * coeff
        referenced_flowrate= get_flowrate(referenced_volume, measurement_time)
        measured_flowrate= get_flowrate(measured_volume, measurement_time)
        coefficient = format(coeff, '.4f')
        error = format((((measured_volume - tcv) / tcv) * 100), '.2f')
result_referenced_device = ResultDevice.objects.create(
            volume=referenced_volume,
            flowrate=referenced_flowrate,
            device=referenced_device
        )
        result_measured_device = ResultDevice.objects.create(
            volume=measured_volume,
            flowrate=measured_flowrate,
            device=measured_device
        )
        result_referenced_device.save()
        result_measured_device.save()
        station_id = request.POST.get('station')
        station = Station.objects.get(id=station_id)
        user = request.user
        measurement_date = request.POST.get('measurement_date')
        measurement_time_str = request.POST.get('measurement_time')
        measurement_time = get_time(measurement_time_str)
        temperature = request.POST.get('temperature')
        pressure = request.POST.get('pressure')
        reference_device = result_referenced_device
        measured_device = result_measured_device
        result = Result.objects.create(
            user=user,
            measurement_date=measurement_date,
            measurement_time=measurement_time,
            temperature=temperature,
            pressure=pressure,
            error=error,
            station=station,
            reference_device=reference_device,
            measured_device=measured_device,
        )
        result.save()
        return JsonResponse({'success': True})


def get_time(time_str):
    time_list = time_str.split(':')
    if len(time_list) == 2:
        hours, minutes = time_list
        measurement_time = datetime.timedelta(hours=int(hours),
                minutes=int(minutes))
    elif len(time_list) == 3:
        hours, minutes, seconds = time_list
        measurement_time = datetime.timedelta(hours=int(hours),
                minutes=int(minutes), seconds=int(seconds))
    else:
        pass
    return measurement_time


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


def get_coordinates(station_id):
    station = Station.objects.get(id=station_id)
    coordinates = {
        'lat': station.latitude,
        'lon': station.longitude
    }
    json_data = json.dumps(coordinates)
    return json_data


def get_todays_date(request):
    current_date = datetime.date.today()
    json_date = {
        'current_date': current_date
    }
    return JsonResponse(json_date)


def get_flowrate(volume, meas_time):
    if len(meas_time) == 5:
        meas_time = time.strptime(meas_time, '%H:%M')
        meas_time_delta = datetime.timedelta(
            hours=meas_time.tm_hour,
            minutes=meas_time.tm_min
        )
        meas_time_minutes = meas_time_delta.seconds / 60
        flowrate = format(volume / meas_time_minutes, '.2f')
        return flowrate
    elif len(meas_time) == 8:
        meas_time = time.strptime(meas_time, '%H:%M:%S')
        meas_time_delta = datetime.timedelta(
            hours=meas_time.tm_hour,
            minutes=meas_time.tm_min,
            seconds=meas_time.tm_sec
        )
        meas_time_minutes = meas_time_delta.seconds / 60
        flowrate = format(volume / meas_time_minutes, '.2f')
        return flowrate
    else:
        return None

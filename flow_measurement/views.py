from django.views.generic import TemplateView, ListView, CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Station, Device
from django.http import HttpResponse, JsonResponse


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
        context['devices'] = Device.objects.all()
        return context


class SettingsView(TemplateView):
    template_name = 'flow_measurement/settings.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SettingsView, self).dispatch(*args, **kwargs)


class InfoView(TemplateView):
    template_name = 'flow_measurement/info.html'


def parameters(request):
    P_ST = 1013
    T_ST = 293
    if request.method == 'POST':
        try:
            stat_id = request.POST.get('station')
            stat = Station.objects.get(id=stat_id)
            stat_name = stat.name
            dev_id = request.POST.get('device')
            dev = Device.objects.get(id=dev_id)
            dev_name = dev.name + ', ' + dev.serial_number

            temperature = float(request.POST.get('temperature')) + 273
            pressure = float(request.POST.get('pressure'))
            gas_meter_volume = float(request.POST.get('gasMeterVolume'))
            cv = float(request.POST.get('controllerVolume'))
            coefficient = (P_ST * temperature)/(T_ST * pressure)
            tcv = gas_meter_volume * coefficient
            error = ((cv - tcv) / tcv) * 100
            json_string = {
                'station': stat_name,
                'device': dev_name,
                'temperature': temperature,
                'pressure': pressure,
                'gas_meter_volume': gas_meter_volume,
                'controller_volume': cv,
                'coefficient': coefficient,
                'theoretical_controller_volume': tcv,
                'error': error
            }
        except ValueError:
            return JsonResponse({'message': 'Coś jest nie tak z wartościami!'})

        return JsonResponse(json_string)
    else:
        return HttpResponse('<p> Nie działa! </p>')


class StationListView(ListView):
    model = Station


class StationCreateView(CreateView):
    template_name = 'flow_measurement/forms/station_create_form.html'
    model = Station
    fields = '__all__'


class DeviceListView(ListView):
    model = Device


class DeviceCreateView(CreateView):
    template_name = 'flow_measurement/forms/device_create_form.html'
    model = Device
    fields = '__all__'

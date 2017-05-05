from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Station, Device


class MainPage(TemplateView):
    template_name = 'flow_measurement/main.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MainPage, self).dispatch(*args, **kwargs)


class MeasurementView(TemplateView):
    template_name = 'flow_measurement/measurement.html'
    model = Station

    def get_context_data(self, **kwargs):
        context = super(MeasurementView, self).get_context_data(*kwargs)
        context['stations'] = Station.objects.all()
        context['devices'] = Device.objects.all()
        return context


class SettingsView(TemplateView):
    template_name = 'flow_measurement/settings.html'


class InfoView(TemplateView):
    template_name = 'flow_measurement/info.html'

import datetime

from django import forms

from flow_measurement.models import Device, Station

class DeviceForm(forms.ModelForm):
    name = forms.CharField(label='name', max_length=35)
    serial_number = forms.CharField(label='serial number', max_length=35)
    TYPES_OF_DEVICES = (
        ('reference_dev', 'reference device'),
        ('measured_dev', 'measured device'),
        ('regulator', 'regulator'),
    )
    dev_type = forms.ChoiceField(label='device type', choices=TYPES_OF_DEVICES)
    station = forms.ModelChoiceField(label='station', required=False,  queryset=Station.objects.all())

    class Meta:
        model = Device
        fields = ['name', 'serial_number', 'dev_type', 'station']


class StationForm(forms.ModelForm):
    name = forms.CharField(label='name', max_length=40)
    longitude = forms.FloatField(label='longitude')
    latitude = forms.FloatField(label='latitude')

    class Meta:
        model = Station
        fields = ['name', 'longitude', 'latitude']

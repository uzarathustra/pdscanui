from django import forms
from .models import Transmitter, Receiver, Measurement


class TransmitterForm(forms.ModelForm):
    class Meta:
        model = Transmitter
        labels = {
            'wavelength': 'Wavelength [nm]',
            'temperature_min': 'Max. Temperature [°C]',
            'temperature_max': 'Min. Temperature [°C]',
            'power_max': 'Max Power [mW]',
            'current_max': 'Max Current [mA]'
        }
        fields = ['name', 'manufacturer', 'type_of_transmitter', 'wavelength', 'temperature_min', 'temperature_max',
                  'power_max', 'current_max']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control'}),
            'type_of_transmitter': forms.Select(attrs={'class': 'form-control'}),
            'wavelength': forms.TextInput(attrs={'class': 'form-control'}),
            'temperature_min': forms.NumberInput(attrs={'class': 'form-control'}),
            'temperature_max': forms.NumberInput(attrs={'class': 'form-control'}),
            'power_max': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'limit value'}),
            'current_max': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'limit value'}),
        }


class ReceiverForm(forms.ModelForm):
    class Meta:
        model = Receiver
        labels = {
            'temperature_min': 'Max. Temperature [°C]',
            'temperature_max': 'Min. Temperature [°C]',
            'sensitive_area': 'Sensitive Area [qmm]',
            'spectral_bandwidth': 'Spectral Bandwidth [nm]',
            'response_time': 'Response Time [ns]'
        }
        fields = ['name', 'manufacturer', 'type_of_receiver', 'temperature_min', 'temperature_max', 'sensitive_area',
                  'spectral_bandwidth', 'response_time']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control'}),
            'type_of_receiver': forms.Select(attrs={'class': 'form-control'}),
            'temperature_min': forms.NumberInput(attrs={'class': 'form-control'}),
            'temperature_max': forms.NumberInput(attrs={'class': 'form-control'}),
            'sensitive_area': forms.NumberInput(attrs={'class': 'form-control'}),
            'spectral_bandwidth': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'limit value'}),
            'response_time': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'limit value'}),
        }


class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement

        transmitter = forms.ModelChoiceField(queryset=Transmitter.objects.all())
        receiver = forms.ModelChoiceField(queryset=Receiver.objects.all())

        fields = ['transmitter', 'receiver', 'date', 'note']

        widgets = {
            'transmitter': forms.Select(attrs={'class': 'form-select', 'aria-label': 'Default select example'}),
            'receiver': forms.Select(attrs={'class': 'form-select', 'aria-label': 'Default select example'}),
            'date': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input',
                         'data-target': '#datetimepicker1'}),
            'note': forms.TextInput(attrs={'class': 'form-control'}),
        }


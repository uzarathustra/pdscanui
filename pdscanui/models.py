from django.db import models
from django.utils import timezone as tz

class Transmitter(models.Model):
    VCSEL_N = "VCSEL_N"
    VCSEL_P = "VCSEL_P"
    LED_N = "LED_N"
    LED_P = "LED_P"
    RCLED_N = "RCLED_N"
    RCLED_P = "RCLED_P"
    TYPE_OF_TRANSMITTER_CHOICES = [
        (VCSEL_N, "VCSEL_N-type"),
        (VCSEL_P, "VCSEL_P-type"),
        (LED_N, "LED_N-type"),
        (LED_P, "LED_P-type"),
        (RCLED_N, "RCLED_N-type"),
        (RCLED_P, "RCLED_P-type")
    ]

    name = models.CharField(max_length=30)
    manufacturer = models.CharField(max_length=30)
    type_of_transmitter = models.CharField(max_length=8, choices=TYPE_OF_TRANSMITTER_CHOICES, default="VCSEL_N")
    wavelength = models.CharField(max_length=30)
    temperature_min = models.FloatField()
    temperature_max = models.FloatField()
    current_max = models.FloatField()
    power_max = models.FloatField(default=1)
    def __str__(self):
        return self.name


class Receiver(models.Model):
    PIN = "PIN-Diode"
    APD = "Avalanche-PD"
    MSM = "MSM-PD"
    MLED = "Modified-LED"
    TYPE_OF_RECEIVER_CHOICES = [
        (PIN, "PIN-Diode"),
        (APD, "Avalanche-Photo-Diode"),
        (MSM, "Metal-Semiconductor-Metal-Photo-Diode"),
        (MLED, "Modified-LED")
    ]

    name = models.CharField(max_length=30)
    manufacturer = models.CharField(max_length=30)
    type_of_receiver = models.CharField(max_length=12, choices=TYPE_OF_RECEIVER_CHOICES, default="VCSEL_N")
    temperature_min = models.FloatField()
    temperature_max = models.FloatField()
    sensitive_area = models.FloatField()
    spectral_bandwidth = models.CharField(max_length=30)
    response_time = models.FloatField()
    def __str__(self):
        return self.name


class Measurement(models.Model):
    transmitter = models.ForeignKey(Transmitter, on_delete=models.CASCADE)
    receiver = models.ForeignKey(Receiver, on_delete=models.CASCADE)
    date = models.DateTimeField(null=False, blank=False, default=tz.now)
    note = models.TextField(blank=True)
    def __str__(self):
        return str(self.id)


class Data(models.Model):
    measurement_id = models.ForeignKey(Measurement, on_delete=models.CASCADE)
    position = models.IntegerField()
    optpower_in = models.FloatField()
    optpower_out = models.FloatField()


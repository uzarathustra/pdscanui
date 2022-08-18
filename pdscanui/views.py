import subprocess
import os
#from datetime import time
import time

import websocket
import json
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Transmitter, Receiver, Measurement
from .forms import TransmitterForm, ReceiverForm, MeasurementForm
from .models import Measurement
from .models import Data
from django.http import JsonResponse
from django.core import serializers


def home(request):
    return render(request, 'pdscanui/home.html')

def drive(request):
    return render(request, 'pdscanui/drive.html')

def receive(ws):
    encoderValue_old = 2000000
    counter = 0
    while counter < 10:
        receivedData = ws.recv()
        splittedDataArray = receivedData.split()
        encoderValue = splittedDataArray[0]
        sauronValue = splittedDataArray[1]
        print("EncoderValue: ", encoderValue)
        print("SauronValue: ", sauronValue)
        # if result_old != result:
            # dataList.append(int(result))
        if encoderValue_old == encoderValue:  # Equality Counter
            counter += 1
        encoderValue_old = encoderValue
    return {'encv':encoderValue, 'sauv': sauronValue}


def direction(dir_value):
    switcher={
        "yinc" : 1,
        "ydec" : -1,
        "xinc" : 2,
        "xdec" : -2,
        "zinc" : 3,
        "zdec" : -3,
        "xyhome" : 10,
        "zhome" : 30
    }
    return (switcher.get(dir_value))

def view_update_drive(request):
    if request.method == 'POST':
        # Values from POST-Transfer evaluate
        if ('pos_value' and 'dir_value') in request.POST:
            pos_value = request.POST['pos_value']
            dir_value = request.POST['dir_value']
            dir_float = direction(dir_value)
            print("Werte:" + pos_value + " " + str(dir_float))

            ws = websocket.WebSocket()
            ws.connect("ws://192.168.177.46/ws")

            # Define Dir-Positions (X,Y,Z)
            if dir_float < 4:
                myDict = {"mot": abs(dir_float), "pos": (dir_float/abs(dir_float))*(float(pos_value)), "res": 0, "deb": 1}
                ws.send(json.dumps(myDict))
                print("...gesendet!")
            else:
                # Define Home-Positions
                myDict = {"mot": dir_float/10, "pos": 0, "res": 0, "deb": 1}
                ws.send(json.dumps(myDict))
                print("...gesendet!")

            # Receive new data
            encv = receive(ws)['encv']
            sauv = receive(ws)['sauv']
            encv2 = "0"
            sauv2 = "0"
            print("... disconnected.")

            if dir_float == 10:
                time.sleep(2)
                # Define Home-Positions (X-Pos)
                myDict = {"mot": 2, "pos": 0, "res": 0, "deb": 1}
                ws.send(json.dumps(myDict))
                print("...gesendet!")
                encv2 = receive(ws)['encv']
                sauv2 = receive(ws)['sauv']

            print(encv)
            print(sauv)

            ws.close()

    #return render(request, 'pdscanui/drive.html')
    return HttpResponse('success', {'enc_value': encv, 'sau_value': sauv, 'enc2_value': encv2, 'sau2_value': sauv2})  # if everything is OK

def updatePosition(request):
    if request.is_ajax and request.method == 'GET':
        dir_value = request.GET.get('dir_value')
        pos_value = request.GET.get('pos_value')
        if pos_value != "":
            print("pos:" + pos_value)

            dir_float = direction(dir_value)

            ws = websocket.WebSocket()
            ws.connect("ws://192.168.177.46/ws")

            # Define Dir-Positions (X,Y,Z)
            if dir_float < 4:
                myDict = {"mot": abs(dir_float), "pos": (dir_float / abs(dir_float)) * (float(pos_value)), "res": 0,
                          "deb": 1}
                ws.send(json.dumps(myDict))
            else:
                # Define Home-Positions
                myDict = {"mot": dir_float / 10, "pos": 0, "res": 0, "deb": 1}
                ws.send(json.dumps(myDict))

            # Receive new data
            encv = receive(ws)['encv']
            sauv = receive(ws)['sauv']
            encv2 = "0"
            sauv2 = "0"

            # Time to read buffer completely
            time.sleep(1)

            # disconnect
            ws.close()


            if dir_float == 10:
                ws.connect("ws://192.168.177.46/ws")

                # Define Home-Positions (X-Pos)
                myDict = {"mot": 2, "pos": 0, "res": 0, "deb": 1}
                ws.send(json.dumps(myDict))
                print("...gesendet!")
                print("")
                encv2 = receive(ws)['encv']
                sauv2 = receive(ws)['sauv']
                print(encv2)
                # disconnect
                ws.close()

            print(encv)
            print("")
            print(encv2)

            return JsonResponse({'dir_return': dir_value, 'pos_return':encv,  'opw_return':sauv, 'pos2_return':encv2,  'opw2_return':sauv2}, status=200)
        else:
            return HttpResponse('error')


##################################### Tranmitter-Views

def transmitter_create(request):
    if request.method == 'GET':
        return render(request, 'pdscanui/transmitter_create.html', {'form': TransmitterForm()})
    else:
        try:
            form = TransmitterForm(request.POST)
            form.save()
            return redirect('transmitter_list')
        except ValueError:
            return render(request, 'pdscanui/transmitter_create.html', {'form': TransmitterForm(), 'error': 'Falsche Eingabedaten. Versuche es nochmal.'})

def transmitter_list(request):
    # transmitters = Transmitter.objects.filter(name='ADL65074TL')
    transmitters = Transmitter.objects.all()
    return render(request, 'pdscanui/transmitter_list.html', {'transmitters': transmitters})


def transmitter_modify(request, transmitter_pk):
    transmitters = Transmitter.objects.all()
    if request.method == 'GET':
        transmitter = get_object_or_404(Transmitter, pk=transmitter_pk)  # pk-value from GET-Methode
    else:  # after submit-Button --> POST-request
        transmitter = get_object_or_404(Transmitter, pk=request.POST.get('Transmitter')) # pk-value from POST-Methode ???)
    form = TransmitterForm(instance=transmitter)  # submit instance after form-call ???
    return render(request, 'pdscanui/transmitter_modify.html', {'transmitters': transmitters, 'transmitter': transmitter, 'form': form})


def transmitter_delete(request, transmitter_pk):
    transmitters = Transmitter.objects.all()
    transmitter = get_object_or_404(Transmitter, pk=transmitter_pk)
    if request.method == 'POST':
        transmitter.delete()
        return redirect('transmitter_list')


def transmitter_save(request, transmitter_pk):
    transmitters = Transmitter.objects.all()
    transmitter = get_object_or_404(Transmitter, pk=transmitter_pk)
    form = TransmitterForm(request.POST, instance=transmitter)
    if request.method == 'POST':
        try:
            print("Success")
            form.save()
            return render(request, 'pdscanui/transmitter_modify.html', {'transmitter': transmitter, 'form': form, 'transmitters': transmitters})
        except ValueError:
            print("Error")
            form = TransmitterForm(instance=transmitter)
            return render(request, 'pdscanui/transmitter_modify.html', {'transmitter': transmitter, 'form': form, 'transmitters': transmitters})


##################################### Receiver-Views

def receiver_create(request):
    if request.method == 'GET':
        return render(request, 'pdscanui/receiver_create.html', {'form': ReceiverForm()})
    else:
        try:
            form = ReceiverForm(request.POST)
            form.save()
            return redirect('receiver_list')
        except ValueError:
            return render(request, 'pdscanui/receiver_create.html', {'form': ReceiverForm(), 'error': 'Falsche Eingabedaten. Versuche es nochmal.'})

def receiver_list(request):
    # receivers = Receiver.objects.filter(name='ADL65074TL')
    receivers = Receiver.objects.all()
    return render(request, 'pdscanui/receiver_list.html', {'receivers': receivers})


def receiver_modify(request, receiver_pk):
    receivers = Receiver.objects.all()
    if request.method == 'GET':
        receiver = get_object_or_404(Receiver, pk=receiver_pk)  # pk-value from GET-Methode
    else:  # after submit-Button --> POST-request
        receiver = get_object_or_404(Receiver, pk=request.POST.get('Receiver')) # pk-value from POST-Methode ???)
    form = ReceiverForm(instance=receiver)  # submit instance after form-call ???
    return render(request, 'pdscanui/receiver_modify.html', {'receivers': receivers, 'receiver': receiver, 'form': form})


def receiver_delete(request, receiver_pk):
    receivers = Receiver.objects.all()
    receiver = get_object_or_404(Receiver, pk=receiver_pk)
    if request.method == 'POST':
        receiver.delete()
        return redirect('receiver_list')


def receiver_save(request, receiver_pk):
    receivers = Receiver.objects.all()
    receiver = get_object_or_404(Receiver, pk=receiver_pk)
    form = ReceiverForm(request.POST, instance=receiver)
    if request.method == 'POST':
        try:
            print("Success")
            form.save()
            return render(request, 'pdscanui/receiver_modify.html', {'receiver': receiver, 'form': form, 'receivers': receivers})
        except ValueError:
            print("Error")
            form = ReceiverForm(instance=receiver)
            return render(request, 'pdscanui/receiver_modify.html', {'receiver': receiver, 'form': form, 'receivers': receivers})


def receiver(request):
    return render(request, 'pdscanui/receiver_list.html')


##################################### Measurement-Views
def measurement_create(request):
    if request.method == 'GET':
        return render(request, 'pdscanui/measurement_create.html', {'form': MeasurementForm()})
    else:
        try:
            form = MeasurementForm(request.POST)
            form.save()
            return redirect('home')
        except ValueError:
            return render(request, 'pdscanui/measurement_create.html', {'form': MeasurementForm(), 'error': 'Falsche Eingabedaten. Versuche es nochmal.'})


def measurement_list(request):
    measurements = Measurement.objects.all()
    return render(request, 'pdscanui/measurement_list.html', {'measurements': measurements})


def measurement_modify(request, measurement_pk):
    measurements = Measurement.objects.all()
    if request.method == 'GET':
        measurement = get_object_or_404(Measurement, pk=measurement_pk)  # pk-value from GET-Methode
    else:  # after submit-Button --> POST-request
        measurement = get_object_or_404(Measurement, pk=request.POST.get('Receiver')) # pk-value from POST-Methode ???)
    form = MeasurementForm(instance=measurement)  # submit instance after form-call ???
    return render(request, 'pdscanui/measurement_modify.html', {'measurements': measurements, 'measurement': measurement, 'form': form})


def measurement_delete(request, measurement_pk):
    measurements = Measurement.objects.all()
    measurement = get_object_or_404(Measurement, pk=measurement_pk)
    if request.method == 'POST':
        measurement.delete()
        return redirect('measurement_list')


def measurement_save(request, measurement_pk):
    measurements = Measurement.objects.all()
    measurement = get_object_or_404(Measurement, pk=measurement_pk)
    form = MeasurementForm(request.POST, instance=measurement)
    if request.method == 'POST':
        try:
            print("Success")
            form.save()
            return render(request, 'pdscanui/measurement_modify.html', {'measurement': measurement, 'form': form, 'measurements': measurements})
        except ValueError:
            print("Error")
            form = MeasurementForm(instance=measurement)
            return render(request, 'pdscanui/measurement_modify.html', {'measurement': measurement, 'form': form, 'measurements': measurements})


def measurement(request):
    return render(request, 'pdscanui/measurement_list.html')


##################################### Result-Views
def results(request):
    return render(request, 'pdscanui/results.html')

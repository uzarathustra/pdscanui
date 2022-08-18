import websocket
import json
#from Functions import dataList, draw_plot, show_plots, dataForErrorAnalysisMotor1, dataForErrorAnalysisMotor2,dataForErrorAnalysisMotor3
import time

print("start")


def receive():
    encoderValue_old = 2000000
    counter = 0
    while counter < 25:
        receivedData = ws.recv()
        splittedDataArray = receivedData.split()
        encoderValue = splittedDataArray[0]
        sauronValue = splittedDataArray[1]
        #print("EncoderValue: ", encoderValue)
        print("SauronValue: ", sauronValue)
        # if result_old != result:
            # dataList.append(int(result))
        if encoderValue_old == encoderValue:
            counter += 1
        encoderValue_old = encoderValue


ws = websocket.WebSocket()
ws.connect("ws://192.168.177.46/ws")


# while True:
# for i in range(0, 9):

myDict = {"mot": 1, "pos": 1350, "res": 0, "deb": 1}       # 3 Rotations to the right
ws.send(json.dumps(myDict))
print("...gesendet!")
receive()
#dataForErrorAnalysisMotor1.append(ws.recv())
#print(f"Motor1: {dataForErrorAnalysisMotor1}")
#draw_plot(dataList, 2)
#dataList.clear()


myDict = {"mot": 1, "pos": 0, "res": 0, "deb": 1}       # 3 Rotations to the right
ws.send(json.dumps(myDict))
print("...gesendet!")
receive()
#dataForErrorAnalysisMotor1.append(ws.recv())
#print(f"Motor1: {dataForErrorAnalysisMotor1}")
#draw_plot(dataList, 2)
#dataList.clear()



    # myDict = {"mot": 1, "pos": 0, "res": 0, "deb": 1}          # 3 Rotations to the left
    # ws.send(json.dumps(myDict))
    # receive()
    # dataForErrorAnalysisMotor1.append(ws.recv())
    # print(f"Motor1: {dataForErrorAnalysisMotor1}")
    #
    # draw_plot(dataList, 1)
    # dataList.clear()


    # myDict = {"mot": 1, "pos": 1080, "res": 0, "deb": 1}        # 3 Rotations to the right
    # ws.send(json.dumps(myDict))
    # receive()
    # dataForErrorAnalysisMotor1.append(ws.recv())
    # print(f"Motor1: {dataForErrorAnalysisMotor1}")
    # draw_plot(dataList, 3)
    # dataList.clear()


    # myDict = {"mot": 2, "pos": 1080, "res": 0, "deb": 0}      # 3 Rotations to the left
    # ws.send(json.dumps(myDict))
    # receive()
    # dataForErrorAnalysisMotor2.append(ws.recv())
    # print(f"Motor2: {dataForErrorAnalysisMotor2}")
    # draw_plot(dataList, 3)
    # dataList.clear()


    # myDict = {"mot": 2, "pos": -1080, "res": 0, "deb": 0}       # 3 Rotations to the right
    # ws.send(json.dumps(myDict))
    # receive()
    # dataForErrorAnalysisMotor2.append(ws.recv())
    # print(f"Motor2: {dataForErrorAnalysisMotor2}")
    # draw_plot(dataList, 3)
    # dataList.clear()
    #
    #
    # myDict = {"mot": 2, "pos": 0, "res": 0, "deb": 0}        # 3 Rotations to the left
    # ws.send(json.dumps(myDict))
    # receive()
    # dataForErrorAnalysisMotor2.append(ws.recv())
    # print(f"Motor2: {dataForErrorAnalysisMotor2}")
    # draw_plot(dataList, 3)
    # dataList.clear()
    #
    #
    # myDict = {"mot": 3, "pos": 1080, "res": 0, "deb": 0}     # 3 Rotations to the right
    # ws.send(json.dumps(myDict))
    # receive()
    # dataForErrorAnalysisMotor3.append(ws.recv())
    # print(f"Motor3: {dataForErrorAnalysisMotor3}")
    # draw_plot(dataList, 3)
    # dataList.clear()
    #
    #
    # myDict = {"mot": 3, "pos": 0, "res": 0, "deb": 0}        # 3 Rotations to the left
    # ws.send(json.dumps(myDict))
    # receive()
    # dataForErrorAnalysisMotor3.append(ws.recv())
    # print(f"Motor3: {dataForErrorAnalysisMotor3}")
    # draw_plot(dataList, 3)
    # dataList.clear()
    #
    #
    # myDict = {"mot": 3, "pos": -1080, "res": 0, "deb": 0}      # 3 Rotations to the right
    # ws.send(json.dumps(myDict))
    # receive()
    # dataForErrorAnalysisMotor3.append(ws.recv())
    # print(f"Motor3: {dataForErrorAnalysisMotor3}")
    # draw_plot(dataList, 3)
    # dataList.clear()



ws.close()
print("... disconnected.")
# show_plots()

import json
import time

import paho.mqtt.client as mqtt
import requests

counter = 0
URL = "https://jsonplaceholder.typicode.com/posts"
threshold_flag = False
threshold = 50


def on_log(client, userdata, level, buf):
    print("log:" + buf)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK")
    else:
        print("Bad connection Returned code = " + rc)


def on_disconnect(client, userdata, flags, rc=0):
    print("Disconnected result code " + str(rc))


def on_message(client, userdata, msg):
    topic = msg.topic
    message = str(msg.payload.decode("utf-8", "ignore"))
    print("message received" + message)
    jsonM = json.loads(message)
    eval_data(jsonM, counter, threshold_flag)


def postNotification(URL, timestamp, sensorValue):
    postMessage = {"Treshold value exceeded":'', "lastSensorTimestamp":timestamp, "lastSensorValue":sensorValue}
    postMessageJson = json.dumps(postMessage)
    print("posting to: " + URL)
    r = requests.post(url=URL, data = postMessageJson)
    pastebin_url = r.text
    print("The pastebin URL is:%s" % pastebin_url)

def eval_data(msg, counter, threshold_flag):
    print("data is being evaluated")
    timestamp = msg["timestamp"]
    sensorValue = msg["value"]
    print("timestamp: " + timestamp)
    print("value: " + str(sensorValue))
    if sensorValue > threshold:
        threshold_flag = True
        print("warning!")
        counter = counter + 6
        print(counter)
        if counter > 5:
            postNotification(URL, timestamp, sensorValue)
    else:
        threshold_exceeded_flag = False
        print(counter)
    print(threshold_flag)


########################################

broker_address="test.mosquitto.org"
topic = "sensors/lyse-test-01"
print("creating new instance")
client = mqtt.Client("di", False) #create new instance
client.on_connect = on_connect
client.on_message = on_message #attach function to callback
#client.on_disconnect = on_disconnect
client.on_log = on_log

print("connecting to broker")
client.connect(broker_address) #connect to broker
client.loop_start()
print("Subscribing to topic: " + topic)
client.subscribe(topic)
time.sleep(1000) # wait
#client.loop_stop() #stop the loop

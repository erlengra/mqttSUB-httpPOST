import json
import logging
import requests
from config import *

counter = Counter()                                             # create counter instance
configure = Config()                                            # create configuration instance
options = configure.options                                     # create options variable
threshold = options["threshold"]                                # create threshold variable from options
url = options["post_to_url"]                                    # create url from options
timer = 3                                                       # timer threshold (non user specific)


'''
function for posting to json-server. This function should only be called when sensor values are above threshold and
no previous posts has been requested during the period above threshold or sensor value has been below threshold 
values for at least 5 min. 
When called the function activates the notify flag and resets the timer. 
The message is json formatted and sent to the local db.json file. 
The db.json will be synchronized  with the url address site using json-server application
The url will be displayed in terminal for debugging reasons.
Additional documentation: https://github.com/typicode/json-server
'''
def postNotification(url, sensorValue, timestamp):
    counter.NOTIFY = True
    counter.reset()
    postMessage = {"Treshold value exceeded": '',
                   "lastSensorTimestamp": timestamp,
                   "lastSensorValue": sensorValue}
    print("posting to: " + url)
    req = requests.post(url, data=postMessage)                          # create a post request and send to db.json
    _url_out = req.text                                                 # prepare url for print to terminal (debug)
    print("The pastebin URL is:%s" % _url_out)


'''
Function for evaluating the message acquired by mqtt broker. Uses the Counter class to hold and update 
counter value, reset, increment and flags.
Internal conditions are designed after assignment specifics.
'''
def eval_data(msg, counter):
    print("data is being evaluated")
    sensorValue = msg["value"]
    timestamp = msg["timestamp"]
    print("value: " + str(sensorValue))

    if sensorValue > options["threshold"]:
        counter.THRESHOLD_EXCEEDED = True
        print(counter.value)
        if counter.value > timer and not counter.NOTIFY:                # Condition for post request
            postNotification(url, sensorValue, timestamp)
        else:
            counter.increment()
    else:
        if counter.NOTIFY:
            counter.increment()
            if counter.value > timer:
                counter.NOTIFY = False
                counter.reset()
        counter.THRESHOLD_EXCEEDED = False
        print(counter.value)



'''
mqtt specific function. See paho documentation https://github.com/eclipse/paho.mqtt.python
'''
def on_log(client, userdata, level, buf):
    print("log:" + buf)



'''
mqtt specific function. See paho documentation https://github.com/eclipse/paho.mqtt.python
'''
def on_connect(client, userdata, flags, rc):
    logging.debug("Connected flags" + str(flags) +
                  "result code " + str(rc) + "client1_id")
    if rc == 0:
        print("connected OK")
        client.connected_flag = True
    else:
        print("Bad connection Returned code = " + rc)
        client.bad_connection_flag = True



'''
mqtt specific function. See paho documentation https://github.com/eclipse/paho.mqtt.python
'''
def on_disconnect(client, userdata, flags, rc=0):
    logging.debug("disconnecting reason  " + str(rc))
    client.connected_flag = False
    client.disconnect_flag = True
    client.subscribe_flag = False
    print("Disconnected result code " + str(rc))



'''
mqtt specific function. See paho documentation. https://github.com/eclipse/paho.mqtt.python
A json load is added to ease key extraction and generalize the message type.
The function will also run the eval_data function each time a message is received
from the mqtt broker.
'''
def on_message(client, userdata, msg):
    topic = msg.topic
    message = str(msg.payload.decode("utf-8", "ignore"))
    print("message received" + message)
    jsonM = json.loads(message)                                     # the message is loaded json
    eval_data(jsonM, counter)                                       # a call to evaluate the message received





    print("data is being evaluated")
    sensorValue = msg["value"]
    timestamp = msg["timestamp"]
    print("value: " + str(sensorValue))

    if sensorValue > options["threshold"]:
        counter.THRESHOLD_EXCEEDED = True
        print(counter.value)
        if counter.value > timer and not counter.NOTIFY:                # Condition for post request
            postNotification(url, sensorValue, timestamp)
        else:
            counter.increment()
    else:
        if counter.NOTIFY:
            counter.increment()
            if counter.value > timer:
                counter.NOTIFY = False
                counter.reset()
        counter.THRESHOLD_EXCEEDED = False
        print(counter.value)



'''
mqtt specific function. See paho documentation
'''
def on_log(client, userdata, level, buf):
    print("log:" + buf)



'''
mqtt specific function. See paho documentation
'''
def on_connect(client, userdata, flags, rc):
    logging.debug("Connected flags" + str(flags) +
                  "result code " + str(rc) + "client1_id")
    if rc == 0:
        print("connected OK")
        client.connected_flag = True
    else:
        print("Bad connection Returned code = " + rc)
        client.bad_connection_flag = True



'''
mqtt specific function. See paho documentation
'''
def on_disconnect(client, userdata, flags, rc=0):
    logging.debug("disconnecting reason  " + str(rc))
    client.connected_flag = False
    client.disconnect_flag = True
    client.subscribe_flag = False
    print("Disconnected result code " + str(rc))



'''
mqtt specific function. See paho documentation.
A json load is added to ease key extraction and generalize the message type.
The function will also run the eval_data function each time a message is received
from the mqtt broker.
'''
def on_message(client, userdata, msg):
    topic = msg.topic
    message = str(msg.payload.decode("utf-8", "ignore"))
    print("message received" + message)
    jsonM = json.loads(message)                                     # the message is loaded json
    eval_data(jsonM, counter)                                       # a call to evaluate the message received





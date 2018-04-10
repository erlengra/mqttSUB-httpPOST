import paho.mqtt.client as mqtt
from mqtt_handler import *
import sys
import time

configure = Config()                                            # create configuration instance
options = configure.options                                     # create option variable


topic = options["topic"]                                        # create topic variable from options
user = options["user"]                                          # create user variable from options
broker = options["broker"]                                      # create broker variable from options
port = options["port"]                                          # create port variable from options


def main():

    client = mqtt.Client(user, False)                           # create new client instance
    client.on_connect = on_connect                              # attach function to connection
    client.on_message = on_message                              # attach function to callback
    client.on_disconnect = on_disconnect                        # attach function to disconnection
    client.on_log = on_log                                      # attach function to log

    client.run_flag = True                                      # set condition for loop (unnecessary)

    while client.run_flag:
        print("connecting to broker")
        client.connect(broker)                                  # connect to broker
                                                                # loop until interrupted
        try:
            client.loop_start()                                 # start threaded loop
            client.subscribe(topic)                             # subscribe to topic
        except KeyboardInterrupt:
            print("interrrupted by keyboard")
            client.loop_stop()                                  # stop the loop
            client.disconnect()                                 # disconnect after loop stop
        time.sleep(1000)                                        # wait
        raise SystemExit(1)



if __name__ == "__main__" and len(sys.argv) >= 1:               # define main run condition
    options = configure.config_input(options)                   # create options variable from Config class
    main()
else:
    print("Need broker name and topics to continue.. ")
    raise SystemExit(1)     

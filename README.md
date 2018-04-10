# mqttSUB-httpPOST
This is a simple example on how to subscribe to an MQTT broker and selected topic, handle received data and further send warnings and notify to a designated url via http POST. The application utilizes a predefined topic at test.mosquitto.org which provides
(expired) a json formatted sensor and timestamp message every 10 sek. The application uses a threshold value (set in options) to determine the post action when sensor value exceedes threshold value for more than 5 minutes. 

## prerequisites
-json-server installed
-db.json file configured
-python 2.7 or later
-paho-mqtt package
-request package

## to run
-initiate json-server in terminal and make sure the db.json file is correctly defined and present in the json-server execution path.

-run python main.py with desired options. (broker and topic are required)
valid_options = --help <help> 
                -u <User>
                -h or -b <broker>
                -p <port>
                -t <topic>
                -n Client ID or Name
                -v <threshold>
                -a <URL> 

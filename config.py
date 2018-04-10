import sys
import getopt


'''
Config class used to hold all options available from runtime. The options are placed in a directory and loaded
to the initialization of the application. 

-configure_init() initializes the object
-config_input() returns a directory of options by using the sys class. options are set in the command terminal
'''
class Config(object):

    options = dict()                                                            # create the options dictionary
    options["user"] = "er"
    options["broker"] = "test.mosquitto.org"
    options["port"] = 1883
    options["topic"] = [("sensors/lyse-test-01", 0)]
    options["post_to_url"] = ""
    options["threshold"] = 0


    def configure_init(self, configure):
        self.configure = configure



    def config_input(self, options={}):
        valid_options = " --help <help> \
        -u <User>\
        -h or -b <broker>\
        -p <port>\
        -t <topic>\
        -n Client ID or Name\
        -v <threshold>\
        -a <URL> "

        try:
            opts, args = getopt.getopt(sys.argv[1:], "--help:u:h:p:t:n:v:a:")        # code borrowed from youtube.com
        except getopt.GetoptError:                                                   #
            print(sys.argv[0], valid_options)                                        #
            sys.exit(2)                                                              #
        qos = 0                                                                      #

        for opt, arg in opts:
            if opt == '-h':
                options["broker"] = str(arg)

            elif opt == '--help':
                print(valid_options)

            elif opt == "-b":
                options["broker"] = str(arg)

            elif opt == "-p":
                options["port"] = int(arg)

            elif opt == "-t":
                options["topic"] = str(arg)

            elif opt == "-u":
                options["user"] = str(arg)

            elif opt == "-a":
                options["post_to_url"] = str(arg)

            elif opt == "-v":
                options["threshold"] = int(arg)

        print("User: " + options["user"])                                      # very simple user feedback
        print("Broker: " + options["broker"])
        print("Port: " + str(options["port"]))
        print("Topic: " + str(options["topic"]))
        print("post_to_url: " + str(options["post_to_url"]))
        print("Threshold: " + str(options["threshold"]))
        print("\n")
        print("Configuration complete")
        print("\n")
        return options

#END OF CLASS: CONFIG



'''
The Counter class holds necessary functions and variables for the counter used in the eval_data function. 
Notify is a flag to determine if a post request has been sent.
Threshold_exceeded is a flag to determine if the sensor value has surpassed the user specific threshold value.
value holds the current counter value

-Init() initializes the instance
-Increment() increases the value by 1
-Reset() resets the value to 0  

'''
class Counter:

    NOTIFY = False
    THRESHOLD_EXCEEDED = False
    value = 0

    def counter_init(self, counter):
        self.counter = counter


    def increment(self):
        self.value += 1


    def reset(self):
        self.value = 0

#END OF CLASS: COUNTER

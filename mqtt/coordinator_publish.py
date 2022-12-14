
"""
* This code creates sensor client for MQTT
* Sets up an MQTT Broker
* Publishes the sensor values to MQTT Broker
* Simulates an MQTT publishing

"""
#* to read json file
import datetime
import json
#* to create delay (additionally)
import time
#* to create a client and connect to broker
from paho.mqtt import client as mqtt_client
#* to use tls
from paho import mqtt
#* to get cpu heat
#* just some make-up
import sys

#* Gets broker info from json file
broker_ = json.load(open("./broker.json"))

#* Gives client we created an id and identify publishing topic
client_id = "000"

def connect_mqtt():

    #* RC returns either zero or one due to connection status
    def on_connect(client, userdata, flags, rc):
        if rc==0:
            print("Successfully connected to MQTT broker")
        else:
            print("Failed to connect, return code %d", rc)
 
    #* set as a client (node)
    client = mqtt_client.Client(client_id)

    #* enable TLS for secure connection
    #* some mqtt broker services use this
    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

    #* Broker login infos
    client.username_pw_set(broker_["username"], broker_["password"])
    client.on_connect = on_connect
    client.connect(broker_["broker"], broker_["port"])
    return client

#* 
def publish(client):
     message_send = 0
     message_fail = 0

     message = None
     while True:
        with open("C:\\Users\\tinrafiq\\Documents\\xx\\results\\SINK_7", "r") as file:
            last_line = file.readlines()[-1]
        if last_line == message:
            pass

        else:
            message = last_line
            topic = "xbee"
            #* sensor_id, generated_time, value, saved_time, send_time
            msg = last_line + " " + str(datetime.datetime.now().time())
            result = client.publish(topic, msg, qos=0)
            #* result: [0, 1]
            status = result[0]
            if status == 0:
                # print(f"Send `{msg}` to topic `{topic}`")
                message_send +=1
            else:
                # print(f"Failed to send message to topic {topic}")
                message_fail +=1

        time.sleep(0.001)

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)

if __name__ == '__main__':
    try:
        run()

    except KeyboardInterrupt:
        print("\nPrograms was stopped")  
        sys.exit()




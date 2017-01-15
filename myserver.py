#!/usr/bin/python
import paho.mqtt.client as mqtt
import time

labState = 0;

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("labOpenButton")
    client.subscribe("temperature")
    client.subscribe("humidity")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if(msg.topic == "labOpenButton"):
	if (msg.payload[0] == "0"):
	    client.publish("labStatus", "0")
	    labState = 0;
	    file = open("/home/pi/web/islabopen/labStatus.txt", "w")
	    file.write("It's CLOSED!")
	    file.close()
	else:
	    client.publish("labStatus", "1")
	    labState = 1;
	    file = open("/home/pi/web/islabopen/labStatus.txt", "w")
	    file.write("It's OPEN!")
	    file.close()
	file = open("/home/pi/web/islabopen/labStatusUpdateTime.txt", "w")
	file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
	file.close()
    elif(msg.topic == "temperature"):
        file = open("/home/pi/web/base/temperature.txt", "w")
        file.write(str(msg.payload))
        file.close()
	file = open("/home/pi/web/base/lastUpdatedTime.txt", "w")
	file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
	file.close()
    elif(msg.topic == "humidity"):
        file = open("/home/pi/web/base/humidity.txt", "w")
        file.write(str(msg.payload))
        file.close()
	file = open("/home/pi/web/base/lastUpdatedTime.txt", "w")
	file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
	file.close()


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.loop_forever()


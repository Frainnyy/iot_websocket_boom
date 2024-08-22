import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
led_pin = 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)

def on_connect(client, userdata, flags, rc):
   print("Connected with result code "+str(rc))
   client.subscribe("rain/led")

def on_message(client, userdata, msg):
   print(msg.topic+" "+str(msg.payload))
   mesg = msg.payload
   print(mesg.decode())
   if msg.payload.decode() == "ON":
        GPIO.output(led_pin, GPIO.HIGH)  #LED
        print("LED is ON")
   elif msg.payload.decode() == "OFF":
        GPIO.output(led_pin, GPIO.LOW)  #LED
        print("LED is OFF")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("mqtt-dashboard.com", 1883)
client.loop_forever()

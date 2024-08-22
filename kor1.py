import asyncio
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

switch_pin = 4

mqttc = mqtt.Client()
mqttc.connect("mqtt-dashboard.com", 1883)

GPIO.setmode(GPIO.BCM)
GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def read_switch():
    return GPIO.input(switch_pin)

async def send_switch_data():
    last_state = GPIO.HIGH  # Initial state is HIGH (button not pressed)
    while True:
        switch_state = read_switch()
        if switch_state == GPIO.LOW and last_state == GPIO.HIGH:  # Check if button is pressed
            mqttc.publish("rain/swpub", "ON")  # Publish ON message when button is pressed
            print("Switch Pressed - State ON")
        last_state = switch_state
        time.sleep(0.1)  # Short delay to debounce the button

asyncio.get_event_loop().run_until_complete(send_switch_data())

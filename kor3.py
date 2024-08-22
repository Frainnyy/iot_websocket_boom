import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

led_pin = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("rain/temp")

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"Message from {msg.topic}: {payload}")
    if payload == "on":
        pwm.stop()
        GPIO.output(led_pin, GPIO.HIGH)
        print("LED is ON")
    elif payload == "off":
        pwm.stop()
        GPIO.output(led_pin, GPIO.LOW)
        print("LED is OFF")
    elif payload.isdigit():
        pwm_value = int(payload)
        pwm.ChangeDutyCycle(pwm_value)
        print(f"LED brightness set to {pwm_value}")
        pwm.start(pwm_value)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt-dashboard.com", 1883)

pwm = GPIO.PWM(led_pin, 100)

client.loop_forever()

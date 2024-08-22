import spidev
import time
import asyncio
import paho.mqtt.client as mqtt

mqttc = mqtt.Client()
mqttc.connect("mqtt-dashboard.com", 1883)

def read_adc(channel):
    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.max_speed_hz = 1350000
    adc = spi.xfer2([6 | (channel & 4) >> 2, (channel & 3) << 6, 0])
    data = ((adc[1] & 15) << 8) + adc[2]
    spi.close()
    return data

async def send_potentiometer_data():
 while True:
  pot_value = read_adc(0)
  print(f"Potentiometer Value: {pot_value}")
  mqttc.publish("rain/pm25", pot_value)
  time.sleep(1)

asyncio.get_event_loop().run_until_complete(send_potentiometer_data())

import time
from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor
from counterfit_shims_grove.grove_led import GroveLed
import paho.mqtt.client as mqtt
import json

CounterFitConnection.init('127.0.0.1', 5000)

light_sensor = GroveLightSensor(0)
led = GroveLed(5)

id = 'lffwan'

client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/command' # 要订阅的主题
client_name = id + 'nightlight_client'

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()

print("MQTT connected!")

while True:
    light = light_sensor.light
    telemetry = json.dumps({'light' : light})

    print("Sending telemetry ", telemetry)

    mqtt_client.publish(client_telemetry_topic, telemetry)

    time.sleep(5)

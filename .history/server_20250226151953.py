import json
import time

import paho.mqtt.client as mqtt

id = 'lffwan'

client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/command'
client_name = id + '_nightlight_server'

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()


def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)

    command = json.dumps({'led_on': payload['light'] < 300})
    print("Sending command:", command)
    


mqtt_client.subscribe(client_telemetry_topic)
mqtt_client.on_message = handle_telemetry

while True:
    time.sleep(2)

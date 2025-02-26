import time
from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor
from counterfit_shims_grove.grove_led import GroveLed

import paho.mqtt.client as mqtt
import json

CounterFitConnection.init('127.0.0.1', 5000)

light_sensor = GroveLightSensor(0)
led = GroveLed(5)

id = 'dsa65d45sa6d456sad4'
client_name = id+'nightlight_client'  # 客户端名称
client_telemetry_topic = id+'/telemetry'  # 客户端遥测主题
server_command_topic = id+'/commands'  # 服务器命令主题

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()
print('Connected to MQTT broker!')


def handle_telemetry(client: mqtt.Client, userdata, msg):
    payload = json.loads(msg.payload.decode()) # msg: 传感器->broker->客户端
    print('Message received:', payload)

    command = {'led_on': payload['light'] < 300}
    print('Sending command:', command)
    client.publish(server_command_topic, json.dumps(command)) # command: 客户端->broker->灯

mqtt_client.subscribe(client_telemetry_topic) # 订阅遥测主题
mqtt_client.on_message = handle_telemetry # 根据遥测主题处理消息

while True:
    # light = light_sensor.light
    # print('Light:', light)
    # led.on() if light < 300 else led.off()

    # telemetry = {'light': light}
    # print('Sending telemetry:', telemetry)
    # mqtt_client.publish(client_telemetry_topic, json.dumps(telemetry))

    time.sleep(1)
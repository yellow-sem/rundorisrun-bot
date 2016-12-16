#!python3 -tt
# -*- coding: utf-8 -*-

import json
from paho.mqtt import client as mqtt
from time import sleep
from datetime import timedelta

MQTT_HOST = 'prata.technocreatives.com'
MQTT_PORT = 1883

BOT_ID = 'rdr'

TOPIC_RDR = 'thehub/rundorisrun/score/gethighscores'
TOPIC_BOT = 'yellow/bot/rdr/outgoing'

def on_connect(client, userdata, rc):
    print('Connected')
    client.subscribe(TOPIC_RDR)

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    print('Message received {}'.format(data))
    if not isinstance(data, list):
        return
    message = '<br/>'.join([
        '{} Level: {} Score: {}'.format(item['Score_ID'],
                                        item['Level_ID'],
                                        item['Score'])
        for item in data
    ])
    print('Sending to bot: "{}"'.format(message))
    client.publish(TOPIC_BOT, message)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print('Connecting')
client.connect(MQTT_HOST, MQTT_PORT, 60)

client.loop_start()

while True:
    print('Requesting scores')
    client.publish(TOPIC_RDR, json.dumps({'Level': 1}))
    sleep(timedelta(hours=1).total_seconds())

client.loop_stop()

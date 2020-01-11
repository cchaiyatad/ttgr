import paho.mqtt.client as mqtt
import time
import socket
import urllib.request
import json
from datetime import datetime

id = 'Vorapojpisut'
topic = '/tgr2020/jan08/data/99'
fburl = 'https://tgr2020-ble-location.firebaseio.com/jan08/morning.json'
payload = None

def on_connect(client, userdata, flags, rc):
    client.subscribe(topic)
    print('Subscribed')
    
def on_message(client, userdata, msg):
    global payload
    print(msg.topic, ':', msg.payload)
    payload = json.loads(msg.payload)
    payload['topic'] = msg.topic
    payload['timestamp'] = str(datetime.now())

def on_disconnect(client, userdata, rc):
    print(userdata)
    
client = mqtt.Client(client_id=id)
client.connect('202.139.192.75')
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.socket().setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2048)
client.loop_start()

while True:
    if payload is not None:
        print('Sending to Firebase')
        headers = {'Content-Type': 'application/json'}
        req = urllib.request.Request(fburl, json.dumps(payload).encode('utf-8'), headers)
        with urllib.request.urlopen(req) as resp:
            print(resp.read())
        payload = None
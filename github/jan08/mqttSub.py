import paho.mqtt.client as mqtt
import time
import socket

id = 'Vorapojpisut'
topic = '/tgr2020/pm25/data/44'

def on_connect(client, userdata, flags, rc):
    client.subscribe(topic)
    print('Subscribed')
    
def on_message(client, userdata, msg):
    print(msg.topic, ':', msg.payload)

def on_disconnect(client, userdata, rc):
    print(userdata)
    
client = mqtt.Client(client_id=id)
client.connect('202.139.192.75')
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.socket().setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2048)
client.loop_forever()

while True:
    time.sleep(10)
    print('Waiting')
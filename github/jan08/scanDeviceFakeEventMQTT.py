import asyncio
from time import sleep
from bleak import discover
import paho.mqtt.client as mqtt
import json
from datetime import datetime

id = ?
topic = ?

async def scan(mac_addrs, queue):
    while True:
        print('Start scanning')
        tstart = loop.time()
        devices = await discover()
        print('Found %d devices'%(len(devices)))
        for dev in devices:
            dev_mac = str(dev).split(': ')[0]
            print(dev_mac)
            if dev_mac in mac_addrs:                
                print(dev_mac, 'detected at', dev.rssi, 'dBm')
                evt_code = 0
                now = datetime.now()
                queue.put_nowait({'mac_addr':dev_mac, 'rssi':dev.rssi, 'timestamp':str(now), 'event_code':evt_code})
        telapsed = loop.time() - tstart
        print('Elapsed time: %.1f'%(telapsed))
        await asyncio.sleep(15 - telapsed)

def on_connect(client, userdata, flags, rc):
    print('MQTT connected')
    
def on_message(client, userdata, msg):
    print(msg.payload)

def on_disconnect(client, userdata, rc):
    print(userdata)

async def publish(queue):
    client = mqtt.Client(client_id=id)
    client.connect('202.139.192.75')
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.loop_start()
    print('Start MQTT publisher')
    while True:
        val = await queue.get()
        print('Forwarding', val)
        client.publish(topic, json.dumps(val), qos=1)
        await asyncio.sleep(1)
    mqtt.loop_stop()

if __name__ == '__main__':
    mac_addrs = ("80:E1:26:07:C8:FB", "80:E1:26:00:66:5F", "80:E1:26:00:62:97")
    loop = asyncio.get_event_loop()
    queue = asyncio.Queue()
    loop.create_task(scan(mac_addrs, queue))
    loop.create_task(publish(queue))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.close()
        print('Program stopped')
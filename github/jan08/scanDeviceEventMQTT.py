import asyncio
from time import sleep
from bleak import discover
from bleak import BleakClient
import paho.mqtt.client as mqtt
import json
from datetime import datetime

id = ?
topic = ?

evt_list = list()

SERV_UUID = ('00000000-0001-11E1-9AB4-0002A5D5C51B')
CHAR_UUID = ('0000AACC-8e22-4541-9d4c-21edae82ed19')
NOTI_UUID = ('00040000-0001-11E1-AC36-0002A5D5C51B')

def notification_handler(sender, data):
    """Simple notification handler which prints the data received."""
    global evt_list
    evt_list.append(int.from_bytes(data[2:4], byteorder='little'))
    print("{0}: {1}".format(sender, data))

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
                async with BleakClient(dev_mac, loop=loop) as client:
                    global evt_list
                    evt_list = list()
                    flag = await client.is_connected()
                    await client.start_notify(NOTI_UUID.lower(), notification_handler)
                    await asyncio.sleep(10, loop=loop)
                    await client.stop_notify(NOTI_UUID.lower())
                    now = datetime.now()
                    print(evt_list)
                    if len(evt_list) > 0:
                        evt_code = max(evt_list);
                    else:
                        evt_code = 0
                    queue.put_nowait({'mac_addr':dev_mac, 'rssi':dev.rssi, 'timestamp':str(now), 'event_code':evt_code})
                del client
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
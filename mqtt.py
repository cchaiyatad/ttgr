import asyncio
from time import sleep
from bleak import discover
from bleak import BleakClient
import paho.mqtt.client as mqtt
import json
from datetime import datetime

id = 'downgun'
topic = '/tgr2020/jan08/data/17'
macQueue = ''
rssiQueue = 0

evt_list = list()
queue = asyncio.Queue()

SERV_UUID = ('00000000-0001-11E1-9AB4-0002A5D5C51B')
CHAR_UUID = ('0000AACC-8e22-4541-9d4c-21edae82ed19')
NOTI_UUID = ('00040000-0001-11E1-AC36-0002A5D5C51B')
mapping = {
    2048: "Dead",
    4352: "Alive",
    32768: "Fall"
}


def notification_handler(sender, data):
    """Simple notification handler which prints the data received."""
    global evt_list
    global queue
    eventCode = int.from_bytes(data[2:4], byteorder='little')

    if (eventCode == 4352):
        if (len(evt_list) < 1):
            return
        evt_list = list()
        print("Alive")

    if (eventCode in evt_list):
        return

    evt_list.append(eventCode)
    now = str(datetime.now())
    print("mac_addr:{0} rssi:{1} timeStamp:{2} event_code:{3} event:{4}".format(macQueue, rssiQueue, now, eventCode,
                                                                                mapping[eventCode]))

    queue.put_nowait({'mac_addr': macQueue, 'rssi': rssiQueue, 'timestamp': now, 'event_code': eventCode})


async def scan(mac_addrs, queue):
    while True:
        print('Start scanning')
        tstart = loop.time()
        devices = await discover()
        print('Found %d devices' % (len(devices)))
        for dev in devices:
            dev_mac = str(dev).split(': ')[0]
            # print(dev_mac)
            if dev_mac in mac_addrs:
                print(dev_mac, 'detected at', dev.rssi, 'dBm')
                try:
                    async with BleakClient(dev_mac, loop=loop) as client:
                        global evt_list
                        global macQueue
                        global rssiQueue

                        macQueue = dev_mac
                        rssiQueue = dev.rssi

                        evt_list = list()

                        flag = await client.is_connected()
                        await client.start_notify(NOTI_UUID.lower(), notification_handler)
                        while True:
                            await asyncio.sleep(3, loop=loop)
                            isConnect = await client.is_connected()
                            if (not isConnect):
                                break

                        # await client.stop_notify(NOTI_UUID.lower())
                    # del client
                except Exception:
                    print("Error", flag)
        telapsed = loop.time() - tstart
        print('Elapsed time: %.1f' % (telapsed))
        waitTime = 10 - telapsed if 10 - telapsed > 0 else 0
        await asyncio.sleep(waitTime)


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
    client.loop_stop()


if __name__ == '__main__':
    mac_addrs = ("80:E1:26:00:B4:04")
    loop = asyncio.get_event_loop()
    queue = asyncio.Queue()
    loop.create_task(scan(mac_addrs, queue))
    loop.create_task(publish(queue))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.close()
        print('Program stopped')

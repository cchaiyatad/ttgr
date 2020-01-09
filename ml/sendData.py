import asyncio
from datetime import datetime
from time import sleep
from bleak import discover


def writeFile(data_mac, data_rssi, timestamp, label):
    f = open("data.csv", "a")
    f.write(data_mac + ", " + str(data_rssi) + ", " + str(timestamp) + ", " + str(label) + "\n")
    f.close()


async def scan(mac_addrs):
    while True:
        print('Start scanning')
        tstart = loop.time()
        devices = await discover()
        print('Found %d devices' % (len(devices)))
        label = 14
        for dev in devices:
            dev_mac = str(dev).split(': ')[0]
            if dev_mac in mac_addrs:
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                print(dev_mac, 'detected at', dev.rssi, 'dBm', 'at time', current_time, 'label', label)
                writeFile(dev_mac, dev.rssi, current_time, label)
        telapsed = loop.time() - tstart
        print('Elapsed time: %.1f' % (telapsed))
        await asyncio.sleep(10 - telapsed)


if __name__ == '__main__':
    mac_addrs = ("80:E1:26:07:C9:51", "80:E1:26:00:B4:04", "80:E1:25:00:D6:D7", "80:E1:26:07:C8:B0")

    loop = asyncio.get_event_loop()
    loop.create_task(scan(mac_addrs))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.close()
        print('Program stopped')

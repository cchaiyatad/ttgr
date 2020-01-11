import asyncio
from time import sleep
from bleak import discover

def writeFile(data_mac, data_rssi):
    f = open("data.csv", "a")
    f.write(data_mac + ", " + str(data_rssi) +"\n")
    f.close()


async def scan(mac_addrs):
    while True:
        print('Start scanning')
        tstart = loop.time()
        devices = await discover()
        print('Found %d devices'%(len(devices)))
        for dev in devices:
            dev_mac = str(dev).split(': ')[0]
            if dev_mac in mac_addrs:
                print(dev_mac, 'detected at', dev.rssi, 'dBm')
                writeFile(dev_mac, dev.rssi)
        telapsed = loop.time() - tstart
        print('Elapsed time: %.1f'%(telapsed))
        await asyncio.sleep(10 - telapsed)

if __name__ == '__main__':
    mac_addrs = ("80:E1:26:07:C9:51", "80:E1:26:00:B4:04", "80:E1:25:00:D6:D7", "80:E1:26:07:C8:B0")
   
    f = open("data.csv", "w")
    f.write("mac, rssi\n")
    f.close()

    loop = asyncio.get_event_loop()
    loop.create_task(scan(mac_addrs))
    queue = asyncio.Queue()
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.close()
        print('Program stopped')
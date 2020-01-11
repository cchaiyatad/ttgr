import asyncio
from time import sleep
from bleak import discover

async def scan():
    while True:
        print('Start scanning')
        tstart = loop.time()
        devices = await discover()
        print('Found %d devices'%(len(devices)))
        for dev in devices:
            print(dev)
        telapsed = loop.time() - tstart
        print('Elapsed time: %.1f'%(telapsed))
        await asyncio.sleep(10 - telapsed)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(scan())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.close()
        print('Program stopped')

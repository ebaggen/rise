from device_coordinator.drivers.hue import HueDriver
from device_coordinator.drivers.sonos import SonosDriver
from device_coordinator.drivers.ifttt import IFTTTDriver
import time

hue = HueDriver(60, '192.168.0.59')
sonos = SonosDriver(30, '192.168.0.109')
ifttt = IFTTTDriver()

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        quit()
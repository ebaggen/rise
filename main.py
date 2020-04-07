from hub.device_engines.hue import HueDriver
from hub.device_engines.sonos import SonosDriver
from hub.device_engines.ifttt import IFTTTDriver
import time

hue = HueDriver(60, '192.168.0.59')
sonos = SonosDriver(30, '192.168.0.109')
ifttt = IFTTTDriver()

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        quit()
# UDP Proxy import & define
import time
from socket import *
from datetime import datetime
import json

from sense_hat import SenseHat

waterBool = 0

BROADCAST_TO_PORT = 6666

minutes = 10

sense = SenseHat()
sense.clear()


def get_mac(interface='wlan0'):
    try:
        mac = open('/sys/class/net/%s/address' % interface).read()
    except:
        mac = "00:00:00:00:00:00"
    return mac[0:17]


# UDP Proxy Broadcast
s = socket(AF_INET, SOCK_DGRAM)
s.bind(('', 6666 + 1))     # (ip, port)
# no explicit bind: will bind to default IP + random port
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
while True:
    humidity = sense.get_humidity()

    jsonObj = {
        "fk_macaddress": str(get_mac()),
        "humidity": str(humidity),
        "date": str(datetime.now())
    }

    data = json.dumps(jsonObj)
    s.sendto(bytes(data, "UTF-8"), ('<broadcast>', BROADCAST_TO_PORT))
    time.sleep(60)
    water = s.recvfrom(1024)
    time.sleep(60 * minutes)


# UDP Proxy import & define
import time
from socket import *
from datetime import datetime
import json

from sense_hat import SenseHat

globalRecPort = 6000
sensorRecPort = 0

shouldWater = 0

BROADCAST_TO_PORT = 6666

minutes = 10

sense = SenseHat()
sense.clear()


def water_now():
    print("Watering!")


def get_mac(interface='wlan0'):
    try:
        mac = open('/sys/class/net/%s/address' % interface).read()
    except:
        mac = "00:00:00:00:00:00"
    return mac[0:17]


if sensorRecPort == 0:
    s1 = socket(AF_INET, SOCK_DGRAM)
    s1.bind(('', globalRecPort))
    s1.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    s1.sendto(bytes(str(get_mac()), "UTF-8"), ('<broadcast>', BROADCAST_TO_PORT))
    time.sleep(2)
    jsonObj1 = str(s1.recvfrom(1024))
    splitObj = jsonObj1.split("'")
    portObj = json.loads(splitObj[1])
    if portObj["macAddress"] == str(get_mac()):
        sensorRecPort = int(portObj["port"])
        print("New port set!")


if sensorRecPort != 0:
    s2 = socket(AF_INET, SOCK_DGRAM)
    s2.bind(('', sensorRecPort))
    s2.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    while True:
            print("Check if you are too dry and should water!")
            humidity = sense.get_humidity()

            jsonObj2 = {
                "fk_macaddress": str(get_mac()),
                "humidity": str(humidity),
                "date": str(datetime.now())
            }

            data = json.dumps(jsonObj2)
            s2.sendto(bytes(data, "UTF-8"), ('<broadcast>', BROADCAST_TO_PORT))
            time.sleep(5)
            jsonObjStr = str(s2.recvfrom(1024))
            splitObj2 = jsonObjStr.split("'")
            shouldWater = int(splitObj2[1])
            if shouldWater == 1:
                water_now()
            time.sleep(60 * minutes)



import sys
import time
import threading
import pynmea2
import os
from pprint import pprint
from datetime import datetime

import Adafruit_DHT

from pypact import api
from pypact.adapters import BasePactAdapter


sample_freq = 10  # 20 minutes in seconds
sensor = Adafruit_DHT.DHT22
pin = 16


def format_current_time():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")


def read_sensor_data():
    """Read humidity and temperature from the sensor and returns it"""
    humidity, temp = Adafruit_DHT.read_retry(sensor, pin)
    if temp and humidity:
        return temp, humidity
    return "Failed to read sensor data!"


def send_sensor_data(temp, humidity, latitude, longitude):
    """Sends data to pact server to be saved on blockchain"""
    code = BasePactAdapter.build_code(
        "raspberrypi",
        "update-temp-humidity-gps",
        "admin-keyset",
        **{"temp": temp, "humidity": humidity,
           "latitude": latitude, "longitude": longitude,
           "keyset_name": "admin-keyset",
           "time": format_current_time()}
    )
    print(code)
    result = api.send_and_listen(code, "admin-keyset")
    print(result)


def print_log():
    code = BasePactAdapter.build_code(
        "raspberrypi",
        "logs",
        "admin-keyset"
    )
    print(code)
    result = api.send_and_listen(code, "admin-keyset")
    pprint(result, indent=2)

class Message:
    def __init__(self):
        self.msg =''

# Gps Receiver thread funcion, check gps value for infinte times
def getgpsdata(serial, dmesg):
    print("getgpsdata")
    while True:
        data = serial.readline()
        if data.find('GGA') > 0:
            dmesg.msg = pynmea2.parse(data)

# API to call start the GPS Receiver
def start_gps_receiver(serial, dmesg):
    t2 = threading.Thread(target=getgpsdata, args=(serial, dmesg))
    t2.start()
    print("GPS Receiver started")

# API to fix the GPS Revceiver
def ready_gps_receiver(msg):
    print("Please wait fixing GPS .....")
    dmesg = msg.msg
    while(dmesg.gps_qual != 1):
        pass
    print("GPS Fix available")

# API to get latitude from the GPS Receiver
def get_latitude(msg):
    print("Getting Latitude")
    dmesg = msg.msg
    print("Latitude:", dmesg.latitude)

# API to get longitude from the GPS Receiver
def get_longitude(msg):
    print("Getting Longitude")
    dmesg = msg.msg
    print("Longitude:", dmesg.longitude)

# API to get Number of Satellites from the GPS Receiver
def get_num_satellite(msg):
    print("Getting Number of satellite")
    dmesg = msg.msg
    print("No of satellites:", dmesg.num_sats)

# API to get Altitude of Antenna from the GPS Receiver
def get_altitude(msg):
    print("Getting altitude of Antenna")
    dmesg = msg.msg
    print("Altitude (M):", dmesg.altitude)

# API to check the status of GPS Fix
def get_gps_fix(msg):
    dmesg = msg.msg
    print("GPS Fix stats:", dmesg.gps_qual)

# API to Exit
def function_exit(msg):
    print("Exiting ......")
    print("stopping the thread")
    exit()
    return 1
msgdata = Message() # Creates a Message Instance

def main():
    while True:
        temp, humidity = read_sensor_data()
        start_gps_receiver(ser, msgdata)
        print(msgdata.msg)
        ready_gps_receiver(msgdata)
        latitude = get_latitude(msgdata.msg)
        longitude = get_longitude(msgdata.msg)
        send_sensor_data(temp, humidity, latitude, longitude)
        time.sleep(sample_freq)


if __name__ == "__main__":
    try:
        print_log()
        main()
    except KeyboardInterrupt:
        print("\n", "Stopping script...")
        sys.exit()

import sys
import time
import threading
import pynmea2
import serial, string
import os
from pprint import pprint
from datetime import datetime
from GPS_API import *

import Adafruit_DHT

from pypact import api
from pypact.adapters import BasePactAdapter

ser = serial.Serial("/dev/ttyAMA0")  # Select your Serial Port
ser.baudrate = 9600  # Baud rate
ser.timeout = 50
msgdata = Message() # Creates a Message Instance

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

import sys
import time
import webbrowser
import serial
import string
import os
from pprint import pprint
from datetime import datetime

import pynmea2
import Adafruit_DHT

from pypact import api
from pypact.adapters import CommandFactory


sample_freq = 5  # 20 minutes in seconds
sensor = Adafruit_DHT.DHT22
pin = 16

ser = serial.Serial("/dev/ttyUSB0")  # Select your Serial Port
ser.baudrate = 9600  # Baud rate
ser.timeout = 50
ser.timeout = 1


def format_current_time():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")


def quote_string(value):
   return f'"{str(value)}"'


def read_sensor_data():
    """Read humidity and temperature from the sensor and returns it"""
    humidity, temp = Adafruit_DHT.read_retry(sensor, pin)
    if temp and humidity:
        return temp, humidity
    return "Failed to read sensor data!"


def send_sensor_data(temp, humidity, latitude, longitude):
    """Sends data to pact server to be saved on blockchain"""
    print(latitude, longitude)
    code = CommandFactory(
        "update-temp-humidity-gps",
        "raspberrypi",
        **{"temp": str(temp),
           "humidity": str(humidity),
           "latitude": str(latitude),
           "longitude": str(longitude),
           "time": '(time "%s")' %format_current_time(),
           "keyset_name": quote_string("admin-keyset")}
    ).build_code()
    print(code)
    result = api.send_and_listen(code, "admin-keyset")
    print(result)


def print_log():
    code = CommandFactory(
        "logs",
        "raspberrypi"
    ).build_code()
    print(code)
    result = api.send_and_listen(code, "admin-keyset")
    pprint(result, indent=2)


def open_gmaps(GPS_coordinates):
    gmaps = 'http://www.google.com/maps/place/'
    webbrowser.open(gmaps + GPS_coordinates)

       
def main():
    while True:
        temp, humidity = read_sensor_data()
        if ser.inWaiting() > 0 :
            recv=ser.readline().decode('utf-8')
            #print(recv)
            if recv.find('$GPGGA')!=-1:
                msg = pynmea2.parse(recv)
                #print (msg.timestamp)
                latitude = str(msg.latitude)
                longitude = str(msg.longitude)
                
                if msg.lat_dir == 'S':
                    latitude = '-' + latitude
                if msg.lon_dir == 'W':
                    longitude = '-' + longitude
                
                send_sensor_data(temp, humidity, latitude, longitude)
                open_gmaps(latitude + ',' + longitude)
        time.sleep(sample_freq)


if __name__ == "__main__":
    try:
        print_log()
        main()
    except KeyboardInterrupt:
        print("\n", "Stopping script...")
        sys.exit()

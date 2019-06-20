import sys
import time
import webbrowser
import serial
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


def format_current_time():
    """
    Format current time for pact
    :return:
    """
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")


def quote_string(value):
    """
    Add quotes to the value
    :param value:
    :return: quoted string value
    """
    return f'"{str(value)}"'


def read_sensor_data():
    """
    Read humidity and temperature from sensor
    :return: temp, humidity or "Failed to read sensor data!"
    """
    humidity, temp = Adafruit_DHT.read_retry(sensor, pin)
    if temp and humidity:
        return temp, humidity
    return "Failed to read sensor data!"


def send_sensor_data(temp, humidity, latitude, longitude):
    """
    Send data to pact server to be saved on blockchain
    :param temp:
    :param humidity:
    :param latitude:
    :param longitude:
    :return: None
    """
    current_time = format_current_time()
    code = CommandFactory(
        "update-temp-humidity-gps",
        "raspberrypi",
        **{"temp": str(temp),
           "humidity": str(humidity),
           "latitude": str(latitude),
           "longitude": str(longitude),
           "time": f'(time "{current_time}")',
           "keyset_name": quote_string("admin-keyset")}
    ).build_code()
    result = api.send_and_listen(code, "admin-keyset")
    print(f'temperature: {temp} humidity: {humidity} latitude: {latitude} '
          f'longitude: {longitude} time: {current_time}')
    print(result)


def read_gps_data():
    """
    Read GPS data from serial port. If could't read GPS data returns None
    :return: gps_data or None
    """
    try:
        gps_data = ser.readline().decode('utf-8')
        return gps_data
    except UnicodeDecodeError:
        print("Could not read GPS data")


def parse_gps_data(gps_data):
    """
    Parse gps data, transform latitude and longitude for google maps
    to show exact location.
    :param gps_data:
    :return: latitude, longitude
    """
    msg = pynmea2.parse(gps_data)
    # print(msg.timestamp)
    latitude = str(msg.latitude)
    longitude = str(msg.longitude)

    if msg.lat_dir == 'S':
        latitude = '-' + latitude
    if msg.lon_dir == 'W':
        longitude = '-' + longitude
    return latitude, longitude


def open_google_maps(coordinates):
    """
    Open google maps on the browser with the coordinates
    :param coordinates:
    :return: None
    """
    webbrowser.open('http://www.google.com/maps/place/' + coordinates)


def print_historical_data():
    """
    Print data stored on Blockchain in a pretty format
    :return: None
    """
    print(30 * "=")
    print("  Historical data on Blockchain")
    print(30 * "=")
    code = CommandFactory(
        "logs",
        "raspberrypi"
    ).build_code()
    print(code)
    result = api.send_and_listen(code, "admin-keyset")
    pprint(result, indent=2)
    print(30 * "=")


def main():
    """
    Loop infinite, call read_sensor_data(), read_gps_data() functions and
    send their data to Blockchain. Call open_google_maps() to show coordinates
     on google maps. Wait for sample freq.
    :return: None
    """
    print("Starting to record humidity, temperature and GPS data on Blockchain...")
    print()
    while True:
        temp, humidity = read_sensor_data()
        if ser.inWaiting() > 0:
            gps_data = read_gps_data()
            if gps_data is None:
                continue
            if gps_data.find('$GPGGA') != -1:
                latitude, longitude = parse_gps_data(gps_data)
                send_sensor_data(temp, humidity, latitude, longitude)
                open_google_maps(latitude + ',' + longitude)
        time.sleep(sample_freq)


if __name__ == "__main__":
    args = sys.argv
    show_history = False
    if len(args) >= 2:
        show_history = True
    try:
        if show_history:
            print_historical_data()
        else:
            main()
    except KeyboardInterrupt:
        print("\n", "Stopping script...")
        sys.exit()

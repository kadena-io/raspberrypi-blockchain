import sys
import time
import datetime

import Adafruit_DHT

from pypact import api
from pypact.adapters import BasePactAdapter


sample_freq = 2  # 20 minutes in seconds
sensor = Adafruit_DHT.DHT22
pin = 16


def format_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")


def read_sensor_data():
    """Read humidity and temperature from the sensor and returns it"""
    temp, humidity = Adafruit_DHT.read_retry(sensor, pin)
    if temp and humidity:
        return temp, humidity
    return "Failed to read sensor data!"


def send_sensor_data(temp, humidity):
    """Sends data to pact server to be saved on blockchain"""
    code = BasePactAdapter.build_code(
        "raspberrypi",
        "update-temp-humidity",
        "admin-keyset",
        **{"temp": temp, "humidity": humidity}
    )
    result = api.send_and_listen(code, "admin-keyset")
    print(result)


def main():
    while True:
        temp, humidity = read_sensor_data()
        send_sensor_data(temp, humidity)
        time.sleep(sample_freq)


if __name__ == "__main__":
    try:
        print("temperature(°C)  humidity")
        main()
    except KeyboardInterrupt:
        print("\n", "Stopping script...")
        sys.exit()

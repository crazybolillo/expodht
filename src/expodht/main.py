from os import environ
from random import uniform
from time import sleep

from prometheus_client import start_http_server, Gauge
from logging import getLogger, basicConfig, NOTSET
from pigpio import pi
from expodht.dht22 import Sensor

basicConfig(level=NOTSET)
_logger = getLogger(__name__)

TEMPERATURE = Gauge("dht22_temperature", "Temperature (Celsius) as read by the sensor")
HUMIDITY = Gauge("dht22_humidity", "Relative humidity as read by the sensor")

GPIO = environ.get("GPIO_PIN", 4)
INTERVAL = environ.get("INTERVAL_SECONDS", 10)
HTTP_PORT = environ.get("HTTP_PORT", 9200)
HTTP_ADDR = environ.get("HTTP_ADDR", "0.0.0.0")
DUMMY_MODE = environ.get("DUMMY_MODE")


def dummy_read_metrics():
    return round(uniform(15, 30), 2), round(uniform(15, 30), 2)


def dht_read_metrics(sensor):
    def _read():
        _, _, _, temp, hum = sensor.read()
        return temp, hum

    return _read


def main():
    read_metrics = dummy_read_metrics
    if not DUMMY_MODE:
        gpiod = pi()
        if not gpiod.connected:
            _logger.error("Connection to pigpiod failed. Exiting now")
            raise SystemExit(1)

        sensor = Sensor(gpiod, GPIO)
        read_metrics = dht_read_metrics(sensor)

    start_http_server(HTTP_PORT, HTTP_ADDR)
    _logger.info("Listening on %s:%d", HTTP_ADDR, HTTP_PORT)
    if DUMMY_MODE:
        _logger.info(
            "Running in dummy mode. Metrics will be updated every %s seconds", INTERVAL
        )
    else:
        _logger.info("Will read on GPIO %d every %d seconds", GPIO, INTERVAL)
    while True:
        temp, hum = read_metrics()
        TEMPERATURE.set(temp)
        HUMIDITY.set(hum)
        sleep(INTERVAL)


if __name__ == "__main__":
    main()

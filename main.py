#!/usr/bin/env python3

import requests
import RPi.GPIO as GPIO
from dotenv import load_dotenv
import os
import LCD1602
import time
import board
from adafruit_bme280 import basic as adafruit_bme280

i2c = board.I2C()
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x77)

LOCAL_TEMP = bme280.temperature * (9/5) + 32
LOCAL_HUMIDITY = bme280.humidity
LOCAL_HPA = bme280.pressure

def setup_LCD():
	LCD1602.init(0x27, 1)	# init(slave address, background light)
	LCD1602.write(0, 0, 'Outdoor   Local')
	LCD1602.write(0, 1, f"{int(current_temps['remote_temp'])}*F     {int(LOCAL_HUMIDITY)}%{int(LOCAL_TEMP)}*F")
	time.sleep(2)

def destroy_LCD():
	LCD1602.clear()

load_dotenv()
SERVER_IP = os.environ.get("SERVER_IP")
GARAGE_IP = os.environ.get("GARAGE_IP")
#VENSTAR_IP = os.environ.get("VENSTAR_IP")
#VENSTAR_SENSOR_URL = 'http://' + VENSTAR_IP + '/query/sensors'
temp_response = requests.get(f'http://{SERVER_IP}/api/current_temps')
current_temps = temp_response.json()
# garage_response = requests.get(f'http://{GARAGE_IP}/get-status')
# garage_temps = garage_response.json()
#sensor_response = requests.get(VENSTAR_SENSOR_URL)
#sensors = sensor_response.json()
#remote_temp = 'N/A' # set to N/A in case its not found!
#for sensor in sensors['sensors']:
#    if sensor['name'] == 'Remote':
# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
# LIVING_RM_PIN = 17
# LOCAL_PIN = 27
# GPIO.setup(LIVING_RM_PIN, GPIO.OUT)
# GPIO.setup(LOCAL_PIN, GPIO.OUT)


# remote_temp = 65
# current_temps = {}
# garage_temps = {}
# current_temps['living_room_temp'] = 65
# current_temps['thermostat_temp'] = 65
# garage_temps['temperature'] = 65
# if current_temps['living_room_temp'] <= garage_temps['temperature']:
#     if not GPIO.input(LIVING_RM_PIN):
#         GPIO.output(LIVING_RM_PIN, GPIO.HIGH)
# else:
#     if GPIO.input(LIVING_RM_PIN):
#         GPIO.output(LIVING_RM_PIN, GPIO.LOW)

# if current_temps['thermostat_temp'] <= garage_temps['temperature']:
#     if not GPIO.input(LOCAL_PIN):
#         GPIO.output(LOCAL_PIN, GPIO.HIGH)
# else:
#     if GPIO.input(LOCAL_PIN):
#         GPIO.output(LOCAL_PIN, GPIO.LOW)

try:
    setup_LCD()
except KeyboardInterrupt:
    destroy_LCD()

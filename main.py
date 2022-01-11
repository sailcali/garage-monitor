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
local_farenheight = bme280.temperature * (9/5) + 32
def setup():
	LCD1602.init(0x27, 1)	# init(slave address, background light)
	LCD1602.write(0, 0, 'Local     Garage')
	LCD1602.write(1, 0, f"{int(garage_temps['temperature'])}*F        {int(local_farenheight)}*F")
	time.sleep(2)

def destroy():
	LCD1602.clear()


load_dotenv()
SERVER_IP = os.environ.get("SERVER_IP")
GARAGE_IP = os.environ.get("GARAGE_IP")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
LIVING_RM_PIN = 17
LOCAL_PIN = 27
GPIO.setup(LIVING_RM_PIN, GPIO.OUT)
GPIO.setup(LOCAL_PIN, GPIO.OUT)

temp_response = requests.get(f'http://{SERVER_IP}/api/current_temps')
current_temps = temp_response.json()
garage_response = requests.get(f'http://{GARAGE_IP}/get-status')
garage_temps = garage_response.json()

if current_temps['living_room_temp'] <= garage_temps['temperature']:
    if not GPIO.input(LIVING_RM_PIN):
        GPIO.output(LIVING_RM_PIN, GPIO.HIGH)
else:
    if GPIO.input(LIVING_RM_PIN):
        GPIO.output(LIVING_RM_PIN, GPIO.LOW)

if current_temps['thermostat_temp'] <= garage_temps['temperature']:
    if not GPIO.input(LOCAL_PIN):
        GPIO.output(LOCAL_PIN, GPIO.HIGH)
else:
    if GPIO.input(LOCAL_PIN):
        GPIO.output(LOCAL_PIN, GPIO.LOW)

try:
    setup()
except KeyboardInterrupt:
    destroy()
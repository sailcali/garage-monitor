#!/usr/bin/env python3

import requests
import RPi.GPIO as GPIO
from dotenv import load_dotenv
import os

load_dotenv()
SERVER_IP = os.environ.get("SERVER_IP")
GARAGE_IP = os.environ.get("GARAGE_IP")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO_PIN = 17
GPIO.setup(GPIO_PIN, GPIO.OUT)

temp_response = requests.get(f'http://{SERVER_IP}/temps/current_temps')
current_temps = temp_response.json()
garage_response = requests.get(f'http://{GARAGE_IP}/get-status')
garage_temps = garage_response.json()

if current_temps['thermostat_temp'] <= garage_temps['temperature']:
    if not GPIO.input(GPIO_PIN):
        GPIO.output(GPIO_PIN, GPIO.HIGH)
else:
    if GPIO.input(GPIO_PIN):
        GPIO.output(GPIO_PIN, GPIO.LOW)
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

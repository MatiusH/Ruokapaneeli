__author__ = 'Matius Hurskainen'

import main
import RPi.GPIO as GPIO
import queue_number
import lcd_i2c
import order
import order_mode
from time import sleep



def enter_serving_mode():
    # TODO
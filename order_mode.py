__author__ = 'Matius Hurskainen'


import main
import RPi.GPIO as GPIO
import queue_number
import lcd_i2c
import order
import serving_mode
from time import sleep


def next_order():
    # TODO


def previous_order():
    # TODO


def food_count(food_number, direction):
    # TODO



def enter_order_mode():
    try:
        GPIO.add_event_detect(main.NUMBER_UP, GPIO.FALLING)
        GPIO.add_event_detect(main.NUMBER_DOWN, GPIO.FALLING)
        GPIO.add_event_detect(main.FOOD_0_UP, GPIO.FALLING)
        GPIO.add_event_detect(main.FOOD_0_DOWN, GPIO.FALLING)
        GPIO.add_event_detect(main.FOOD_1_UP, GPIO.FALLING)
        GPIO.add_event_detect(main.FOOD_1_DOWN, GPIO.FALLING)
        GPIO.add_event_detect(main.FOOD_2_UP, GPIO.FALLING)
        GPIO.add_event_detect(main.FOOD_2_DOWN, GPIO.FALLING)
        GPIO.add_event_detect(main.FOOD_3_UP, GPIO.FALLING)
        GPIO.add_event_detect(main.FOOD_3_DOWN, GPIO.FALLING)

        while not GPIO.event_detected(main.MAIN_SWITCH):
            if GPIO.event_detected(main.NUMBER_UP):
                next_order()
            elif GPIO.event_detected(main.NUMBER_DOWN):
                previous_order()
            elif GPIO.event_detected(main.FOOD_0_UP):
                food_count(0, 1)
            elif GPIO.event_detected(main.FOOD_0_DOWN):
                food_count(0, 0)
            elif GPIO.event_detected(main.FOOD_1_UP):
                food_count(1, 1)
            elif GPIO.event_detected(main.FOOD_1_DOWN):
                food_count(1, 0)
            elif GPIO.event_detected(main.FOOD_2_UP):
                food_count(2, 1)
            elif GPIO.event_detected(main.FOOD_2_DOWN):
                food_count(2, 0)
            elif GPIO.event_detected(main.FOOD_3_UP):
                food_count(3, 1)
            elif GPIO.event_detected(main.FOOD_3_DOWN):
                food_count(3, 0)
            sleep(0.5)

        serving_mode.enter_serving_mode()

    except KeyboardInterrupt:
        GPIO.cleanup()
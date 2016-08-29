__author__ = 'Matius Hurskainen'

import RPi.GPIO as GPIO
import lcd_i2c
import order
import order_mode
from time import sleep




# def food_count(food_number, direction):
#     # Increase food count
#     if direction == 1:
#         variables.TO_BE_COOKED[food_number] += 1
#     # Decrease food count
#     elif direction == 0:
#         if variables.TO_BE_COOKED[food_number] > 0:
#             variables.TO_BE_COOKED[food_number] -= 1
#     update_LCD(food_number, str(variables.TO_BE_COOKED[food_number]))
#     cycle_queue_number(100)
#
#
#
#
# def enter_serving_mode():
#     GPIO.add_event_detect(MAIN_SWITCH, GPIO.RISING)
#     GPIO.remove_event_detect(NUMBER_UP)
#     GPIO.remove_event_detect(NUMBER_DOWN)
#
#     try:
#         while not GPIO.event_detected(MAIN_SWITCH):
#             if GPIO.event_detected(FOOD_0_UP):
#                 GPIO.remove_event_detect(FOOD_0_UP)
#                 food_count(0, 1)
#                 GPIO.add_event_detect(FOOD_0_UP, GPIO.FALLING)
#
#             elif GPIO.event_detected(FOOD_0_DOWN):
#                 GPIO.remove_event_detect(FOOD_0_DOWN)
#                 food_count(0, 0)
#                 GPIO.add_event_detect(FOOD_0_DOWN, GPIO.FALLING)
#
#             elif GPIO.event_detected(FOOD_1_UP):
#                 GPIO.remove_event_detect(FOOD_1_UP)
#                 food_count(1, 1)
#                 GPIO.add_event_detect(FOOD_1_UP, GPIO.FALLING)
#
#             elif GPIO.event_detected(FOOD_1_DOWN):
#                 GPIO.remove_event_detect(FOOD_1_DOWN)
#                 food_count(1, 0)
#                 GPIO.add_event_detect(FOOD_1_DOWN, GPIO.FALLING)
#
#             elif GPIO.event_detected(FOOD_2_UP):
#                 GPIO.remove_event_detect(FOOD_2_UP)
#                 food_count(2, 1)
#                 GPIO.add_event_detect(FOOD_2_UP, GPIO.FALLING)
#
#             elif GPIO.event_detected(FOOD_2_DOWN):
#                 GPIO.remove_event_detect(FOOD_2_DOWN)
#                 food_count(2, 0)
#                 GPIO.add_event_detect(FOOD_2_DOWN, GPIO.FALLING)
#
#             elif GPIO.event_detected(FOOD_3_UP):
#                 GPIO.remove_event_detect(FOOD_3_UP)
#                 food_count(3, 1)
#                 GPIO.add_event_detect(FOOD_3_UP, GPIO.FALLING)
#
#             elif GPIO.event_detected(FOOD_3_DOWN):
#                 GPIO.remove_event_detect(FOOD_3_DOWN)
#                 food_count(3, 0)
#                 GPIO.add_event_detect(FOOD_3_DOWN, GPIO.FALLING)
#
#             cycle_queue_number(1)
#
#         GPIO.remove_event_detect(MAIN_SWITCH)
#         order_mode.enter_order_mode()
#
#     except KeyboardInterrupt:
#         return
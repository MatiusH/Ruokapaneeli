__author__ = 'Matius Hurskainen'


import RPi.GPIO as GPIO
import variables
import time


# # DIGIT_1 =  PIN 12
# # DIGIT_2 =  PIN 9
# # DIGIT_3 =  PIN 8
# # DIGIT_4 =  PIN 6
#
# # SEGMENT_A =  PIN 11
# # SEGMENT_B =  Pin 7
# # SEGMENT_C =  Pin 4
# # SEGMENT_D =  Pin 2
# # SEGMENT_E =  Pin 1
# # SEGMENT_F =  Pin 10
# # SEGMENT_G =  Pin 5
# # SEGMENT_DP = Pin 3
#
# DIGITS = [9, 27, 17, 11]
#
# SEGMENTS = [10, 4, 6, 13, 19, 22, 5]
#
# NUMBERS = {' ': (0, 0, 0, 0, 0, 0, 0),
#            '0': (1, 1, 1, 1, 1, 1, 0),
#            '1': (0, 1, 1, 0, 0, 0, 0),
#            '2': (1, 1, 0, 1, 1, 0, 1),
#            '3': (1, 1, 1, 1, 0, 0, 1),
#            '4': (0, 1, 1, 0, 0, 1, 1),
#            '5': (1, 0, 1, 1, 0, 1, 1),
#            '6': (1, 0, 1, 1, 1, 1, 1),
#            '7': (1, 1, 1, 0, 0, 0, 0),
#            '8': (1, 1, 1, 1, 1, 1, 1),
#            '9': (1, 1, 1, 1, 0, 1, 1)}
#
#
# def setup_7_seg_pins():
#     for digit in DIGITS:
#         GPIO.setup(digit, GPIO.OUT)
#         GPIO.output(digit, 1)
#
#     for segment in SEGMENTS:
#         GPIO.setup(segment, GPIO.OUT)
#
#
#
# def update_queue_number():
#     variables.FOUR_DIGIT_QUEUE_NUMBER = (4 - len(str(variables.QUEUE_NUMBER))) * ' ' + \
#                                                     str(variables.QUEUE_NUMBER)


def cycle_queue_number():
    try:
        # for i in range(10):
            for digit_num in range(4):
                for segment_num in range(7):
                    GPIO.output(SEGMENTS[segment_num], NUMBERS[variables.FOUR_DIGIT_QUEUE_NUMBER[digit_num]][segment_num])
                GPIO.output(DIGITS[digit_num], 0)
                time.sleep(0.001)
                GPIO.output(DIGITS[digit_num], 1)


    except KeyboardInterrupt:
        return
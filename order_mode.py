__author__ = 'Matius Hurskainen'

import RPi.GPIO as GPIO
import queue_number
import lcd_i2c
import order
import serving_mode
from time import sleep
import variables


MAIN_SWITCH = 18
FOOD_0_UP   = 23
FOOD_0_DOWN = 24
FOOD_1_UP   = 25
FOOD_1_DOWN = 8
FOOD_2_UP   = 7
FOOD_2_DOWN = 12
FOOD_3_UP   = 16
FOOD_3_DOWN = 20
NUMBER_UP   = 21
NUMBER_DOWN = 26

# DIGIT_1 =  PIN 12
# DIGIT_2 =  PIN 9
# DIGIT_3 =  PIN 8
# DIGIT_4 =  PIN 6

# SEGMENT_A =  PIN 11
# SEGMENT_B =  Pin 7
# SEGMENT_C =  Pin 4
# SEGMENT_D =  Pin 2
# SEGMENT_E =  Pin 1
# SEGMENT_F =  Pin 10
# SEGMENT_G =  Pin 5
# SEGMENT_DP = Pin 3

DIGITS = [9, 27, 17, 11]

SEGMENTS = [10, 4, 6, 13, 19, 22, 5]

NUMBERS = {' ': (0, 0, 0, 0, 0, 0, 0),
           '0': (1, 1, 1, 1, 1, 1, 0),
           '1': (0, 1, 1, 0, 0, 0, 0),
           '2': (1, 1, 0, 1, 1, 0, 1),
           '3': (1, 1, 1, 1, 0, 0, 1),
           '4': (0, 1, 1, 0, 0, 1, 1),
           '5': (1, 0, 1, 1, 0, 1, 1),
           '6': (1, 0, 1, 1, 1, 1, 1),
           '7': (1, 1, 1, 0, 0, 0, 0),
           '8': (1, 1, 1, 1, 1, 1, 1),
           '9': (1, 1, 1, 1, 0, 1, 1)}

LCD_DEFAULT_LINES = ["Ranut   0       ",
                     "MaPe    0       ",
                     "Sipuli  0       ",
                     "Lihis   0  = 0 e"]


def setup_7_seg_pins():
    for digit in DIGITS:
        GPIO.setup(digit, GPIO.OUT)
        GPIO.output(digit, 1)

    for segment in SEGMENTS:
        GPIO.setup(segment, GPIO.OUT)



def format_LCD():
    for i in range(4):
        lcd_i2c.lcd_string(LCD_DEFAULT_LINES[i], lcd_i2c.LCD_ADDRESSES[i])



def update_queue_number():
    variables.FOUR_DIGIT_QUEUE_NUMBER = (4 - len(str(variables.QUEUE_NUMBER))) * ' ' + \
                                                    str(variables.QUEUE_NUMBER)


def setup_buttons():
        GPIO.setup(MAIN_SWITCH, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(NUMBER_UP,   GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(NUMBER_DOWN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(FOOD_0_UP,   GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(FOOD_0_DOWN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(FOOD_1_UP,   GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(FOOD_1_DOWN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(FOOD_2_UP,   GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(FOOD_2_DOWN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(FOOD_3_UP,   GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(FOOD_3_DOWN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)


def write_order_to_logfile():
    logfile = open('logfile.txt', 'r+')
    # If the order exists and needs to be modified
    queue_number_str = ((4 - len(str(variables.QUEUE_NUMBER))) * '0' + str(variables.QUEUE_NUMBER))
    for rivi in logfile:
        if rivi[0:4] == queue_number_str:
            rivi = (rivi[0:5] + str(variables.TO_BE_COOKED[0]) + ' ' + \
                         str(variables.TO_BE_COOKED[1]) + ' ' + \
                         str(variables.TO_BE_COOKED[2]) + ' ' + \
                         str(variables.TO_BE_COOKED[3]) + '\n')
            logfile.close()
            return
        else:
            continue
    # If the order is new
    logfile.write('\n' + (4 - len(str(variables.QUEUE_NUMBER))) * '0' + \
                           str(variables.QUEUE_NUMBER)   + ' ' + \
                           str(variables.TO_BE_COOKED[0]) + ' ' + \
                           str(variables.TO_BE_COOKED[1]) + ' ' + \
                           str(variables.TO_BE_COOKED[2]) + ' ' + \
                           str(variables.TO_BE_COOKED[3]))
    logfile.close()


def read_order_from_logfile():
    logfile = open('logfile.txt', 'r')
    queue_number_str = ((4 - len(str(variables.QUEUE_NUMBER))) * '0' + str(variables.QUEUE_NUMBER))
    for rivi in logfile:
        if rivi[0:4] == queue_number_str:
            variables.TO_BE_COOKED[0] = rivi[5]
            variables.TO_BE_COOKED[1] = rivi[7]
            variables.TO_BE_COOKED[2] = rivi[9]
            variables.TO_BE_COOKED[3] = rivi[11]
        else:
            continue
    logfile.close()


def next_order():
    write_order_to_logfile()
    variables.TO_BE_COOKED = [0, 0, 0, 0]
    format_LCD()
    variables.QUEUE_NUMBER += 1
    update_queue_number()
    cycle_queue_number(100)
    GPIO.add_event_detect(NUMBER_UP,   GPIO.FALLING)
    return


def previous_order():
    if variables.QUEUE_NUMBER > 0:
        variables.QUEUE_NUMBER -= 1
    update_queue_number()

    # Update food orders on LCD
    read_order_from_logfile()
    for i in range(4):
        update_LCD(i, str(variables.TO_BE_COOKED[i]))

    cycle_queue_number(100)
    GPIO.add_event_detect(NUMBER_DOWN,   GPIO.FALLING)
    return


def food_count(food_number, direction):
    # Increase food count
    if direction == 1:
        variables.TO_BE_COOKED[food_number] += 1
    # Decrease food count
    elif direction == 0:
        if variables.TO_BE_COOKED[food_number] > 0:
            variables.TO_BE_COOKED[food_number] -= 1
    update_LCD(food_number, str(variables.TO_BE_COOKED[food_number]))
    cycle_queue_number(100)



def update_LCD(line, number):
    lcd_i2c.lcd_string((LCD_DEFAULT_LINES[line][0:8] + number + LCD_DEFAULT_LINES[line][9:16]), lcd_i2c.LCD_ADDRESSES[line])



def cycle_queue_number(count):
    for i in range(count):
        for digit_num in range(4):
            for segment_num in range(7):
                GPIO.output(SEGMENTS[segment_num], NUMBERS[variables.FOUR_DIGIT_QUEUE_NUMBER[digit_num]][segment_num])
            GPIO.output(DIGITS[digit_num], 0)
            sleep(0.001)
            GPIO.output(DIGITS[digit_num], 1)


def enter_order_mode():
    GPIO.add_event_detect(MAIN_SWITCH, GPIO.FALLING)
    GPIO.add_event_detect(NUMBER_UP,   GPIO.FALLING)
    GPIO.add_event_detect(NUMBER_DOWN, GPIO.FALLING)
    GPIO.add_event_detect(FOOD_0_UP,   GPIO.FALLING)
    GPIO.add_event_detect(FOOD_0_DOWN, GPIO.FALLING)
    GPIO.add_event_detect(FOOD_1_UP,   GPIO.FALLING)
    GPIO.add_event_detect(FOOD_1_DOWN, GPIO.FALLING)
    GPIO.add_event_detect(FOOD_2_UP,   GPIO.FALLING)
    GPIO.add_event_detect(FOOD_2_DOWN, GPIO.FALLING)
    GPIO.add_event_detect(FOOD_3_UP,   GPIO.FALLING)
    GPIO.add_event_detect(FOOD_3_DOWN, GPIO.FALLING)

    try:
        while not GPIO.event_detected(MAIN_SWITCH):
            if GPIO.event_detected(NUMBER_UP):
                GPIO.remove_event_detect(NUMBER_UP)
                next_order()

            elif GPIO.event_detected(NUMBER_DOWN):
                GPIO.remove_event_detect(NUMBER_DOWN)
                previous_order()

            elif GPIO.event_detected(FOOD_0_UP):
                GPIO.remove_event_detect(FOOD_0_UP)
                food_count(0, 1)
                GPIO.add_event_detect(FOOD_0_UP, GPIO.FALLING)

            elif GPIO.event_detected(FOOD_0_DOWN):
                GPIO.remove_event_detect(FOOD_0_DOWN)
                food_count(0, 0)
                GPIO.add_event_detect(FOOD_0_DOWN, GPIO.FALLING)

            elif GPIO.event_detected(FOOD_1_UP):
                GPIO.remove_event_detect(FOOD_1_UP)
                food_count(1, 1)
                GPIO.add_event_detect(FOOD_1_UP, GPIO.FALLING)

            elif GPIO.event_detected(FOOD_1_DOWN):
                GPIO.remove_event_detect(FOOD_1_DOWN)
                food_count(1, 0)
                GPIO.add_event_detect(FOOD_1_DOWN, GPIO.FALLING)

            elif GPIO.event_detected(FOOD_2_UP):
                GPIO.remove_event_detect(FOOD_2_UP)
                food_count(2, 1)
                GPIO.add_event_detect(FOOD_2_UP, GPIO.FALLING)

            elif GPIO.event_detected(FOOD_2_DOWN):
                GPIO.remove_event_detect(FOOD_2_DOWN)
                food_count(2, 0)
                GPIO.add_event_detect(FOOD_2_DOWN, GPIO.FALLING)

            elif GPIO.event_detected(FOOD_3_UP):
                GPIO.remove_event_detect(FOOD_3_UP)
                food_count(3, 1)
                GPIO.add_event_detect(FOOD_3_UP, GPIO.FALLING)

            elif GPIO.event_detected(FOOD_3_DOWN):
                GPIO.remove_event_detect(FOOD_3_DOWN)
                food_count(3, 0)
                GPIO.add_event_detect(FOOD_3_DOWN, GPIO.FALLING)

            cycle_queue_number(1)

        serving_mode.enter_serving_mode()

    except KeyboardInterrupt:
        return
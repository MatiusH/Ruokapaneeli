__author__ = 'Matius Hurskainen'


import RPi.GPIO as GPIO
import main




# DIGIT_1 = 24    # PIN 12
# DIGIT_2 = 25    # PIN 9
# DIGIT_3 = 7    # PIN 8
# DIGIT_4 = 18     # PIN 6

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

# SEGMENT_A = 18  # PIN 11
# SEGMENT_B = 8   # Pin 7
# SEGMENT_C = 16  # Pin 4
# SEGMENT_D = 21  # Pin 2
# SEGMENT_E = 26  # Pin 1
# SEGMENT_F = 23  # Pin 10
# SEGMENT_G = 12  # Pin 5
# SEGMENT_DP = 20 # Pin 3


def init_7_seg_pins():
    for digit in DIGITS:
        GPIO.setup(digit, GPIO.IN)

    for segment in SEGMENTS:
        GPIO.setup(segment, GPIO.OUT)




def change_digit(digit, number):
    # Clear existing number
    GPIO.output(digit, 0)
    for segment in SEGMENTS:
        GPIO.output(segment, 0)

    # Setup new number
    for i in range(0, 7):
        GPIO.output(SEGMENTS[i], NUMBERS[number][i])

    GPIO.output(DIGITS[digit])




def change_queue_number():
    queue_number_str = str(main.QUEUE_NUMBER)

    # Change only the digits needed, empty others
    if len(queue_number_str) == 4:
        for i in range(0, 3):
            change_digit(DIGITS[i], queue_number_str[i])

    elif len(queue_number_str) == 3:
        change_digit(DIGITS[0], ' ')
        for i in range(1, 3):
            change_digit(DIGITS[i], queue_number_str[i - 1])

    elif len(queue_number_str) == 2:
        change_digit(DIGITS[0], ' ')
        change_digit(DIGITS[1], ' ')
        change_digit(DIGITS[2], queue_number_str[0])
        change_digit(DIGITS[3], queue_number_str[1])

    elif len(queue_number_str) == 1:
        for i in range(0, 2):
            change_digit(DIGITS[i], ' ')
        change_digit(DIGITS[3], queue_number_str[0])

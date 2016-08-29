__author__ = 'Matius Hurskainen'

import RPi.GPIO as GPIO
import lcd_i2c
import order
import serving_mode
from time import sleep


MAIN_SWITCH = 26
NUMBER_UP   = 21
NUMBER_DOWN = 20
FOOD_0_UP   = 16
FOOD_0_DOWN = 12
FOOD_1_UP   = 7
FOOD_1_DOWN = 8
FOOD_2_UP   = 25
FOOD_2_DOWN = 24
FOOD_3_UP   = 23
FOOD_3_DOWN = 18

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

# TODO: LUOKKA TÄHÄN HETI
#
# class Vuoronumero:
#     def __init__(self):
#         self.__vuoronumero = 0
#
#     @property
#     def get_vuoronumero(self):
#         return self.__vuoronumero
#
#     def next_vuoronumero(self):
#         self.__vuoronumero += 1
#
#     def previous_vuoronumero(self):
#         self.__vuoronumero -= 1







class Register:
    def __init__(self):
        # Variables
        self.__ALL_ORDERS = []
        self.__QUEUE_NUMBER = 0
        self.__FOUR_DIGIT_QUEUE_NUMBER = '    '


    def setup(self):
        # Setup 7-seg pins
        for digit in DIGITS:
            GPIO.setup(digit, GPIO.OUT)
            GPIO.output(digit, 1)
        for segment in SEGMENTS:
            GPIO.setup(segment, GPIO.OUT)

        # Setup buttons
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

        # Init LCD
        lcd_i2c.lcd_init()
        self.format_LCD()

        # Create Order-objects from logfile
        logfile = open('logfile.txt', 'r')
        for line in logfile:
            number = line[0:4]
            orders = []
            orders.append(5)
            orders.append(7)
            orders.append(9)
            orders.append(11)
            servings = []
            servings.append(13)
            servings.append(15)
            servings.append(17)
            servings.append(19)
            self.__ALL_ORDERS.append(order.Order(number, orders, servings, True))
        logfile.close()

        # Update QUEUE_NUMBER to latest existing one
        if len(self.__ALL_ORDERS) > 0:
            self.__QUEUE_NUMBER = self.__ALL_ORDERS[len(self.__ALL_ORDERS) - 2].return_queue_number



    def format_LCD(self):
        for i in range(4):
            lcd_i2c.lcd_string(LCD_DEFAULT_LINES[i], lcd_i2c.LCD_ADDRESSES[i])



    def update_four_digit_queue_number(self):
        self.__FOUR_DIGIT_QUEUE_NUMBER = (4 - len(str(self.__QUEUE_NUMBER))) * ' ' + str(self.__QUEUE_NUMBER)


    def update_LCD(self, line, number):
        lcd_i2c.lcd_string((LCD_DEFAULT_LINES[line][0:8] + number + LCD_DEFAULT_LINES[line][9:16]), lcd_i2c.LCD_ADDRESSES[line])


    def next_order(self):
        # New order
        if len(self.__ALL_ORDERS) == (self.__QUEUE_NUMBER + 1):
            self.__ALL_ORDERS.append(order.Order(self.__QUEUE_NUMBER + 1))
            self.__QUEUE_NUMBER += 1
            self.update_four_digit_queue_number()
            self.format_LCD()
        # Existing order
        else:
            self.__QUEUE_NUMBER += 1
            self.update_four_digit_queue_number()
        self.cycle_queue_number(100)
        GPIO.add_event_detect(NUMBER_UP,   GPIO.FALLING)


    def previous_order(self):
        if self.__QUEUE_NUMBER > 0:
            self.__QUEUE_NUMBER -= 1
            self.update_four_digit_queue_number()
            # Update LCD
            for i in range(0, 4):
                self.update_LCD(i, self.__ALL_ORDERS[self.__QUEUE_NUMBER - 1].return_ordered_foods[i])

            # Update food orders on LCD
            #             read_order_from_logfile()
            #             for i in range(4):
            #                 update_LCD(i, str(variables.TO_BE_COOKED[i]))

        self.cycle_queue_number(100)
        GPIO.add_event_detect(NUMBER_DOWN,   GPIO.FALLING)



    def cycle_queue_number(self, count):
        if len(self.__ALL_ORDERS) > 0:
            for i in range(count):
                for digit_num in range(4):
                    for segment_num in range(7):
                        # nro = ALL_ORDERS[(vuoronumero - 1)].return_four_digit_queue_number
                        # ALL_ORDERS[(vuoronumero - 1)].typera_testi_metodi
                        GPIO.output(SEGMENTS[segment_num], NUMBERS[self.__FOUR_DIGIT_QUEUE_NUMBER[digit_num]][segment_num])
                        # GPIO.output(SEGMENTS[segment_num], (NUMBERS[nro[digit_num]][segment_num]))
                        # GPIO.output(SEGMENTS[segment_num], NUMBERS['   1'[digit_num]][segment_num])
                    GPIO.output(DIGITS[digit_num], 0)
                    sleep(0.001)
                    GPIO.output(DIGITS[digit_num], 1)


    def order_mode(self):
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

        # Disable 7-segment display
        for digit in DIGITS:
            GPIO.output(digit, 1)

        try:
            # Loop until main switch is flipped
            while not GPIO.event_detected(MAIN_SWITCH):
                if GPIO.event_detected(FOOD_0_UP):
                    GPIO.remove_event_detect(FOOD_0_UP)
                    self.__ALL_ORDERS[self.__QUEUE_NUMBER - 1].add_ordered_food(0)
                    GPIO.add_event_detect(FOOD_0_UP, GPIO.FALLING)

                elif GPIO.event_detected(FOOD_0_DOWN):
                    GPIO.remove_event_detect(FOOD_0_DOWN)
                    self.__ALL_ORDERS[self.__QUEUE_NUMBER - 1].remove_ordered_food(0)
                    GPIO.add_event_detect(FOOD_0_DOWN, GPIO.FALLING)

                elif GPIO.event_detected(FOOD_1_UP):
                    GPIO.remove_event_detect(FOOD_1_UP)
                    self.__ALL_ORDERS[self.__QUEUE_NUMBER - 1].add_ordered_food(1)
                    GPIO.add_event_detect(FOOD_1_UP, GPIO.FALLING)

                elif GPIO.event_detected(FOOD_1_DOWN):
                    GPIO.remove_event_detect(FOOD_1_DOWN)
                    self.__ALL_ORDERS[self.__QUEUE_NUMBER - 1].add_ordered_food(1)
                    GPIO.add_event_detect(FOOD_1_DOWN, GPIO.FALLING)

                elif GPIO.event_detected(FOOD_2_UP):
                    GPIO.remove_event_detect(FOOD_2_UP)
                    self.__ALL_ORDERS[self.__QUEUE_NUMBER - 1].add_ordered_food(2)
                    GPIO.add_event_detect(FOOD_2_UP, GPIO.FALLING)

                elif GPIO.event_detected(FOOD_2_DOWN):
                    GPIO.remove_event_detect(FOOD_2_DOWN)
                    self.__ALL_ORDERS[self.__QUEUE_NUMBER - 1].remove_ordered_food(2)
                    GPIO.add_event_detect(FOOD_2_DOWN, GPIO.FALLING)

                elif GPIO.event_detected(FOOD_3_UP):
                    GPIO.remove_event_detect(FOOD_3_UP)
                    self.__ALL_ORDERS[self.__QUEUE_NUMBER - 1].add_ordered_food(3)
                    GPIO.add_event_detect(FOOD_3_UP, GPIO.FALLING)

                elif GPIO.event_detected(FOOD_3_DOWN):
                    GPIO.remove_event_detect(FOOD_3_DOWN)
                    self.__ALL_ORDERS[self.__QUEUE_NUMBER - 1].remove_ordered_food(3)
                    GPIO.add_event_detect(FOOD_3_DOWN, GPIO.FALLING)

                elif GPIO.event_detected(NUMBER_UP):
                    GPIO.remove_event_detect(NUMBER_UP)
                    self.next_order()

                elif GPIO.event_detected(NUMBER_DOWN):
                    GPIO.remove_event_detect(NUMBER_DOWN)
                    self.previous_order()

                self.cycle_queue_number(1)

            GPIO.remove_event_detect(MAIN_SWITCH)
            serving_mode.enter_serving_mode()

        except KeyboardInterrupt:
            return

# def write_order_to_logfile():               ## Tämä order-metodiksi
#     logfile = open('logfile.txt', 'r+')
#     # If the order exists and needs to be modified
#     # queue_number_str = ((4 - len(str(variables.QUEUE_NUMBER))) * '0' + str(variables.QUEUE_NUMBER))
#     queue_number_str = ((4 - len(str(variables.QUEUE_NUMBER))) * '0' + str(variables.QUEUE_NUMBER)) ########################################
#     for rivi in logfile:
#         if rivi[0:4] == queue_number_str:
#             rivi = (rivi[0:5] + str(variables.TO_BE_COOKED[0]) + ' ' + \
#                          str(variables.TO_BE_COOKED[1]) + ' ' + \
#                          str(variables.TO_BE_COOKED[2]) + ' ' + \
#                          str(variables.TO_BE_COOKED[3]) + '\n')
#             logfile.close()
#             return
#         else:
#             continue
#     # If the order is new
#     logfile.write('\n' + (4 - len(str(variables.QUEUE_NUMBER))) * '0' + \
#                            str(variables.QUEUE_NUMBER)   + ' ' + \
#                            str(variables.TO_BE_COOKED[0]) + ' ' + \
#                            str(variables.TO_BE_COOKED[1]) + ' ' + \
#                            str(variables.TO_BE_COOKED[2]) + ' ' + \
#                            str(variables.TO_BE_COOKED[3]))
#     logfile.close()


# def read_order_from_logfile():
#     logfile = open('logfile.txt', 'r')
#     queue_number_str = ((4 - len(str(variables.QUEUE_NUMBER))) * '0' + str(variables.QUEUE_NUMBER))
#     for rivi in logfile:
#         if rivi[0:4] == queue_number_str:
#             variables.TO_BE_COOKED[0] = rivi[5]
#             variables.TO_BE_COOKED[1] = rivi[7]
#             variables.TO_BE_COOKED[2] = rivi[9]
#             variables.TO_BE_COOKED[3] = rivi[11]
#         else:
#             continue
#     logfile.close()


# def next_order():
#     if len(ALL_ORDERS) == ( + 1):
#         ALL_ORDERS.append(order.Order(vuoronumero.get_vuoronumero+1))
#     else:




# def previous_order():
#     if QUEUE_NUMBER > 0:
#         QUEUE_NUMBER -= 1
#
#     # Update food orders on LCD
#     # TODO
#     #             read_order_from_logfile()
#     #             for i in range(4):
#     #                 update_LCD(i, str(variables.TO_BE_COOKED[i]))
#
#     cycle_queue_number(100)
#     GPIO.add_event_detect(NUMBER_DOWN,   GPIO.FALLING)
#     return


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







# def cycle_queue_number(count):
#     if len(ALL_ORDERS) > 0:
#         for i in range(count):
#             for digit_num in range(4):
#                 for segment_num in range(7):
#                     nro = ALL_ORDERS[(vuoronumero - 1)].return_four_digit_queue_number
#                     # ALL_ORDERS[(vuoronumero - 1)].typera_testi_metodi
#                     # GPIO.output(SEGMENTS[segment_num], NUMBERS[variables.FOUR_DIGIT_QUEUE_NUMBER[digit_num]][segment_num])
#                     GPIO.output(SEGMENTS[segment_num], (NUMBERS[nro[digit_num]][segment_num]))
#                     # GPIO.output(SEGMENTS[segment_num], NUMBERS['   1'[digit_num]][segment_num])
#                 GPIO.output(DIGITS[digit_num], 0)
#                 sleep(0.001)
#                 GPIO.output(DIGITS[digit_num], 1)


# def next_order():
#     # write_order_to_logfile()
#     # variables.TO_BE_COOKED = [0, 0, 0, 0]
#     # format_LCD()
#     # variables.QUEUE_NUMBER += 1
#     # update_queue_number()
#     # cycle_queue_number(100)
#     # GPIO.add_event_detect(NUMBER_UP,   GPIO.FALLING)
#     # return
#
#     # Jos tilaus on uusi
#     if len(ALL_ORDERS) == (vuoronumero + 1):
#         ALL_ORDERS.append(order.Order(vuoronumero + 1))
#     else:
#         vuoronumero += 1
#     format_LCD()
#     cycle_queue_number(100)
#     GPIO.add_event_detect(NUMBER_UP, GPIO.FALLING)
#     return


# def order_mode():
#     GPIO.add_event_detect(MAIN_SWITCH, GPIO.FALLING)
#     GPIO.add_event_detect(NUMBER_UP,   GPIO.FALLING)
#     GPIO.add_event_detect(NUMBER_DOWN, GPIO.FALLING)
#     GPIO.add_event_detect(FOOD_0_UP,   GPIO.FALLING)
#     GPIO.add_event_detect(FOOD_0_DOWN, GPIO.FALLING)
#     GPIO.add_event_detect(FOOD_1_UP,   GPIO.FALLING)
#     GPIO.add_event_detect(FOOD_1_DOWN, GPIO.FALLING)
#     GPIO.add_event_detect(FOOD_2_UP,   GPIO.FALLING)
#     GPIO.add_event_detect(FOOD_2_DOWN, GPIO.FALLING)
#     GPIO.add_event_detect(FOOD_3_UP,   GPIO.FALLING)
#     GPIO.add_event_detect(FOOD_3_DOWN, GPIO.FALLING)
#
#     # Disable 7-segment display
#     for digit in DIGITS:
#         GPIO.output(digit, 1)
#
#     try:
#         while not GPIO.event_detected(MAIN_SWITCH):
#             if GPIO.event_detected(FOOD_0_UP):
#                 GPIO.remove_event_detect(FOOD_0_UP)
#                 # food_count(0, 1)
#                 ALL_ORDERS[vuoronumero - 1].add_ordered_food(0)
#                 GPIO.add_event_detect(FOOD_0_UP, GPIO.FALLING)
#
#             elif GPIO.event_detected(FOOD_0_DOWN):
#                 GPIO.remove_event_detect(FOOD_0_DOWN)
#                 # food_count(0, 0)
#                 ALL_ORDERS[vuoronumero - 1].remove_ordered_food(0)
#                 GPIO.add_event_detect(FOOD_0_DOWN, GPIO.FALLING)
#
#             elif GPIO.event_detected(FOOD_1_UP):
#                 GPIO.remove_event_detect(FOOD_1_UP)
#                 # food_count(1, 1)
#                 ALL_ORDERS[vuoronumero - 1].add_ordered_food(1)
#                 GPIO.add_event_detect(FOOD_1_UP, GPIO.FALLING)
#
#             elif GPIO.event_detected(FOOD_1_DOWN):
#                 GPIO.remove_event_detect(FOOD_1_DOWN)
#                 # food_count(1, 0)
#                 ALL_ORDERS[vuoronumero - 1].add_ordered_food(1)
#                 GPIO.add_event_detect(FOOD_1_DOWN, GPIO.FALLING)
#
#             elif GPIO.event_detected(FOOD_2_UP):
#                 GPIO.remove_event_detect(FOOD_2_UP)
#                 # food_count(2, 1)
#                 ALL_ORDERS[vuoronumero - 1].add_ordered_food(2)
#                 GPIO.add_event_detect(FOOD_2_UP, GPIO.FALLING)
#
#             elif GPIO.event_detected(FOOD_2_DOWN):
#                 GPIO.remove_event_detect(FOOD_2_DOWN)
#                 # food_count(2, 0)
#                 ALL_ORDERS[vuoronumero - 1].remove_ordered_food(2)
#                 GPIO.add_event_detect(FOOD_2_DOWN, GPIO.FALLING)
#
#             elif GPIO.event_detected(FOOD_3_UP):
#                 GPIO.remove_event_detect(FOOD_3_UP)
#                 # food_count(3, 1)
#                 ALL_ORDERS[vuoronumero - 1].add_ordered_food(3)
#                 GPIO.add_event_detect(FOOD_3_UP, GPIO.FALLING)
#
#             elif GPIO.event_detected(FOOD_3_DOWN):
#                 GPIO.remove_event_detect(FOOD_3_DOWN)
#                 # food_count(3, 0)
#                 ALL_ORDERS[vuoronumero - 1].remove_ordered_food(3)
#                 GPIO.add_event_detect(FOOD_3_DOWN, GPIO.FALLING)
#
#             elif GPIO.event_detected(NUMBER_UP):
#                 GPIO.remove_event_detect(NUMBER_UP)
#                 # next_order()
#
#             elif GPIO.event_detected(NUMBER_DOWN):
#                 GPIO.remove_event_detect(NUMBER_DOWN)
#                 # previous_order()
#
#             cycle_queue_number(1)
#
#         GPIO.remove_event_detect(MAIN_SWITCH)
#         serving_mode.enter_serving_mode()
#
#     except KeyboardInterrupt:
#         return




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
    #         GPIO.remove_event_detect(MAIN_SWITCH)
    #         enter_order_mode()
    #
    #     except KeyboardInterrupt:
    #         return
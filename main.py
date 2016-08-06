__author__ = 'Matius Hurskainen'


# Initial setup
import RPi.GPIO as GPIO
import queue_number
import lcd_i2c
import order
import order_mode
import serving_mode
import variables


# MAIN_SWITCH = 18
# NUMBER_UP   = 23
# NUMBER_DOWN = 24
# FOOD_0_UP   = 25
# FOOD_0_DOWN = 8
# FOOD_1_UP   = 7
# FOOD_1_DOWN = 12
# FOOD_2_UP   = 16
# FOOD_2_DOWN = 20
# FOOD_3_UP   = 21
# FOOD_3_DOWN = 26


# LINE_1 = "Ranut   0       "
# LINE_2 = "MaPe    0       "
# LINE_3 = "Sipuli  0       "
# LINE_4 = "Lihis   0  = 0 e"


#QUEUE_NUMBER = 0
# TO_BE_COOKED_0 = 0
# TO_BE_COOKED_1 = 0
# TO_BE_COOKED_2 = 0
# TO_BE_COOKED_3 = 0




def main():
    try:
        GPIO.setmode(GPIO.BCM)

        # Setup 7-seg display
        # queue_number.setup_7_seg_pins()
        order_mode.setup_7_seg_pins()

        # Setup buttons
        order_mode.setup_buttons()

        # # Setup buttons
        # GPIO.setup(MAIN_SWITCH, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        # GPIO.setup(NUMBER_UP,   GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        # GPIO.setup(NUMBER_DOWN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        # GPIO.setup(FOOD_0_UP,   GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        # GPIO.setup(FOOD_0_DOWN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        # GPIO.setup(FOOD_1_UP,   GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        # GPIO.setup(FOOD_1_DOWN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        # GPIO.setup(FOOD_2_UP,   GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        # GPIO.setup(FOOD_2_DOWN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        # GPIO.setup(FOOD_3_UP,   GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        # GPIO.setup(FOOD_3_DOWN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

        # Init LCD-display
        lcd_i2c.lcd_init()
        order_mode.format_LCD()
        # for i in range(4):
        #     lcd_i2c.lcd_string(order_mode.LCD_DEFAULT_LINES[i], lcd_i2c.LCD_ADDRESSES[i])
        # lcd_i2c.lcd_string(LINE_1, lcd_i2c.LCD_LINE_1)
        # lcd_i2c.lcd_string(LINE_2, lcd_i2c.LCD_LINE_2)
        # lcd_i2c.lcd_string(LINE_3, lcd_i2c.LCD_LINE_3)
        # lcd_i2c.lcd_string(LINE_4, lcd_i2c.LCD_LINE_4)

        # Get queue number from logfile
        logfile = open('logfile.txt', 'r')
        for line in logfile:
            pass
        last_line = line
        logfile.close()
        if last_line == '':
            pass
        else:
            variables.QUEUE_NUMBER = int(last_line[0:4])

        # queue_number.update_queue_number()
        order_mode.update_queue_number()
        # queue_number.cycle_queue_number()

        # while True:
        #     pass

        if GPIO.input(order_mode.MAIN_SWITCH):
            order_mode.enter_order_mode()
        else:
            GPIO.add_event_detect(order_mode.MAIN_SWITCH, GPIO.RISING)
            #serving_mode.enter_serving_mode()
            print('Serving_mode')



    except KeyboardInterrupt:
        GPIO.cleanup()
        return

    # except IOError:
    #     lcd_i2c.lcd_string('IOError', 0)

    GPIO.cleanup()



main()
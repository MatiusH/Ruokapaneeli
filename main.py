__author__ = 'Matius Hurskainen'


# Initial setup
import RPi.GPIO as GPIO
import queue_number
import lcd_i2c


MAIN_SWITCH = 18
NUMBER_UP   = 23
NUMBER_DOWN = 24
FOOD_1_UP   = 25
FOOD_1_DOWN = 8
FOOD_2_UP   = 7
FOOD_2_DOWN = 12
FOOD_3_UP   = 16
FOOD_3_DOWN = 20
FOOD_4_UP   = 21
FOOD_4_DOWN = 26


LINE_1 = "Ranut   0       "
LINE_2 = "MaPe    0       "
LINE_3 = "Sipuli  0       "
LINE_4 = "Lihis   0  = 0 €"


QUEUE_NUMBER = 0





def main():
    try:
        GPIO.setmode(GPIO.BCM)

        # Init 7-seg display
        queue_number.init_7_seg_pins()

        # Setup buttons
        GPIO.setup(MAIN_SWITCH, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(NUMBER_UP,   GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(NUMBER_DOWN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(FOOD_1_UP,   GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(FOOD_1_DOWN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(FOOD_2_UP,   GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(FOOD_2_DOWN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(FOOD_3_UP,   GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(FOOD_3_DOWN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(FOOD_4_UP,   GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(FOOD_4_DOWN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

        # Init LCD-display
        lcd_i2c.lcd_init()
        lcd_i2c.lcd_string(LINE_1, lcd_i2c.LCD_LINE_1)
        lcd_i2c.lcd_string(LINE_2, lcd_i2c.LCD_LINE_2)
        lcd_i2c.lcd_string(LINE_3, lcd_i2c.LCD_LINE_3)
        lcd_i2c.lcd_string(LINE_4, lcd_i2c.LCD_LINE_4)

        # Get queue number from logfile
        logfile = open('logfile.txt', 'rw')
        for line in logfile:
            pass
        last_line = line
        logfile.close()
        QUEUE_NUMBER = int(last_line[0:4])
        queue_number.change_queue_number()




    except KeyboardInterrupt:
        GPIO.cleanup()

    except IOError:
        lcd_i2c.lcd_string('IOError', 0)

    GPIO.cleanup()
__author__ = 'Matius Hurskainen'


import RPi.GPIO as GPIO
import queue_number
import lcd_i2c
import order
import order_mode
import serving_mode
import variables


def main():
    try:
        GPIO.setmode(GPIO.BCM)

        # Setup 7-seg display
        order_mode.setup_7_seg_pins()

        # Setup buttons
        order_mode.setup_buttons()

        # Init LCD-display
        lcd_i2c.lcd_init()
        order_mode.format_LCD()

        # # Get queue number from logfile
        # logfile = open('logfile.txt', 'r')
        # for line in logfile:
        #     pass
        # last_line = line
        # logfile.close()
        # if last_line == '':
        #     pass
        # else:
        #     variables.QUEUE_NUMBER = int(last_line[0:4])

        # Luodaan olio jokaisesta lokitiedoston rivistä
        logfile = open('logfile.txt', 'r')
        for line in logfile:
            number = int(line[0:4])
            orders = []
            orders.append(5)
            orders.append(7)
            orders.append(9)
            orders.append(11)
            servings = []
            orders.append(13)
            orders.append(15)
            orders.append(17)
            orders.append(19)
            order_mode.ALL_ORDERS.append(order.Order(number, orders, servings))

        # order_mode.update_queue_number()          pois?


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
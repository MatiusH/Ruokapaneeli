__author__ = 'Matius Hurskainen'


import RPi.GPIO as GPIO
import order_mode


def main():
    try:
        GPIO.setmode(GPIO.BCM)
        #
        # # Setup 7-seg display
        # order_mode.setup_7_seg_pins()
        #
        # # Setup buttons
        # order_mode.setup_buttons()

        # Init LCD-display
        # lcd_i2c.lcd_init()
        # order_mode.format_LCD()

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
        # logfile = open('logfile.txt', 'r')
        # for line in logfile:
        #     number = line[0:4]
        #     orders = []
        #     orders.append(5)
        #     orders.append(7)
        #     orders.append(9)
        #     orders.append(11)
        #     servings = []
        #     servings.append(13)
        #     servings.append(15)
        #     servings.append(17)
        #     servings.append(19)
        #     order_mode.ALL_ORDERS.append(order.Order(number, orders, servings,True))
        # logfile.close()
        #
        # if len(order_mode.ALL_ORDERS) > 0:
        #     order_mode.vuoronumero = order_mode.ALL_ORDERS[len(order_mode.ALL_ORDERS) - 2].return_queue_number

        # order_mode.update_queue_number()          pois?

        # print(order_mode.ALL_ORDERS[0].return_four_digit_queue_number)

        # if GPIO.input(order_mode.MAIN_SWITCH):
        #     order_mode.enter_order_mode()
        # else:
        #     GPIO.add_event_detect(order_mode.MAIN_SWITCH, GPIO.RISING)
        #     #serving_mode.enter_serving_mode()
        #     print('Serving_mode')

        om = order_mode.Register
        om.setup()


        # Start user interface
        if GPIO.input(order_mode.MAIN_SWITCH):
            om.order_mode()
        else:
            GPIO.add_event_detect(order_mode.MAIN_SWITCH, GPIO.RISING)
            #serving_mode()
            print('Serving_mode')
            return

    except KeyboardInterrupt:
        GPIO.cleanup()
        return

    # except IOError:
    #     lcd_i2c.lcd_string('IOError', 0)

    GPIO.cleanup()



main()
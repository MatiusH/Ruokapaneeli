__author__ = 'Matius Hurskainen'


#import main

class TooManyServedException(Exception):
    pass


class Order:
    total_orders = [0, 0, 0, 0]  # Laskuri, jossa lasketaan kaikki jäljellä olevat tilaukset.

    def __init__(self, queue_number, ordered_foods=None, served_foods=None):
        self.__queue_number = queue_number

        self.__ordered_foods = ordered_foods
        self.__served_foods = served_foods

        if ordered_foods is None:
            self.__ordered_foods = [0, 0, 0, 0]

        if served_foods is None:
            self.__served_foods = [0, 0, 0, 0]

        self.__in_logfile = False

        self.update_logfile()

    def update_logfile(self):
        logfile = open('logfile.txt', 'r+')
        string = ""

        if not self.__in_logfile:
            logfile.write('\n' + self.__queue_number + " ")
            self.__in_logfile = True

        if self.__in_logfile:
            for line in logfile:
                if line[0:4] == self.__queue_number:
                    for i in range(0, 2):
                        if i == 0:
                            lista = self.__ordered_foods
                        if i == 1:
                            lista = self.__served_foods

                        for j in range(0, 4):
                            string += str(lista[j] + " ")

                    line = line[0:5] + string
                    break

        logfile.close()

    def return_queue_number(self):
        return self.__queue_number

    def add_ordered_food(self, food_number):
        self.__ordered_foods[food_number] += 1
        Order.total_orders[food_number] += 1  # Lisätään jäljellä oleviin tilauksiin 1.
        self.update_logfile()

    def remove_ordered_food(self, food_number):
        self.__ordered_foods[food_number] -= 1
        Order.total_orders[food_number] -= 1  # Lisätään jäljellä oleviin tilauksiin 1.
        self.update_logfile()

    def return_ordered_food(self):
        return self.__ordered_foods

    def serve_food(self, food_number):
        try:
            # Jos asiakkaalle yrittää antaa liian monta annosta, nostetaan virhe.
            if self.__served_foods[food_number] == self.__ordered_foods[food_number]:
                raise TooManyServedException()

            else:
                self.__served_foods[food_number] += 1
                Order.total_orders[food_number] -= 1  # Vähennetään jäljellä olevista tilauksista 1.
                self.update_logfile()

        except TooManyServedException:
            # Placeholder-tulostus, pitänee nostaa virhe ylemmäs ohjelmassa.
            print("Tried to serve too many dishes to customer.")

    def return_served_food(self):
        return self.__served_foods

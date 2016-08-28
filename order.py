__author__ = 'Matius Hurskainen'


#import main

class TooManyServedException(Exception):
    pass


class Order:
    total_orders = [0, 0, 0, 0] # Laskuri, jossa lasketaan kaikki jäljellä olevat tilaukset.

    def __init__(self, queue_number):
        self.__queue_number = queue_number
        self.__ordered_foods = [0, 0, 0, 0]
        self.__served_foods = [0, 0, 0, 0]

    def __del__(self): # Purkaja, en tiiä miten pitäis kutsua. (Automaagisesti???)
        print("hei hei!")

    def add_ordered_food(self, food_number):
        self.__ordered_foods[food_number] += 1
        Order.total_orders[food_number] += 1 # Lisätään jäljellä oleviin tilauksiin 1.

    def return_ordered_food(self):
        return self.__ordered_foods

    def serve_food(self,food_number):
        try:
            # Jos asiakkaalle yrittää antaa liian monta annosta, nostetaan virhe.
            if self.__served_foods[food_number] == self.__ordered_foods[food_number]:
                raise TooManyServedException()

            else:
                self.__served_foods[food_number] += 1
                Order.total_orders[food_number] -= 1 # Vähennetään jäljellä olevista tilauksista 1.

        except TooManyServedException:
            # Placeholder-tulostus, pitänee nostaa virhe ylemmäs ohjelmassa.
            print("Tried to serve too many dishes to customer.")

    def return_served_food(self):
        return self.__served_foods

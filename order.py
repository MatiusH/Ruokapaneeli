__author__ = 'Matius Hurskainen'


#import main

class TooManyServedException(Exception):
    pass


class Order:
    def __init__(self, queue_number):
        self.__queue_number = queue_number
        self.__ordered_foods = [0, 0, 0, 0]
        self.__served_foods = [0, 0, 0, 0]

    def add_ordered_food(self, food_number):
        self.__ordered_foods[food_number] += 1

    def return_ordered_food(self):
        return self.__ordered_foods

    def serve_food(self,food_number):
        try:
            if self.__served_foods[food_number] == self.__ordered_foods[food_number]:
                raise TooManyServedException()
            else:
                self.__served_foods[food_number] += 1
        except TooManyServedException:
            print("Tried to serve too many dishes to customer.")

    def return_served_food(self):
        return self.__served_foods

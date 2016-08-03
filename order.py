__author__ = 'Matius Hurskainen'


import main


class Order:
    def __init__(self, queue_number):
        self.__queue_number = queue_number
        self.__foods = [0, 0, 0, 0]


    def add_food(self, food_number):
        self.__foods[food_number] += 1



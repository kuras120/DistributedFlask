class Counter:
    def __init__(self, init_value=0):
        self.__data_to_count = init_value

    def add(self, number):
        self.__data_to_count += number

    def get(self):
        return self.__data_to_count

from abc import ABCMeta, abstractmethod

class Entry():

    def __init__(self, data : str):
        if(not self.validate(data)):raise TypeError
        self.__data = data

    def value(self) -> str:
        return self.__data

    def validate(self, data : str) -> bool:
        return False

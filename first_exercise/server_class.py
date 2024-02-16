import math
class Server:
    def __init__(self, id, status):
        self.__id = id
        self.__status = status
        self.__finish_time = math.inf
        self.__customer_served = None
    
    def get_id(self):
        return self.__id
    
    def get_status(self):
        return self.__status
    
    def get_finish_time(self):
        return self.__finish_time

    def set_status(self, new_status):
        self.__status = new_status
    
    def set_finish_time(self, new_time):
        self.__finish_time = new_time
    
    def get_customer(self):
        return self.__customer_served
    
    def assign_customer(self, customer_id):
        self.__customer_served = customer_id
    
    def remove_customer(self):
        self.__customer_served = None
        self.__finish_time = math.inf
    

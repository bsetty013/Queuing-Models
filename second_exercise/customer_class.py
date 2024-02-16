class Customer:
    def __init__(self, id, new_arrival_time, new_service_time, priority_given):
        self.__id = id
        self.__location = None
        self.__arrival_time = new_arrival_time
        self.__service_time = new_service_time
        self.__priority = priority_given
    
    def get_id(self):
        return self.__id
    
    def get_location(self):
        return self.__location
    
    def get_arrival_time(self):
        return self.__arrival_time
    
    def get_service_time(self):
        return self.__service_time
    
    def get_priority(self):
        return self.__priority
    
    def change_location(self, new_location):
        self.__location = new_location
    
    def set_priority(self, new_priority):
        self.__priority = new_priority
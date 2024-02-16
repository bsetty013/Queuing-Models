class Customer:
    def __init__(self, id, new_arrival_time, new_service_time):
        self.__id = id
        self.__location = None
        self.__arrival_time = new_arrival_time
        self.__service_time = new_service_time
    
    def get_id(self):
        return self.__id
    
    def get_location(self):
        return self.__location
    
    def get_arrival_time(self):
        return self.__arrival_time
    
    def get_service_time(self):
        return self.__service_time
    
    def change_location(self, new_location):
        self.__location = new_location
    

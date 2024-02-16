import numpy as np
from customer_class import Customer
from server_class import Server

class Simulate:
    def __init__(self, server_amount, customer_amount, mean_arrival, mean_service):
        self.__server_amount = server_amount
        self.__servers = []
        for i in range(server_amount):
            new_server = Server(i, "idle")
            self.__servers.append(new_server)
        self.__customers = []
        #Once this amount of customers is reached, simualtions will stop
        self.__customer_amount = customer_amount
        #Average Rate of Arrivals
        self.__mean_arrival_time = mean_arrival
        #Average Time for Service to be completed
        self.__mean_service_time = mean_service
    
    def get_server_amount(self):
        return self.__server_amount
    
    def get_servers(self):
        return self.__servers
    
    def get_customers(self):
        return self.__customers
    
    def get_a_customer(self, id):
        return self.__customers[id]
    
    def get_customer_amount(self):
        return self.__customer_amount
    
    def get_mean_arrival_time(self):
        return self.__mean_arrival_time
    
    def get_mean_service_time(self):
        return self.__mean_service_time
    
    def initialise_customers(self):
        """
            Creating all the customers that will arrive
            into the simualtion.
        """
        amount_of_customers = self.get_customer_amount()
        #Creaing poisson distribution of arrival times using average arrival rate
        arrival_times = np.random.poisson(self.get_mean_arrival_time(), amount_of_customers)
        #Creating exponential distribution of service times using average service time
        service_times = np.random.exponential(self.get_mean_service_time(), amount_of_customers)
        #First call will have an arrival time of 0
        self.__customers.append(Customer(0,0,service_times[0]))
        #Create customer objects for all calls and added to an array
        for i in range(1,amount_of_customers):
            this_arrival_time = arrival_times[i] + self.get_customers()[i-1].get_arrival_time()
            new_customer = Customer(i, this_arrival_time, service_times[i])
            self.__customers.append(new_customer)
    
    def find_server(self):
        """
            Searching through servers to see if there is a
            free server. If a free server is found, the server
            object is returned, otherwise None is returned
        """
        all_servers = self.get_servers()
        available_server = None
        for each_server in all_servers:
            this_status = each_server.get_status()
            if this_status == "idle":
                available_server = each_server
        return available_server
            
    def assign_customer_server(self,customer_index, customer_server, clock):
        """
            Method is called and executed when a call needs to be assigned
            a server.
        """
        new_customer = self.get_a_customer(customer_index)
        customer_server.set_status("busy")
        customer_server.assign_customer(customer_index)
        new_customer.change_location(customer_server)
        #Calculating the time that the customer will finish being served at the server
        server_finish_time = clock + new_customer.get_service_time()
        #Storing the finish time that will be calculated
        customer_server.set_finish_time(server_finish_time)
    
    def discard_customer(self, id):
        """
            Method is called when a call needs to be discarded
            from the simulation. This is either because the customer
            has been blocked or because the call is finished at
            the server.
        """
        customer = self.get_a_customer(id)
        customer.change_location("discarded")
    
    def check_servers(self, clock):
        """
            This method is called when there some
            customers may have to be removed from the
            simulation. 
        """
        all_servers = self.get_servers()
        finished_customers = 0
        #Searching through the servers
        for each_server in all_servers:
            #Seeing if the call is finished at this server
            finish_time = each_server.get_finish_time()
            if clock >= finish_time:
                server_customer_id = each_server.get_customer()
                #Stating that the server is free
                each_server.set_status("idle")
                each_server.remove_customer()
                self.discard_customer(server_customer_id)
                finished_customers += 1
    
    def update_area_status(self, area_server_status, time_diff):
        """
            Method is called during every iteration in the
            run_process() method, this helps calculate the
            server utilization after the simulation is complete.
        """
        #Searching through the server
        all_servers = self.get_servers()
        for server in all_servers:
            #Finding servers that are busy
            if server.get_status() == "busy":
                id = server.get_id()
                #Adding onto the current area status the
                #time passed since the last event
                area_server_status[id] += time_diff
        #Returning the updated area status' of all the servers
        return area_server_status
    
    def decide_next_event(self, incoming_customer, clock):
        """
            Method is called during every iteration of the
            run_process() method. Method is used to decide
            what the next event of the simulation is.
        """

        #Creating array of when all current calls will finish
        finish_times = []
        all_servers = self.get_servers()
        for server in all_servers:
            finish_times.append(server.get_finish_time())
        
        #Comparing the closest finish time of calls to the time of next arriving call
        if min(finish_times) < incoming_customer.get_arrival_time():
            next_event = "Departure"
            next_time = min(finish_times)
        else:
            next_event = "Arrival"
            next_time = incoming_customer.get_arrival_time()
        #Returning the decided next event in the simulation
        #Returning the new time stamp that the simulation is at
        return next_event, next_time


    def run_process(self):
        #Variable to track time passing through the simulation
        clock = 0
        #Id of the customer being currently served
        customer_index = 0
        #Amount of customers blocked
        customers_lost = 0
        #Creating all the calls that will arrive into the simulation
        self.initialise_customers()
        #Dictionary to store area status' of all servers
        area_server_status = {}
        for i in range(self.get_server_amount()):
            area_server_status[i] = 0
        #First event in simulation is an arrival
        next_event = "Arrival"
        while customer_index != self.get_customer_amount():
            incoming_customer = self.get_a_customer(customer_index)
            if next_event == "Departure":
                self.check_servers(clock)
            elif next_event == "Arrival":
                available_server = self.find_server()
                if available_server == None:
                    self.discard_customer(customer_index)
                    #Help calculate blocking probability
                    customers_lost += 1
                else:
                    # Assign the call a server to take palce at
                    self.assign_customer_server(customer_index, available_server, clock)
                customer_index += 1
            #Storing the current time
            last_time = clock
            #Deciding the next event in the simulation
            next_event_info = self.decide_next_event(incoming_customer, clock)
            #Storing what the next event in the simulation is
            next_event = next_event_info[0]
            #Storing the new time that the simulation is at
            clock = next_event_info[1]
            #Updating the area status' of all the servers
            area_server_status = self.update_area_status(area_server_status, (clock-last_time))
        return customers_lost, area_server_status, clock
        
    
    def calc_blocking_probability(self, loss_customers):
        #Divide the amount of customers being blocked by the amount of customers in the simualtion
        blocking_probability = loss_customers / self.get_customer_amount()
        return blocking_probability
    
    def calc_server_utilisation(self, area_server_status, clock):
        #Storing the area status of each server
        server_utilisation = []
        for i in range(self.get_server_amount()):
            server_utilisation.append(area_server_status[i] / clock)
        total_server_utilisation = sum(server_utilisation) / self.get_server_amount()
        return total_server_utilisation
        
        


            



from customer_class import Customer
from server_class import Server
import numpy as np

class Simulate:
    def __init__(self, server_amount, customer_amount, mean_service, new_arrival_rate, handover_arrival_rate, threshold):
        self.__server_amount = server_amount
        self.__servers = []
        for i in range(server_amount):
            new_server = Server(i, "idle")
            self.__servers.append(new_server)
        self.__customer_amount = customer_amount
        self.__service_times = np.random.exponential(mean_service, customer_amount)
        self.__new_arrival_rates = np.random.poisson(new_arrival_rate, customer_amount)
        self.__handover_arrival_rates = np.random.poisson(handover_arrival_rate, customer_amount)
        self.__threshold = threshold
    
    def get_server_amount(self):
        return self.__server_amount
    
    def get_servers(self):
        return self.__servers
    
    def get_customer_amount(self):
        return self.__customer_amount
    
    def get_new_rates(self):
        return self.__new_arrival_rates
    
    def get_handover_rates(self):
        return self.__handover_arrival_rates
    
    def get_service_times(self):
        return self.__service_times
    
    def get_threshold(self):
        return self.__threshold
    
    def generate_incoming_customer(self, customer_index, customer_type, clock):
        """
            This generates a new incoming customer with an arrival time that
            is greater than the current time passed through the simulation
        """
        if customer_type == "new":
            arrival_times = self.get_new_rates()
        elif customer_type == "handover":
            arrival_times = self.get_handover_rates()
        service_times = self.get_service_times()
        #First new call or first handover call arrive at time 0
        if customer_index == 0 or customer_index == 1:
            this_service_time = service_times[customer_index]
            incoming_customer = Customer(customer_index, 0, this_service_time, customer_type)
        else:
            #Exponentially distributed arrival time allocated
            this_arrival_time = arrival_times[customer_index] + clock
            #Value from poisson distribution allocated to customer
            this_service_time = service_times[customer_index]
            #Creating new customer class object
            incoming_customer = Customer(customer_index, this_arrival_time, this_service_time, customer_type)
        return incoming_customer
        
    def decide_next_event(self, new_arrival_time, handover_arrival_time):
        """
            Method is called and executed in every each iteration that
            takes place in the run_process() method. Method decides whether
            the next event is an arrival or departure.
        """
        #Storing when all the current calls at the servers will finish
        all_servers = self.get_servers()
        finish_times = []
        for server in all_servers:
            finish_times.append(server.get_finish_time())
        #Storing closest departure time and  closest arrival time       
        possible_next_events = {
            "Arrival": min([new_arrival_time, handover_arrival_time]),
            "Departure": min(finish_times)
        }
        #Key of min key value is the next event
        next_event =  min(possible_next_events, key=possible_next_events.get)
        #Min key value is the new time stamp the simulation is at
        increment_time = possible_next_events[next_event]
        return next_event, increment_time
    
    def find_free_server(self):
        """
            Method checks to see if a free server exists.
            If it does this server object will be returned,
            otherwise None will be returned.
        """
        all_servers = self.get_servers()
        available_server = None
        for server in all_servers:
            this_status = server.get_status()
            if this_status == "idle":
                available_server = server
        return available_server
    
    def find_idle_amount(self):
        """
            This method will find the amount of
            free servers. If this total gets higher
            to the threshold value this means new
            calls can be accepted. In this case
            True will be returned, otherwise False
            will be returned.
        """
        all_servers = self.get_servers()
        threshold = self.get_threshold()
        valid = False
        free_amount = 0
        for server in all_servers:
            this_status = server.get_status()
            if this_status == "idle":
                free_amount += 1
                if free_amount > threshold:
                    valid = True
                    break
        return valid

    def assign_customer_server(self,incoming_customer, customer_server, clock):
        """
            This method assigns a customer to a server
        """
        customer_server.set_status("busy")
        customer_server.assign_customer(incoming_customer)
        incoming_customer.change_location(customer_server)
        server_finish_time = clock + incoming_customer.get_service_time()
        customer_server.set_finish_time(server_finish_time)
    
    def decide_arrival(self, incoming_new, incoming_handover):
        """
            This method is called when the decision has been made
            that the next event is an arrival. In this method the
            decision is made whether the incoming new or handover call
            is accepted.
        """
        #Priority is given to handover calls if arrival times are equivalent
        if incoming_new.get_arrival_time() == incoming_handover.get_arrival_time():
            next_customer_type = "handover"        
        else:
            #Closest arrival time is found
            arrival_data = {
                "new":incoming_new.get_arrival_time(),
                "handover":incoming_handover.get_arrival_time()
            }
            #Customer with closest arrival time is call that will be accepted
            next_customer_type =  min(arrival_data, key=arrival_data.get)
        return next_customer_type

    
    def deal_with_arrival(self, incoming_customer, clock):
        """
            This method takes the appropriate action for an
            arriving customer.
        """
        #Search for an available server
        available_server = self.find_free_server()
        #Assert which type of call has arrived
        customer_type = incoming_customer.get_priority()
        call_loss = 0
        #Possibility that no servers are free
        if available_server == None:
            incoming_customer.change_location("discarded")
            call_loss = 1
        else:
            #Checking to see how many servers are free, before new call is accepted
            if customer_type == "new":
                new_valid = self.find_idle_amount()
                #Blocking if enough free servers are not available
                if new_valid == False:
                    incoming_customer.change_location("discarded") 
                    call_loss = 1
                else:
                    #Conditions have been met, new call is assigned a server
                    self.assign_customer_server(incoming_customer, available_server, clock)
            #Assigning a handover call a server
            elif customer_type == "handover":
                self.assign_customer_server(incoming_customer, available_server, clock)
        #Returning whether the call was blocked or not
        return call_loss

    def deal_with_departure(self, clock):
        """
            Method is called to check if there are calls
            that have finsihed and discarded from the
            simulation
        """
        all_servers = self.get_servers()
        for server in all_servers:
            this_finish_time = server.get_finish_time()
            #Checking if an calls have finished yet
            if clock >= this_finish_time:
                server_customer = server.get_customer()
                server.set_status("idle")
                server.remove_customer()
                server_customer.change_location("discarded")

    def run_process(self):
        customer_index = 1
        clock = 0
        #Generate new call
        incoming_new = self.generate_incoming_customer(0, "new", clock)
        #Generate handover call
        incoming_handover = self.generate_incoming_customer(1, "handover", clock)
        total_new = 1
        total_handover = 1
        new_loss = 0
        handover_loss = 0
        #Keep executing loop until limit of customers have been reached
        while customer_index != (self.get_customer_amount()-1):
            #Accessing arrival time of new customer
            new_arrival_time = incoming_new.get_arrival_time()
            #Accessing arrival of handover customer
            new_handover_time = incoming_handover.get_arrival_time()
            #Deciding next event int eh simulation
            next_event_info = self.decide_next_event(new_arrival_time, new_handover_time)
            next_event = next_event_info[0]
            #Storing new time that the simulation has reached
            clock = next_event_info[1]
            if next_event == "Arrival":
                #Decide which call is accepted
                next_type = self.decide_arrival(incoming_new, incoming_handover)
                #Deal with arrival and generate new arrival
                if next_type == "new":
                    #Arrival either blocked or assigned 
                    loss_amount = self.deal_with_arrival(incoming_new, clock)
                    #Increment total if call was blocked
                    new_loss += loss_amount
                    #Id of new customere
                    customer_index += 1
                    #Generate next new call      
                    incoming_new = self.generate_incoming_customer(customer_index, "new", clock)
                    total_new += 1
                elif next_type == "handover":
                    #Arrival either blocked or assigned
                    loss_amount = self.deal_with_arrival(incoming_handover, clock)
                    #Increment total if call was blocked
                    handover_loss += loss_amount
                    #Id of new customer
                    customer_index += 1
                    #Generate next handover call
                    incoming_handover = self.generate_incoming_customer(customer_index, "handover", clock)
                    total_handover += 1
            elif next_event == "Departure":
                #Search for calls that have finished, free up servers, and discard calls from simulation
                loss_info = self.deal_with_departure(clock)
        return total_new, total_handover, new_loss, handover_loss
    
    def calc_agg_blocking_prop(self, total_new, total_handover, loss_new, loss_handover):
        """
            Method is used to calculate aggregrate blocking probability of a simulation.
        """
        new_block = loss_new / total_new
        handover_block = loss_handover / total_handover
        agg_block = new_block + 10 * handover_block
        return agg_block

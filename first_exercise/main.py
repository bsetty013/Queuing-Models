from simulate import Simulate
import numpy as np
import matplotlib.pyplot as plt

""" new_simulation = Simulate(16, 100, 100, 0.1)
output_info = new_simulation.run_process()
print(new_simulation.calc_blocking_probability(output_info[0], output_info[1]))
print(new_simulation.calc_server_utilisation(output_info[2])) """

def second_exercise():
    arrival_times = [0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1]

    probs = []
    utils = []
    for arrival_time in arrival_times:
        inter_arrival = 1 / arrival_time
        new_simulation = Simulate(16, 10000, inter_arrival, 100)
        output_info = new_simulation.run_process()
        this_prob = new_simulation.calc_blocking_probability(output_info[0])
        this_util = new_simulation.calc_server_utilisation(output_info[1], output_info[2])
        probs.append(this_prob)
        utils.append(this_util)

    plt.figure("Figure 1")
    plt.plot(arrival_times,probs)
    plt.xlabel("Arrival Rate")
    plt.ylabel("Blocking Probability")

    plt.figure("Figure 2")
    plt.plot(arrival_times,utils)
    plt.xlabel("Arrival Rate")
    plt.ylabel("Server Utilisation")

    plt.show()

#second_exercise()

def third_exercise():
    new_call_rate = 0.01
    probs = []
    blocking_prob = 0
    while blocking_prob < 0.01:
        print("New Call Rate: ",new_call_rate)
        inter_arrival = 1 / new_call_rate
        new_simulation = Simulate(16, 10000, inter_arrival, 100)
        output_info = new_simulation.run_process()
        blocking_prob = new_simulation.calc_blocking_probability(output_info[0])
        print("Blocking Probability",blocking_prob)
        new_call_rate += 0.01

third_exercise()

#service_rate = 0.01

def comparison():
    new_call_rate = 0.01
    probs = []
    for i in range(10):
        print("New Call Rate: ",new_call_rate)
        inter_arrival = 1 / new_call_rate
        new_simulation = Simulate(16, 10000, inter_arrival, 100)
        output_info = new_simulation.run_process()
        server_util = new_simulation.calc_server_utilisation(output_info[1],output_info[2])
        print("Server Utilisation: ",server_util)
        new_call_rate += 0.01
#comparison()



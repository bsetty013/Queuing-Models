from simulate import Simulate



service_average = 100
customer_limit = 10000
C = 16
threshold = 2

def second_exercise(C, customer_limit, service_average, threshold):
    handover_rate = 0.0001
    new_call_rate = 0.1
    a_b_p = 0
    while a_b_p < 0.02:
        print("Handover Rate: ",handover_rate)
        new_simulation = Simulate(C, customer_limit, service_average, (1/new_call_rate), (1/handover_rate), 2)
        simulation_info = new_simulation.run_process()
        a_b_p = new_simulation.calc_agg_blocking_prop(simulation_info[0], simulation_info[1], simulation_info[2], simulation_info[3])
        print("Aggregrate: ",a_b_p)
        handover_rate += 0.01

#second_exercise(C, customer_limit, service_average, threshold)

def third_exercise(C, customer_limit, service_average, threshold):
    new_call_rate = 0.01
    handover_rate = 0.03
    a_b_p = 0
    while a_b_p < 0.019:
        print("New Call Rate: ",new_call_rate)
        new_simulation = Simulate(C, customer_limit, service_average, (1/new_call_rate), (1/handover_rate), 2)
        simulation_info = new_simulation.run_process()
        a_b_p = new_simulation.calc_agg_blocking_prop(simulation_info[0], simulation_info[1], simulation_info[2], simulation_info[3])
        print("Aggregrate: ",a_b_p)
        new_call_rate += 0.01
third_exercise(C, customer_limit, service_average, threshold)
import math

def validate_blocking_prob(LAMBDA, MU, C):
    numerator = ((LAMBDA/MU)**C) / math.factorial(C)
    denominator = 0
    for k in range(C+1):
        denominator += (LAMBDA/MU)**k / math.factorial(k)
    return numerator/denominator

LAMBDA = 0.5
for i in range(10):
    #print("Blocking Probability: ")
    blocking_prob = validate_blocking_prob(LAMBDA,0.01,16)
    #print(blocking_prob)
    LAMBDA += 0.01

def validate_server_utilisation(LAMBDA, C, MU):
    return LAMBDA / (C * MU)

LAMBDA = 0.01
for i in range(10):
    print("Arrival Rate: ",LAMBDA)
    server_util = validate_server_utilisation(LAMBDA,16,0.01)
    print("Server Utilisation: ",server_util)
    LAMBDA += 0.01



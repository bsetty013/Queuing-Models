import math

def calc_p_zero(lambda_one, lambda_two, mu, c):
    total = 0
    for i in range(c):
        total += ((lambda_one + lambda_two)**i) / math.factorial(i) * mu**i
    return 1 / total

def calc_p_k(lambda_one, lambda_two, mu, c, p0, k, n):
    if k >= 0 and k <= (c-n):
        return 1/math.factorial(k) * ((lambda_one + lambda_two)/mu)**k * p0
    elif k >= (c-n+1) and k <= c:
        return 1/math.factorial(k) * ((lambda_one + lambda_two)/mu)**(c-n) * (lambda_one/mu)**(k-(c-n)) * p0

def calc_loss(lambda_one, lambda_two, mu, c, p0, k, n):
    loss = 0
    for k in range (c-n):
        p0 = calc_p_zero(lambda_one, lambda_two, mu, c)
        loss += calc_p_k(lambda_one, lambda_two, mu, c, p0, k, n)
    return loss



        
        



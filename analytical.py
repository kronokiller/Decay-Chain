from math import exp, log

# Solve for an analytical solution of the triple decay chain at time t given initial conditions
def analyticalSolution(lambda_A, lambda_B, N_A0, N_B0, N_C0, delta_t, t_final, t):
    # d/dt (N_A) = - lambda_A * N_A
    N_A = N_A0 * exp(-lambda_A * t)

    # d/dt (N_B) = lambda_A * N_A - lambda_B * N_B
    N_B = N_B0 * exp(-lambda_B * t) + (lambda_A * N_A0) * (exp(-lambda_A * t) - exp(-lambda_B * t)) / (lambda_B - lambda_A)

    # d/dt (N_C) = lambda_B * N_B
    N_C = N_C0 + N_B0 * (1 - exp(-lambda_B * t)) + N_A0 * (lambda_B * (1 - exp(-lambda_A * t)) - lambda_A * (1 - exp(-lambda_B * t))) / (lambda_B - lambda_A)

    return (N_A, N_B, N_C)

def calculateAnalyticalMaxN_B(lambda_A, lambda_B, N_A0, N_B0, N_C0, delta_t, t_final):
    # d/dt(N_B) = 0
    # N_B = N_B0 * exp(-lambda_B * t) + (lambda_A * N_A0) * (exp(-lambda_A * t) - exp(-lambda_B * t)) / (lambda_B - lambda_A)
    t = 1 / (lambda_B - lambda_A) * log((N_B0 * lambda_B - lambda_A * lambda_B * N_A0 / (lambda_B - lambda_A)) / (-lambda_A ** 2 * N_A0 / (lambda_B - lambda_A)))
    return (analyticalSolution(lambda_A, lambda_B, N_A0, N_B0, N_C0, delta_t, t_final, t)[1], t)

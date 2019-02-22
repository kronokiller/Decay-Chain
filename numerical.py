# Placeholders are used for unused data from unpacked tuples
def numericalSolution(lambda_A, lambda_B, a, b, c, delta_t, d, e, f, g, h, N_A, N_B, N_C, i):
    # Calculate the amount of each decay and add or subtract it to the relevant counts

    # N_A(t + delta_t) = N_A(t) + deltaN_A(t)
    # deltaN_A(t) = - lambda_A * N_A * delta_t
    # N_B(t + delta_t) = N_B(t) + deltaN_B(t)
    # deltaN_B(t) = (lambda_A * N_A - lambda_B * N_B) * delta_t
    # N_C(t + delta_t) = N_C(t) + deltaN_C(t)
    # deltaN_C(t) = lambda_B * N_B * delta_t

    N_Adecay = delta_t * lambda_A * N_A
    N_Bdecay = delta_t * lambda_B * N_B

    N_A -= N_Adecay
    N_B += N_Adecay - N_Bdecay
    N_C += N_Bdecay
    return (N_A, N_B, N_C, N_A + N_B + N_C)

def calculateNumericalMaxN_B(data):
    # Get the data point with max N_B
    point = max(data, key = lambda p : p[5])

    # Return the time and N_B of this point
    return (point[5], point[0])

def checkRepeat(data1, data2, significance):
    # Check if any of the numerical counts change significantly from one data set to the next
    # i is the index of the data point in data1
    for i in range(len(data1)):
        # j is the index of the data point which contains the numerical values of N_A, N_B, and N_C
        for j in range(4, 7):
            # Check for a difference of 0.05% of the total atoms in any amount
            if not(- data1[i][7] * significance <= data1[i][j] - data2[i * 2][j] <= data1[i][7] * significance):
                return True
    # If nothing changes significantly, don't repeat
    return False

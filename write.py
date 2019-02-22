from os import listdir
from math import log10, floor


def getOutputNumber(directory):
    # List the files in the directory and add the file names starting with output and ending with .txt to a list after stripping the first and last portions
    strippedFileNames = [file[6:-4] for file in listdir(directory) if len(file) >= 10 and file[:6] == 'output' and file[-4:] == '.txt']

    # List all output file numbers used
    usedNumbers = []
    for name in strippedFileNames:
        # Check that the identified portion of the string is an integer
        try:
            usedNumbers.append(int(name))
        except ValueError:
            pass

    # Iterate through the output file numbers until an empty space an unused number
    number = 0
    while number in usedNumbers:
        number += 1

    # Return the first unused number
    return str(number)

def writeOutput(outputFile, data, initialValues, analyticalMaxN_B, numericalMaxN_B):
    # Get the maximum amount of space needed for a time value based on the time delta and the final time
    if isinstance(initialValues[-2], int):
        timeWidth = int(floor(log10(initialValues[-1])) + 1)
    elif isinstance(initialValues[-2], float):
        timeWidth = len(str(initialValues[-2]))
        if initialValues[-1] >= 1:
            timeWidth += int(floor(log10(initialValues[-1])) + 1)
    else:
        # The time should always be either a float or an int
        raise ValueError('Time Delta should be a float or an int')

    # If less than 4 digits are required to represent the time, use 4 digits to contain the header
    if timeWidth < 4:
        timeWidth = 4

    # Write and close the output file using this information
    writeInitial(outputFile, *initialValues)
    writeOutputHeader(outputFile, timeWidth, analyticalMaxN_B, numericalMaxN_B)
    writeData(outputFile, timeWidth, data)
    outputFile.close()

def writeInitial(outputFile, lambda_A, lambda_B, N_A0, N_B0, N_C0, delta_t, t_final):
    # Rewrite the initial file but with units of atoms and seconds or seconds inverse
    outputFile.write(('Input Data\n----------\n\n'
        'Decay Rate A = {} /s\n'
        'Decay Rate B = {} /s\n'
        'Initial Count A = {}\n'
        'Initial Count B = {}\n'
        'Initial Count C = {}\n'
        'Time Delta = {} s\n'
        'Final Time = {} s\n\n\n'
        ).format(lambda_A, lambda_B, N_A0, N_B0, N_C0, delta_t, t_final))

def writeOutputHeader(outputFile, timeWidth, analyticalMaxN_B, numericalMaxN_B):
    # Write the header of the data tables
    outputFile.write((
        'Output Data\n' +
        '-----------\n\n' +
        'Max N(B)\n' +
        '--------\n'
        'Analytical : {0} at t = {1} s\n' +
        'Numerical  : {2} at t = {3} s\n\n' +
        '{4:^' + str(timeWidth) + '}     {5:^44}   {6:^59}\n' +
        '{7:^' + str(timeWidth) + '}     {8:^14}|{9:^14}|{10:^14}     {8:^14}|{9:^14}|{10:^14}|{11:^14}\n' +
        '-' * timeWidth + ('     ' + '-' * 14 + '|' + '-' * 14 + '|' + '-' * 14) * 2 + '|' + '-' * 14 + '\n'
        ).format(*analyticalMaxN_B, *numericalMaxN_B, 'Time', 'Analytical', 'Numerical', '(s)', 'N (A)', 'N (B)', 'N (C)', 'N (total)'))

def writeData(outputFile, timeWidth, data):
    # Write the values for each data point
    for point in data:
        outputFile.write(('{:>' + str(timeWidth) + '}     '
            '{:<14.9G}|{:<14.9G}|{:<14.9G}     {:<14.9G}|{:<14.9G}|{:<14.9G}|{:<14.9G}\n').format(*point))

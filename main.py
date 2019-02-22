from inspect import getsourcefile
from os.path import abspath, dirname
from os import chdir
from read import readInput, readSettings
from write import writeOutput, getOutputNumber
from analytical import analyticalSolution, calculateAnalyticalMaxN_B
from numerical import numericalSolution, calculateNumericalMaxN_B
from plotting import makeReferenceGraph, makeFinalGraphs
from check import checkRepeat
from matplotlib.pyplot import show, clf

def main(run, generate, multiple, significance, initialValues = None, previousData = None):
    if run:
        # Open the output file to be written
        fileNum = getOutputNumber(directory)
        outputFile = open('output' + fileNum + '.txt', 'w')

        # Open and read the input file or use previous initial values with half time delta
        if initialValues != None:
            initialValues = (*initialValues[:-2], initialValues[-2] / 2, initialValues[-1])

        else:
            inputFile = open("input.txt", 'r')
            initialValues = readInput(inputFile)
        lambda_A, lambda_B, N_A0, N_B0, N_C0, delta_t, t_final = initialValues

        # Preallocate space for the data so that it may be populated with tuple references
        size = int(t_final // delta_t + 1)
        data = size * [None]

        # Skip calculations of the t = 0 data point because the initial conditions are given
        data[0] = (0, N_A0, N_B0, N_C0, N_A0, N_B0, N_C0, N_A0 + N_B0 + N_C0)
        previousValues = data[0]

        # Calculate the analytical and numerical solutions every delta_t between 0 < t <= t_final
        for i in range(1, size):
            data[i] = ((i * delta_t, *analyticalSolution(*initialValues, i * delta_t), *numericalSolution(*initialValues, *previousValues)))
            previousValues = data[i]

        # Caluclate the maximum value and time of N_B analytically and numerically
        analyticalMaxN_B = calculateAnalyticalMaxN_B(*initialValues)
        numericalMaxN_B = calculateNumericalMaxN_B(data)

        # Write the output file
        writeOutput(outputFile, data, initialValues, analyticalMaxN_B, numericalMaxN_B)

        # Make the reference graphs if asked for in the settings
        if generate:
            makeReferenceGraph(initialValues, data, 'image' + fileNum + '.png')

    # Repeat if there has only been one iteration or if there is a significant difference (0.05% of the total number of atoms, if 100 total atoms then 0.1 atoms) in any of the points.
    # Also show the final plot or clear the plot to be repopulated in the next iteration.
    # Don't repeat if multiple setting is False
    if multiple and (previousData == None or checkRepeat(previousData, data, significance)):
        if generate:
            clf()
        main(run, generate, multiple, significance, initialValues = initialValues, previousData = data)
    elif generate:
        show()

# Get the directory of main.py and make it the current working directory
directory = dirname(abspath(getsourcefile(lambda:0)))
chdir(directory)

# Read the settings file
(run, generate, multiple, significance, plot, *plotInfo) = readSettings(open('settings.txt'))
main(run, generate, multiple, significance)
if plot:
    makeFinalGraphs(*plotInfo)



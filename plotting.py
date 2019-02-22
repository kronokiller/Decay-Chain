from matplotlib.pyplot import plot, show, ylabel, xlabel, title, savefig, legend, clf
from read import readOutput


# Either input in command line after prompts with userInput = True or at the bottom of this file with userInput = False
userInput = False

def makeReferenceGraph(initialValues, data, path):
    # Set a limit to the number of points graphed on the reference graphs
    maxPoints = 400

    # Pick points by dividing the indices of the data in increments of 1/399 times the total number of points and rounding so that the first and last points are included
    numPoints = len(data)
    if numPoints > maxPoints:
        # numPoints - 1  is the largest index and maxPoints - 1 is the largest value in range(maxPoints)
        data = [data[round(j * (numPoints - 1)/ (maxPoints - 1))] for j in range(maxPoints)]

    # Get the data values as 8 lists instead of 1 list of tuples containing 8 elements each
    # a denotes analytical and n denotes numerical
    t, N_Aa, N_Ba, N_Ca, N_An, N_Bn, N_Cn, N_total = ([point[i] for point in data] for i in range(8))

    # Plot and save the graph
    plot(t, N_An, 'r', t, N_Aa, 'r--', t, N_Bn, 'g', t, N_Ba, 'g--', t, N_Cn, 'b', t, N_Ca, 'b--', t, N_total, 'black')
    ylabel('N (atoms)')
    xlabel('Time (s)')
    title(r'$\Delta$ t = ' + str(initialValues[-2]) + ' s')
    legend([r'$N_A$  (Numerical)', r'$N_A$  (Analytical)', r'$N_B$  (Numerical)', r'$N_B$  (Numerical)', r'$N_C$  (Analytical)', r'$N_C$  (Analytical)', r'$N_{Total}$ (Numerical)'])
    savefig(path, format = 'png')

def plotN_Bvs_t(path_coarse, path_medium, path_fine, imageName):
    # Get the data from the 3 files
    data_coarse = readOutput(open(path_coarse, 'r'))[3]
    data_medium = readOutput(open(path_medium, 'r'))[3]
    data_fine = readOutput(open(path_fine, 'r'))[3]

    # Separate the data into lists
    (Xcoarse, Ycoarse) = ([point[i] for point in data_coarse] for i in [0, 5])
    (Xmedium, Ymedium) = ([point[i] for point in data_medium] for i in [0, 5])
    (Xfine, Yanalytical, Yfine) = ([point[i] for point in data_fine] for i in [0, 2, 5])

    # Plot and save the graph with high resolution
    plot(Xcoarse, Ycoarse, 'g', Xmedium, Ymedium, 'b', Xfine, Yfine, 'r', Xfine, Yanalytical, 'black')
    ylabel('N (atoms)')
    xlabel('Time (s)')
    title(r'$N_B$ vs t')
    legend(['Coarse', 'Medium', 'Fine', 'Analytical'])
    savefig(imageName, format = 'png', dpi = 1200)
    clf()

def plotNumerical(path_fine, imageName):
    # Get the data from the file
    data_fine = readOutput(open(path_fine, 'r'))[3]

    # Split the data into relevant lists
    (t, N_A, N_B, N_C, N_total) = ([point[i] for point in data_fine] for i in [0, 4, 5, 6, 7])

    # Plot and save the graph with high resolution
    plot(t, N_A, 'r', t, N_B, 'g', t, N_C, 'b', t, N_total, 'black')
    ylabel('N (atoms)')
    xlabel('Time (s)')
    title('N vs t')
    legend([r'$N_A$', r'$N_B$', r'$N_C$', r'$N_T$'])
    savefig(imageName, format = 'png', dpi = 1200)
    clf()

def plotMaxN_BvsDelta_t(pathList, imageName):
    # Make arrays to append to
    x = []
    y = []

    # get the time delta and max time from each file
    for path in pathList:
        (inputValues, maxAnalyticalN_B, maxNumericalN_B, data) = readOutput(open(path), excludeData = True)
        x.append(1 / inputValues[-2])
        y.append(maxNumericalN_B[1])

    # Plot and save the graph with high resolution
    plot(x, y)
    ylabel('Time (s)')
    xlabel(r'Inverse Time Delta ($s^{-1}$)')
    title(r'Time of $N_B$ max vs $\frac{1}{\Delta t}$')
    savefig(imageName, format = 'png', dpi = 1200)
    clf()

def makePathList(numList):
    if isinstance(numList, list):
        return ['output' + num + '.txt' for num in numList]
    elif isinstance(numList, str):
        # Remove whitespace
        numList = ''.join(numList.split())

        # Remove square brackets
        if numList[0] == '[':
            numList = numList[1:]
        if numList[-1] == ']':
            numList = numList[:-1]

        # Split the list at the commas and send it back into the function as a list
        return makePathList(numList.split(','))

def makeFinalGraphs(userInput, image1Name, image2Name, image3Name, coarseNum, mediumNum, fineNum, numList):
    if userInput:
        # Ask the user for input to create and save the three required figures
        plotN_Bvs_t(*makePathList([input('N_B vs t\nGive the number of the output file to be used as the coarse line: '),
            input('Give the number of the output file to be used as the medium line: '),
            input('Give the number of the output file to be used as the fine line: ')]),
            input('Give the name that the image file should be saved as (excluding the extension): ') + '.png')
        plotNumerical('output' + input('\nNumerical Solution\nGive the number of the output file to be used for the numerical solution: ') + '.txt',
            input('Give the name that the image file should be saved as (excluding the extension): ') + '.png')
        plotMaxN_BvsDelta_t(makePathList(input('\nmax N_B vs Delta t\nGive a list of output files to be used as a comma separated list of output file numbers: ')),
            input('Give the name that the image file should be saved as (excluding the extension): ') + '.png')

    else:
        # Same except with the inputs used to generate the graphs included
        plotN_Bvs_t(*makePathList([coarseNum,
            mediumNum,
            fineNum]),
            image1Name + '.png')
        plotNumerical('output' + fineNum + '.txt',
            image2Name + '.png')
        plotMaxN_BvsDelta_t(makePathList(numList),
            image3Name + '.png')

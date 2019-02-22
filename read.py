from math import log


# Define units and unit conversions to 1 second and 1 atom
ratioUnits = ['', '%']
timeUnits = ['s', 'm', 'h', 'd', 'y']
countUnits = ['', 'mol']
convert = {'s' : 1, 'm' : 60, 'h' : 3600, 'd' : 86400, 'y' : 31557600, 'mol' : 6.0221408E23, '' : 1, '%' : 0.01 }

# Define a default error message to precede any error message
errorMessage = 'Error in line {} of {}.txt,'

def expect(received, expected, argNum, lineNum, s):
    # Format the expected string as the received string was formatted
    adjusted = ''.join(expected.split()).lower()

    # If many arguments are expected let the argNum be the amount of commas + 1
    if argNum == 'many':
        argNum = received.count(',') + 1

    # Check if the received line and number of arguments matches and that there is exactly one "="
    if received.lower()[:len(adjusted)] != adjusted or received.count(',') != argNum - 1 or received.count('=') != 1:
        # If not, raise an exception
        raise(Exception(errorMessage.format(lineNum, s) + ' expected "' + expected + '" followed by ' + str(argNum) + ' comma separated arguments'))


def checkUnits(str, argNum, lineNum, s, unitList):
    # Check that the units are in the relevant unit list
    if str not in unitList:
        raise(Exception(errorMessage.format(lineNum, s) + ' Expected a unit in', unitList,  'as argument number', argNum))


def checkFloat(str, argNum, lineNum, s):
    # Check that the float argument can be cast as a float
    try:
        float(str)
    except(ValueError):
        raise(Exception(errorMessage.format(lineNum, s) + ' expected a float as a decimal or in scientific notation as argument number' + str(argNum)))

def checkTruth(str, lineNum, s):
    # Check that the value is true, t, false, or f
    if str not in ['true', 't', 'false', 'f']:
        raise(Exception(errorMessage.format(lineNum, s) + 'Expected "True" or "False"'))

def checkDigits(str, lineNum, s):
    # Check that all of the characters are digits
    for ch in str:
        if ch not in '0123456789':
            raise(Exception(errorMessage.format(lineNum, s) + 'Expected only digits'))

def getArgList(line):
    # Separate the initial condition's name from the arguments and separate the arguments at the commas to return a list
    return line.split('=')[1].split(',')


def getLambda(line, lineNum, s):
    # Extract the arguments from the line
    argList = getArgList(line)

    # Determine which decay rate is given and convert to a decay constant in seconds inverse
    if argList[0] == "half-life":
        checkFloat(argList[1], 2, lineNum, s)
        checkUnits(argList[2], 3, lineNum, s, timeUnits)
        return log(2) / float(argList[1]) / convert[argList[2]]

    elif argList[0] == "decayconstant":
        checkFloat(argList[1], 2, lineNum, s)
        checkUnits(argList[2], 3, lineNum, s, timeUnits)
        return float(argList[1]) / argList[2]

    elif argList[0] == "meanlifetime":
        checkFloat(argList[1], 2, lineNum, s)
        checkUnits(argList[2], 3, lineNum, s, timeUnits)
        return 1 / float(argList[1]) / convert[argList[2]]

    # If none of these values are specified, raise an error
    else:
        raise(Exception(errorMessage.format(lineNum, s) + ' expected "half-life", "decay constant", or "mean lifetime" as the first argument'))


def getCount(line, lineNum, s):
    # Extracts the arguments from the line
    argList = getArgList(line)

    # Check the number and the units
    checkFloat(argList[0], 1, lineNum, s)
    checkUnits(argList[1], 2, lineNum, s, countUnits)

    # return the number of molecules
    return float(argList[0]) * convert[argList[1]]

def getNum(line, lineNum, s):
    # Extracts the arguments from the line
    argList = getArgList(line)

    # Check the number and the units
    checkDigits(argList[0], lineNum, s)

    # return the number as a string
    return argList[0]


def getRatio(line, lineNum, s):
    # Extracts the arguments from the line
    argList = getArgList(line)

    # Check the number and the units
    checkFloat(argList[0], 1, lineNum, s)
    checkUnits(argList[1], 2, lineNum, s, ratioUnits)

    # return the number of as a decimal
    return float(argList[0]) * convert[argList[1]]

def getFileName(line, lineNum, s):
    # Extract the arguments from the line
    argList = getArgList(line)

    # return the file name without .png
    if '.png' == argList[0][-4:]:
        return argList[0][:-4]
    return argList[0]


def getTime(line, lineNum, s):
    # Extracts the arguments from the line
    argList = getArgList(line)

    # Check the number and the units
    checkFloat(argList[0], 1, lineNum, s)
    checkUnits(argList[1], 2, lineNum, s, timeUnits)

    # Convert to seconds
    time = float(argList[0]) * convert[argList[1]]

    # Return an in if possible
    if time % 1 == 0:
        return int(time)
    else:
        return float(time)

def getTruth(line, lineNum, s):
    #Extracts the arguments from the line
    argList = getArgList(line)

    # Check that the input is a truth value
    checkTruth(argList[0], lineNum, s)
    if argList[0] in ['true', 't']:
        return True
    else:
        return False

def getList(line, lineNum, s):
    # Extracts the arguments from the line
    argList = getArgList(line)

    # Check that the arguments are just numbers and compile the list
    l = []
    for el in argList:
        checkDigits(el, lineNum, s)
        l.append(el)

    return l

def readInput(inputFile):
    # Define a variable to use in error messages
    s = 'input'

    # Define variables to keep track of the expected datum and the line of the file
    datumNum = 0
    lineNum = 0

    # Gather input data from the input file
    for line in inputFile:
        lineNum += 1

        # Remove whitespace and make all letters lowercase
        line = ''.join(line.split()).lower()

        # Ignore commented and empty lines
        if line != '' and line[0] != '#':

            # Verify that the line is the expected line and formatting and get the value if so
            if datumNum == 0:
                expect(line, "Decay Rate A =", 3, lineNum, s)
                lambda_A = getLambda(line, lineNum, s)
                datumNum += 1
            elif datumNum == 1:
                expect(line, "Decay Rate B =", 3, lineNum, s)
                lambda_B = getLambda(line, lineNum, s)
                datumNum += 1
            elif datumNum == 2:
                expect(line, "Initial Count A =", 2, lineNum, s)
                N_A0 = getCount(line, lineNum, s)
                datumNum += 1
            elif datumNum == 3:
                expect(line, "Initial Count B =", 2, lineNum, s)
                N_B0 = getCount(line, lineNum, s)
                datumNum += 1
            elif datumNum == 4:
                expect(line, "Initial Count C =", 2, lineNum, s)
                N_C0 = getCount(line, lineNum, s)
                datumNum += 1
            elif datumNum == 5:
                expect(line, "Time Delta =", 2, lineNum, s)
                Delta_t = getTime(line, lineNum, s)
                datumNum += 1
            elif datumNum == 6:
                expect(line, "Final Time =", 2, lineNum, s)
                t_final = getTime(line, lineNum, s)
                datumNum += 1

    return (lambda_A, lambda_B, N_A0, N_B0, N_C0, Delta_t, t_final)

def readOutput(outputFile, excludeData = False):
    # Iterate over all of the lines in the file and retrieve relevant data
    lineNum = 0
    data = []
    inputValues = []
    for line in outputFile:
        lineNum += 1

        # Get the input values
        if 3 < lineNum < 11:
            inputValue = line.split(' = ')[1]
            if '/s' in inputValue:
                inputValue = inputValue[:-3]
            elif 's' in inputValue:
                inputValue = inputValue[:-2]
            inputValues.append(float(inputValue))

        # Get the analytical max of N_B
        if lineNum == 18:
            maxAnalyticalN_B = line.split(' at t = ')
            maxAnalyticalN_B[0] = float(maxAnalyticalN_B[0].split(' : ')[1])
            maxAnalyticalN_B[1] = float(maxAnalyticalN_B[1].split(' s')[0])

        # Get the numerical max of N_B
        if lineNum == 19:
            maxNumericalN_B = line.split(' at t = ')
            maxNumericalN_B[0] = float(maxNumericalN_B[0].split(' : ')[1])
            maxNumericalN_B[1] = float(maxNumericalN_B[1].split(' s')[0])
            if excludeData:
                break

        # Get the size of the columns
        if lineNum == 23:
            # Split the line by the column table separator
            timeSize = len(line[:-1].split('     ')[0])
            countSize = 14
            separatorSize = 5

        if lineNum >= 24:
            # Get each data point from the tables
            t = float(line[:timeSize])
            N_Aa = float(line[timeSize + separatorSize : timeSize + separatorSize + countSize])
            N_Ba = float(line[timeSize + separatorSize + countSize + 1 : timeSize + separatorSize + 2 * countSize + 1])
            N_Ca = float(line[timeSize + separatorSize + 2 * countSize + 2 : timeSize + separatorSize + 3 * countSize + 2])
            N_An = float(line[timeSize + 2 * separatorSize + 3 * countSize + 2 : timeSize + 2 * separatorSize + 4 * countSize + 2])
            N_Bn = float(line[timeSize + 2 * separatorSize + 4 * countSize + 3 : timeSize + 2 * separatorSize + 5 * countSize + 3])
            N_Cn = float(line[timeSize + 2 * separatorSize + 5 * countSize + 4 : timeSize + 2 * separatorSize + 6 * countSize + 4])
            N_Total = float(line[timeSize + 2 * separatorSize + 6 * countSize + 5 : timeSize + 2 * separatorSize + 7 * countSize + 5])

            # Append it to the list of data points as a tuple
            data.append((t, N_Aa, N_Ba, N_Ca, N_An, N_Bn, N_Cn, N_Total))
    return (inputValues, maxAnalyticalN_B, maxNumericalN_B, data)

# Use readInput as a template for readSettings
def readSettings(settingsFile):
    # Define a string to use in error messages
    s = 'settings'

    # Define variables to keep track of the expected datum and the line of the file
    datumNum = 0
    lineNum = 0

    # Gather input data from the input file
    for line in settingsFile:
        lineNum += 1

        # Remove whitespace and make all letters lowercase if not looking for a file name
        if 5 < datumNum < 9:
            line = ''.join(line.split())
        else:
            line = ''.join(line.split()).lower()

        # Ignore commented and empty lines
        if line != '' and line[0] != '#':

            # Verify that the line is the expected line and formatting and get the value if so
            if datumNum == 0:
                expect(line, "Run Main =", 1, lineNum, s)
                run = getTruth(line, lineNum, s)
                datumNum += 1
            elif datumNum == 1:
                expect(line, "Generate Reference Graphs =", 1, lineNum, s)
                generate = getTruth(line, lineNum, s)
                datumNum += 1
            elif datumNum == 2:
                expect(line, "Run Multiple =", 1, lineNum, s)
                multiple = getTruth(line, lineNum, s)
                datumNum += 1
            elif datumNum == 3:
                expect(line, "Percent of Total =", 2, lineNum, s)
                significance = getRatio(line, lineNum, s)
                datumNum += 1
            elif datumNum == 4:
                expect(line, "Plot =", 1, lineNum, s)
                plot = getTruth(line, lineNum, s)
                datumNum += 1
            elif datumNum == 5:
                expect(line, "User Input for Plotting =", 1, lineNum, s)
                userInput = getTruth(line, lineNum, s)
                datumNum += 1
            elif datumNum == 6:
                expect(line, "Image 1 Name =", 1, lineNum, s)
                image1Name = getFileName(line, lineNum, s)
                datumNum += 1
            elif datumNum == 7:
                expect(line, "Image 2 Name =", 1, lineNum, s)
                image2Name = getFileName(line, lineNum, s)
                datumNum += 1
            elif datumNum == 8:
                expect(line, "Image 3 Name =", 1, lineNum, s)
                image3Name = getFileName(line, lineNum, s)
                datumNum += 1
            elif datumNum == 9:
                expect(line, "Coarse Data Number =", 1, lineNum, s)
                coarseNum = getNum(line, lineNum, s)
                datumNum += 1
            elif datumNum == 10:
                expect(line, "Medium Data Number =", 1, lineNum, s)
                mediumNum = getNum(line, lineNum, s)
                datumNum += 1
            elif datumNum == 11:
                expect(line, "Fine Data Number =", 1, lineNum, s)
                fineNum = getNum(line, lineNum, s)
                datumNum += 1
            elif datumNum == 12:
                expect(line, "Data Numbers =", 'many', lineNum, s)
                numList = getList(line, lineNum, s)
                datumNum += 1

    return (run, generate, multiple, significance, plot, userInput, image1Name, image2Name, image3Name, coarseNum, mediumNum, fineNum, numList)

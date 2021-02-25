import numpy as np

def electrodesToVertHori(electrodeSignals, leftInd, rightInd, downInd, upInd):
    # Subtraction of the signals
    leftElec = electrodeSignals[leftInd]
    rightElec = electrodeSignals[rightInd]
    downElec = electrodeSignals[downInd]
    upElec = electrodeSignals[upInd]

    verticalEOG = np.subtract(upElec, downElec)
    horizontalEOG = np.subtract(leftElec, rightElec)

    return verticalEOG, horizontalEOG
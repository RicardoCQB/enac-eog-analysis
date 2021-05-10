import numpy as np

def electrodesToVertHori(electrodeSignals, leftInd, rightInd, downInd, upInd):
    '''
    Transforms the individual electrode signals into the vertical and horizontal EOG.
    :param electrodeSignals: 4 channels/signals with each corresponding to the signal of one electrode
    Assuming the EOG is read using 4 electrodes, the next parameters are the indexes of those 4 channels.
    :param leftInd:
    :param rightInd:
    :param downInd:
    :param upInd:
    :return:
    '''
    # Subtraction of the signals
    leftElec = electrodeSignals[leftInd]
    rightElec = electrodeSignals[rightInd]
    downElec = electrodeSignals[downInd]
    upElec = electrodeSignals[upInd]

    verticalEOG = np.subtract(upElec, downElec)
    horizontalEOG = np.subtract(leftElec, rightElec)

    return verticalEOG, horizontalEOG

def cutArtifacts(signal, numCut):
    # Returns signal a certain number of elements cut from the start and end of the signal
    return signal[numCut:-numCut]
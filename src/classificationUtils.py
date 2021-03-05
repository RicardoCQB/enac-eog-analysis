import numpy as np

def peaksToBinary(peaksArray, eogCWT):
    '''
    This function turns an array with the peaks of the eog CWT into an array of 0's and 1's
    The 0's represent negative peaks and the 1´s represent positive peaks
    :param peaksArray: array with the indexes of the peaks of the eogCWT
    :param eogCWT: eog signal array after the continuous wavelet transform
    :return: peaks binary array
    '''

    # Create array with same length as the signal and transform peaks into 0 (negative peak) and 1 (positive peak)
    peaksBinary = np.zeros(len(peaksArray))
    for i, peakV in enumerate(peaksArray):
        if eogCWT[peakV] < 0:
            peaksBinary[i] = 0
        elif eogCWT[peakV] > 0:
            peaksBinary[i] = 1

    return peaksBinary


def peaksBinaryToString(peaksBinary):
    '''
    Turns the array with the binary code for the negative and positive peaks and turns it into to a string
    :param peaksBinary: rray with the binary code for the negative and positive peaks
    :return: returns a string with 0's and 1's
    '''

    peaksString = np.array2string(peaksBinary.astype(int))

    peaksString = peaksString.replace(' ', '')
    peaksString = peaksString.replace('[', '')
    peaksString = peaksString.replace(']', '')

    return peaksString


def countEyeMovements(vertPeaksString, horiPeaksString):
    '''
    This function counts the number of each type movement that occur in the signal based on codes that define them
    On the verticalEOG: 0110 represents an upwards saccade and 1001 represents a downwards saccade
    On the horizontal EOG: 0110 represents a left saccade and 1001 represents a right saccade
    :param vertPeaksString: 0's and 1's representing the negative and positive peaks of the vertical EOG signal
    :param horiPeaksString: 0's and 1's representing the negative and positive peaks of the horizontal EOG signal
    :return: returns the eye movements count
    '''

    upwardSaccadeCount = vertPeaksString.count('0110')
    downwardSaccadeCount = vertPeaksString.count('1001')
    leftSaccadeCount = horiPeaksString.count('0110')
    rightSaccadeCount = horiPeaksString.count('1001')
    blinksCount = vertPeaksString.count('010')

    return upwardSaccadeCount, downwardSaccadeCount, leftSaccadeCount, rightSaccadeCount, blinksCount

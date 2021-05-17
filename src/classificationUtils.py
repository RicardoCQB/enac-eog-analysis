import numpy as np
from scipy import signal


def findPeaks(cwt, minPeakHeight, maxPeakHeight, minPeakDistance):
    '''
    This function uses the continuous wavelet transform of the signal to find the negative and positive peaks of the signal
    :param cwt: continuous wavelet transform of the EOG signal
    :param minPeakHeight: minimum coefficient value for the peak's height
    :param maxPeakHeight: maximum coefficient value for the peak's height
    :param minPeakDistance: minimum distance between same signal peaks for them to be detected
    :return: returns an array with the all the peaks ordered by their initial signal's position
    '''

    # Returns peaks' indexes and their properties in a dict
    # The peaks are detected in the module version of signal in order to find the negative peaks as well
    negativePeaks, propertiesN = signal.find_peaks(-cwt, height=[minPeakHeight, maxPeakHeight], distance=minPeakDistance)
    positivePeaks, propertiesP = signal.find_peaks(cwt, height=[minPeakHeight, maxPeakHeight], distance=minPeakDistance)

    allPeaks = np.hstack((negativePeaks, positivePeaks))

    allPeaks = np.sort(allPeaks)

    return allPeaks


def peaksToBinary(peaksArray, eogCWT):
    '''
    This function turns an array with the peaks of the eog CWT into an array of 0's and 1's
    The 0's represent negative peaks and the 1´s represent positive peaks
    :param peaksArray: array with the indexes of the peaks of the eogCWT
    :param eogCWT: eog signal array after the continuous wavelet transform
    :return: peaks binary array (array with the indexes of the peaks, the values of the peaks and binary code for negative or positive peaks).
    '''
    peaksBinary = np.zeros((3, len(peaksArray)))

    # Create array with same length as the number of peaks and transform peaks into 0 (negative peak) and 1 (positive peak)
    for i, peakV in enumerate(peaksArray):
        peaksBinary[0][i] = peakV
        peaksBinary[1][i] = eogCWT[peakV]
        if eogCWT[peakV] < 0:
            peaksBinary[2][i] = 0
        elif eogCWT[peakV] > 0:
            peaksBinary[2][i] = 1

    return peaksBinary


def peaksBinarySaccadeAnalysis(peaksBinary, jumpIntervalThreshold=500, saccadeLowerThreshold=500, saccadeUpperThreshold=6000):
    '''
    This function takes the array with the CWT peaks and tries to detect if the peaks represent a positive or negative saccade
    :param peaksBinary: peaks binary array (array with the indexes of the peaks, the values of the peaks and binary code for negative or positive peaks).
    :return: returns two lists, one with the start and end of the positve saccades and one with the negative saccades.
    '''
    positiveSaccadeStartEnd = []
    negativeSaccadeStartEnd = []

    peakInd = peaksBinary[0]
    peakBinary = peaksBinary[2]

    for i in range(0, len(peakInd) - 3):
        startInterval = peakInd[i+1] - peakInd[i]
        if peakBinary[i] == 0 and peakBinary[i+1] == 1 and startInterval <= jumpIntervalThreshold:
            positiveStart = peakInd[i]
            endInterval = peakInd[i+3] - peakInd[i+2]
            if peakBinary[i+2] == 1 and peakBinary[i+3] == 0 and endInterval <= jumpIntervalThreshold:
                positiveEnd = peakInd[i+3]
                saccadeInterval = peakInd[i+3] - peakInd[i]
                if saccadeLowerThreshold <= saccadeInterval <= saccadeUpperThreshold:
                    positiveSaccadeStartEnd.append([positiveStart, positiveEnd])

        elif peakBinary[i] == 1 and peakBinary[i+1] == 0 and startInterval <= jumpIntervalThreshold:
            negativeStart = peakInd[i]
            endInterval = peakInd[i+3] - peakInd[i+2]
            if peakBinary[i+2] == 0 and peakBinary[i+3] == 1 and endInterval <= jumpIntervalThreshold:
                negativeEnd = peakInd[i+3]
                saccadeInterval = peakInd[i + 3] - peakInd[i]
                if saccadeLowerThreshold <= saccadeInterval <= saccadeUpperThreshold:
                    negativeSaccadeStartEnd.append([negativeStart, negativeEnd])

    return positiveSaccadeStartEnd, negativeSaccadeStartEnd


def peaksBinarySaccadeAnalysisVersion2(peaksBinary, jumpIntervalThreshold=500, saccadeLowerThreshold=500, saccadeUpperThreshold=6000):
    positiveSaccadeStartEnd = []
    negativeSaccadeStartEnd = []

    peakInd = peaksBinary[0]
    peakBinary = peaksBinary[2]

    for i in range(0, len(peakInd) - 3):
        startInterval = peakInd[i + 1] - peakInd[i]
        if peakBinary[i] == 0 and peakBinary[i + 1] == 1 and startInterval <= jumpIntervalThreshold:
            positiveStart = peakInd[i]
            positiveEnd = peakInd[i + 3]
            positiveSaccadeStartEnd.append([positiveStart, positiveEnd])

        elif peakBinary[i] == 1 and peakBinary[i + 1] == 0 and startInterval <= jumpIntervalThreshold:
            negativeStart = peakInd[i]
            negativeEnd = peakInd[i + 3]
            negativeSaccadeStartEnd.append([negativeStart, negativeEnd])

    return positiveSaccadeStartEnd, negativeSaccadeStartEnd


def peaksBinaryToString(peaksBinary):
    '''
    Turns the array with the peaks, peak value and binary code for the negative and positive peaks and turns it into to a string
    :param peaksBinary: array with the binary code for the negative and positive peaks
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

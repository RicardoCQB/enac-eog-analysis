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
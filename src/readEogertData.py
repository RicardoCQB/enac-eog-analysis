'''
This part of code is dedicated to read the output data from the Eogert_offline algorithm.
This algorithm can be found on Github: https://github.com/bwrc/eogert

Reference to the article that describes this method:
    Toivanen, M., Pettersson, K., Lukander, K. (2015).
    A probabilistic real-time algorithm for detecting blinks, saccades, and fixations from EOG data.
    Journal of Eye Movement Research, 8(2):1,1-14.
'''

import databasePreparation
import scipy.io as sio


def readTmpResults(path):
    '''
    This function receives the path of a .mat matlab and returns it as a python dictionary
    :param path: path of the .mat matlab file
    :return: returns a python dictionary with the values of the .mat input file
    '''
    dictArray = {}
    sio.loadmat(path, dictArray)
    return dictArray


def getTmpResultsArrays(path):
    '''
    This function reads a very specific file that has the name tmpResults and is a result of eogerg algorithm
    :param path: path of the.mat matlab file 'tmpResults.mat'
    :return: returns the saccade and blinks metrics that the file contains
    '''
    tmpResultsDict = readTmpResults(path)

    saccadeStartTimestamps = tmpResultsDict['SAC_START']
    saccadeDurations = tmpResultsDict['SAC_DUR']

    blinkStartTimestamps = tmpResultsDict['BLI_START']
    blinkDurations = tmpResultsDict['BLI_DUR']

    saccadeProbs = tmpResultsDict['SAC_PROB']
    blinkPeaks = tmpResultsDict['BLI_PEAK']
    blinkProbs = tmpResultsDict['BLI_PROB']
    blink = tmpResultsDict['BLI_DMM']

    return saccadeStartTimestamps, saccadeDurations, blinkStartTimestamps, blinkDurations


saccadeStarts, saccadeDurations, blinkStarts, blinkDurations = getTmpResultsArrays('C:/Users/Ricardo/source/enac-eog-analysis/src/matlabFiles/tmpResults_RI02.mat')

    



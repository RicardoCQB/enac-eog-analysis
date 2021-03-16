''' This .py file is dedicated to functions that will be used to separate the useful sections of the signal's
edf file from the non useful sections. This separation will be made using the trigger labels available in the
 labels_triggers_*.csv'''

import numpy as np
import datetime
import scipy.io as sio

labelDict = {
    'CalibrationStart': 'calibration_EOG_C_start',
    'CalibrationEnd': 'calibration_EOG_C_end',

    'SemanticAcessStart': 'S_access',
    'AutobioAcessStart': 'A_access',
    'VisualImageStart': 'V_image',

    'SemanticVisualizationStart': 'S_visualization',
    'AutobioVisualizationStart': 'A_visualization',

    'SemanticDebriefingStart': 'S_debriefing',
    'AutobioDebriefingStart': 'A_debriefing',
    'VisualDebriefingStart': 'V_debriefing'
}

def getEogLabelIndexes(triggerCsv, labelStart, labelEnd):
    '''
    It returns the list of indexes that contain the desired label. It is useful when we want to select
    specific parts of the signal
    :param triggerCsv: array structure with the labels of the triggers and their datapoint index
    :param labelStart: String of the name of the section's starting label
    :param labelEnd: String of the name of the section's ending label
    :return: returns two lists with starting and ending index of the desired label
    If the label occurs more than one time, than there will be more than one index in the returning list.
    '''
    startIndexes = []
    endIndexes = []

    # Stores the labels' indexes that correspond to the start and end label in arrays.
    for triggerPoint, triggerLabel in zip(triggerCsv['latency'], triggerCsv['type']):
        if triggerLabel == labelStart:
            startIndexes.append(np.math.floor(triggerPoint))
        elif triggerLabel == labelEnd:
            endIndexes.append(np.math.floor(triggerPoint))

    if len(startIndexes) != len(endIndexes):
        raise Exception('The number of starting indexes of {} is different from {}. {} != {}'
                        .format(labelStart, labelEnd, len(startIndexes), len(endIndexes)))

    return startIndexes, endIndexes


def getEogCalibrationPart(signal, triggerCsv):
    '''
    Returns the part of the EOG signal that corresponds to the calibration
    :param signal: vertical or horizontal EOG signal array
    :param triggerCsv: array structure with the labels of the triggers and their datapoint index
    :return: signal part corresponding to the calibration
    '''
    calStartIndexes, calEndIndexes = getEogLabelIndexes(triggerCsv,
                                                        labelDict['CalibrationStart'],
                                                        labelDict['CalibrationEnd'])
    # First start element of the calibration
    calStart = calStartIndexes[0]
    # Last end element of the calibration
    calEnd = calEndIndexes[-1]
    # With the first start element and the last end element we can extract the entire calibration part
    if len(signal.shape) == 1: # 1D Numpy Array (Vertical and Horizontal EOG)
        calibrationPart = signal[calStart:calEnd]
    elif len(signal.shape) == 2: # 2D Numpy Array (4 electrodes EOG)
        calibrationPart = signal[:, calStart:calEnd]

    return calibrationPart


def getEogSeveralParts(signal, triggerCsv, labelStart, labelEnd):
    '''
    This function returns the indexes of the several parts start and end points
    Several parts such as the autobiographical, semantic and visual parts
    :param signal: vertical or horizontal EOG signal array
    :param triggerCsv: array structure with the labels of the triggers and their datapoint index
    :param labelStart: String of the name of the section's starting label
    :param labelEnd: String of the name of the section's ending label
    :return: returns the signal parts corresponding do the chosen part
    '''
    startIndexes, endIndexes = getEogLabelIndexes(triggerCsv, labelStart, labelEnd)
    eogSignalParts = []

    for startIndex, endIndex in zip(startIndexes, endIndexes):
        if len(signal.shape) == 1:
            eogSignalParts.append(signal[startIndex:endIndex])
        elif len(signal.shape) == 2:
            eogSignalParts.append(signal[:, startIndex:endIndex])

    return eogSignalParts


def getEogSAVParts(signal, triggerCsv):
    '''
    This functions uses the getEogSeveralParts function to get simultaneously
    :param signal: vertical or horizontal EOG signal array
    :param triggerCsv: array structure with the labels of the triggers and their datapoint index
    :return: returns a list with three items corresponding to arrays of the starting and ending indexes
    of the Semantic, autobiographical and visual parts
    '''
    semanticParts = getEogSeveralParts(signal, triggerCsv,
                                       labelDict['SemanticAcessStart'],
                                       labelDict['SemanticDebriefingStart'])

    autobioParts = getEogSeveralParts(signal, triggerCsv,
                                       labelDict['AutobioAcessStart'],
                                       labelDict['AutobioDebriefingStart'])

    visualTaskParts = getEogSeveralParts(signal, triggerCsv,
                                         labelDict['VisualImageStart'],
                                         labelDict['VisualDebriefingStart'])

    return semanticParts, autobioParts, visualTaskParts


def getEogAnalysisSection(signal, triggerCsv):
    '''
    This function uses getEogSAVParts and getCalibrationParts to join every important part of the signal for analysis
    :param signal: vertical or horizontal EOG signal array
    :param triggerCsv: array structure with the labels of the triggers and their datapoint index
    :return: returns a list with three items corresponding to arrays of the starting and ending indexes
    of the Semantic, autobiographical and visual parts and the starting and ending point of the calibration phase
    '''
    calibrationPart = getEogCalibrationPart(signal, triggerCsv)

    semanticParts, autobioParts, visualTaskParts = getEogSAVParts(signal, triggerCsv)

    return calibrationPart, semanticParts, autobioParts, visualTaskParts


def datapointToSeconds(datapoint, sampleRateFreq):
    '''
    Transforms the given datapoint into seconds
    :param datapoint: datapoint or index
    :param sampleRateFreq: sample frequency which the signal was recorded
    :return: datapoint in seconds
    '''
    return datapoint / sampleRateFreq


def secondsToHMS(seconds):
    '''
    Turns seconds into a string of hours, minutes and seconds
    :param seconds: number of seconds
    :return: string of hours, minutes and seconds
    '''
    str(datetime.timedelta(seconds=seconds))


def arrayToMat(numpyArray, filename):
    '''
    This function turns an 1d numpy array from python into a list and saves it into a matlab  .mat file
    so it can be used in matlab scripts
    :param numpyArray: numpy array of 1 dimensions (n,)
    :param filename: string that contains the name of the .mat file
    :return: null
    '''
    # Creates the x data that represents the indexes of the signal and turns the signal into a list
    x = list(range(0, len(numpyArray)))
    y = numpyArray.tolist()

    # Creates a dictionary with the indexes and the values of the signal
    dictArray = {'x': x, 'y': y}
    sio.savemat('{}.mat'.format(filename), dictArray)


def matToNumpyArray(filename):
    '''
    This function reads the filename.mat file and turns it into a 1d numpy array
    :param filename: string with the filename of the file (without the '.mat')
    :return: returns a numpy array of the read .mat file
    '''

    dictArray = {}
    sio.loadmat('{}.mat'.format(filename), dictArray)

    array = np.array(dictArray['y'])
    return array

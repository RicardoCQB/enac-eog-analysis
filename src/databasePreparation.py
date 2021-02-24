''' This .py file is dedicated to functions that will be used to separate the useful sections of the signal's
edf file from the non useful sections. This separation will be made using the trigger labels available in the
 labels_triggers_*.csv'''

import pyedflib
import numpy as np

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
    :param triggerCsv: Pandas DataFrame with the trigger labels data
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
    :param signal: EOG vertical or horizontal signal
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
    calibrationPart = signal[:,calStart:calEnd] # calibrationPart = signal[calStart:CalEnd]

    return calibrationPart

def getEogSeveralParts(signal, triggerCsv, labelStart, labelEnd):
    startIndexes, endIndexes = getEogLabelIndexes(triggerCsv, labelStart, labelEnd)
    eogSignalParts = []

    for startIndex, endIndex in zip(startIndexes, endIndexes):
        eogSignalParts.append(signal[:, startIndex, endIndex])
        #eogSignalParts.append(signal[startIndex:endIndex])

    return eogSignalParts

def getEogSAVParts(signal, triggerCsv):
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
    calibrationPart = getEogCalibrationPart(signal, triggerCsv)

    semanticParts, autobioParts, visualTaskParts = getEogSAVParts(signal, triggerCsv)

    return calibrationPart, semanticParts, autobioParts, visualTaskParts

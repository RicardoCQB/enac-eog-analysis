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
    'AutiobioVisualizationStart': 'A_visualization',

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
            startIndexes.append(triggerPoint)
        elif triggerLabel == labelEnd:
            endIndexes.append(triggerPoint)

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
    calStart = calStartIndexes[0]
    calEnd = calEndIndexes[-1]
    calibrationPart = signal[calStart:calEnd]

    return calibrationPart

def getEogSAVParts(signal, triggerCsv):

    semanticStartIndexes, semanticEndIndexes = getEogLabelIndexes(triggerCsv,
                                                                  labelDict['SemanticAcessStart'],
                                                                  labelDict['SemanticDebriefingStart'])

    



def getEogAnalysisSection(signal, triggerCsv):
    calibrationPart = getEogCalibrationPart(signal, triggerCsv)







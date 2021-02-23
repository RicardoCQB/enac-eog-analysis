''' This .py file is dedicated to functions that will be used to separate the useful sections of the signal's
edf file from the non useful sections. This separation will be made using the trigger labels available in the
 labels_triggers_*.csv'''

import pyedflib
import numpy as np

# Function that reads from the signal and finds certain section
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
    for triggerPoint, triggerLabel in zip(triggerCsv['latency'], triggerCsv['type']):
        if triggerLabel == labelStart:
            startIndexes.append(triggerPoint)
        elif triggerLabel == labelEnd:
            endIndexes.append(triggerPoint)

    return startIndexes, endIndexes

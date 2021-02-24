import numpy as np
import pyedflib
import pandas as pd


def readEog(fileName):
    # Reading the signals from the EDF file
    try:
        f = pyedflib.EdfReader(fileName)
    except FileNotFoundError as e:
        print(e)
        print('\n The {} file was not found.'.format(fileName))

    # numSignals = f.signals_in_file

    # These are the numbers of the channels that interest us
    channelsOfInterest = [256, 257, 258, 259]
    numEyeChannels = len(channelsOfInterest)

    # signal_labels = f.getSignalLabels()
    # print(signal_labels)

    # Creation of a zero array the correct dimensions.
    eyesData = np.zeros((numEyeChannels, f.getNSamples()[0]))

    for i, channel in enumerate(channelsOfInterest):
        eyesData[i, :] = f.readSignal(channel)

    f.close()

    return eyesData


def readCsvTriggerLabels(fileName):
    try:
        triggerCsv = pd.read_csv(fileName)
    except FileNotFoundError as e:
        print(e)
        print('\n The .csv file was not found, therefore the labels of the triggers will not be shown.')

    return triggerCsv
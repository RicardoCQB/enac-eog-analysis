''' This module is dedicated to visualization and plotting functions needed for the project.'''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def plotEogElectrodesSignal(signal, start=0, end=1000, labels=[],
                  xAxisLabel='Datapoint',
                  yAxisLabel='Amplitude (microVolts)'):
    '''
    Function for plotting the EOG with any number of electrodes read from EDF file using the method in the reading section
    in the jupyter notebook.
    :param signal: signal to be plotted
    :param start: index of the start of the plot
    :param end: indes of the end of the plot
    :param labels: labels for the various signals that could be plotted
    :param xAxisLabel: label of the x axis
    :param yAxisLabel: label of the y axis
    :return:
    '''
    plt.figure(figsize=(20, 5))
    signal = signal[:, start:end]
    signal = np.swapaxes(signal,0,1)
    plt.plot(signal)
    plt.xlabel(xAxisLabel)
    plt.ylabel(yAxisLabel)
    plt.legend(labels)
    plt.show()

def plotVertHorEOG(verticalEOG, horizontalEOG, start, end, mode='both'):
    '''
    Function for plotting the vertical and horizontal EOG signals, these signals are the ones that will be used to
    detect and classify saccades.
    :param verticalEOG: vertical signal of the EOG, that means the up electrode values minus the down electrode valus
    :param horizontalEOG: horizontal signal of the EOG, left electrode signal values minus the right electrode signal values
    :param start: integer index of the start of the plot
    :param end: integer index of the end of the plot
    :param mode: the mode chooses if it is plotted the vertical EOG or the horizontal EOG or both
    Therefore, there are three modes: 'both', 'vertical' and 'horizontal'
    :return:
    '''
    verticalEOG = verticalEOG[start:end]
    horizontalEOG = horizontalEOG[start:end]

    plt.figure(figsize=(40, 10))
    if mode == 'both':
        plt.plot(verticalEOG, color='cyan')
        plt.plot(horizontalEOG, color='magenta')
        labels = ['Vertical EOG (Up - Down)', 'Horizontal EOG (Left - Right)']
    if mode == 'vertical':
        plt.plot(verticalEOG, color='cyan')
        labels = ['Vertical EOG (Up - Down)']
    if mode == 'horizontal':
        plt.plot(horizontalEOG, color='magenta')
        labels = ['Horizontal EOG (Left - Right)']

    plt.xlabel('Datapoint')
    plt.ylabel('Amplitude (microVolts)')
    plt.legend(labels)

    # Reading the .csv file that contains the triggers for this .edf signal file

    try:
        triggerCsv = pd.read_csv('C:/Users/Ricardo\source/enac-eog-analysis/data/EOG_EyeLink/RI02/labels_triggers_603.csv')

        for triggerPoint, triggerLabel in zip(triggerCsv['latency'], triggerCsv['type']):
            if triggerPoint >= start and triggerPoint <= end:
                plt.axvline(x=triggerPoint-start, color='black')
                plt.text(triggerPoint-start, 0, triggerLabel, rotation='vertical')
    except FileNotFoundError as e:
        print(e)
        print('\n The .csv file was not found, therefore the labels of the triggers will not be shown.')

    plt.show()





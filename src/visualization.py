''' This module is dedicated to visualization and plotting functions needed for the project.'''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def plotEogElectrodesSignal(signal, start=None, end=None, labels=[],
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
    plt.figure(figsize=(20, 5), dpi=90) #700,20
    if start and end is not None:
        signal = signal[:, start:end]
    signal = np.swapaxes(signal,0,1)
    plt.plot(signal)
    plt.xlabel(xAxisLabel)
    plt.ylabel(yAxisLabel)
    plt.ylim((-500,500))
    plt.legend(labels)


def plotVertHorEOG(verticalEOG, horizontalEOG, start=None, end=None, mode='both', triggerCsv=None,
                   triggerStart=None, triggerEnd=None):
    '''
    Function for plotting the vertical and horizontal EOG signals, these signals are the ones that will be used to
    detect and classify saccades.
    :param verticalEOG: vertical signal of the EOG, that means the up electrode values minus the down electrode valus
    :param horizontalEOG: horizontal signal of the EOG, left electrode signal values minus the right electrode signal values
    :param start: integer index of the start of the plot
    :param end: integer index of the end of the plot
    :param mode: the mode chooses if it is plotted the vertical EOG or the horizontal EOG or both
    Therefore, there are three modes: 'both', 'vertical' and 'horizontal'
    :param labelsCsvFile: the name of the file that contains the names of the triggers
    :return:
    '''
    if start and end is not None:
        verticalEOG = verticalEOG[start:end]
        horizontalEOG = horizontalEOG[start:end]

    plt.figure(figsize=(20, 5), dpi=90)
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
    plt.ylim((-500,500))
    plt.legend(labels)

    # If the labels csv is being used, then the labels are stamped in the plot
    if triggerStart and triggerEnd and triggerCsv is not None:
        for triggerPoint, triggerLabel in zip(triggerCsv['latency'], triggerCsv['type']):
            if triggerStart <= triggerPoint <= triggerEnd:
                plt.axvline(x=triggerPoint-triggerStart, color='black')
                plt.text(triggerPoint-triggerStart, 0, triggerLabel, rotation='vertical')


def sampleToTimePlot(signal, frequencySample):
    '''
    This function plots the signal in timestamps instead of samples
    :param signal: signal values
    :param frequencySample: frequency sample that the signal was sampled at
    :return:
    '''
    plt.plot(range(len(signal)) / frequencySample, signal)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude (microVolts)')


def plotSaccadeSpanInSignal(signal, positiveSaccadeStartEnd, negativeSaccadeStartEnd):
    plt.figure(figsize=(20, 5), dpi=90)

    for positiveSaccade, negativeSaccade in zip(positiveSaccadeStartEnd, negativeSaccadeStartEnd):
        plt.axvspan(positiveSaccade[0], positiveSaccade[1], color='blue', alpha=0.2)
        plt.axvspan(negativeSaccade[0], positiveSaccade[1], color='red', alpha=0.2)

    plt.plot(signal)

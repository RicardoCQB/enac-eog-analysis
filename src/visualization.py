''' This module is dedicated to visualization and plotting functions needed for the project.'''

import numpy as np
import matplotlib.pyplot as plt


def plotEogElectrodesSignal(signal, start=0, end=1000, labels=[],
                  xAxisLabel='Datapoint',
                  yAxisLabel='Amplitude (microVolts)'):
    '''
    Method for plotting the EOG with any number of electrodes read from EDF file using the method in the reading section
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
    verticalEOG = verticalEOG[start:end]
    horizontalEOG = horizontalEOG[start:end]

    plt.figure(figsize=(50, 5))
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
    plt.show()





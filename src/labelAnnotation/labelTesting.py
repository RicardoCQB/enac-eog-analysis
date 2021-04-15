import os
import sys
sys.path.append('..')

import pyedflib
import numpy as np
from matplotlib.widgets import Slider, Button
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd
import pywt
import readFiles
import databasePreparation
import preProcessing
import readEogertData
import math
from scipy import ndimage, misc
import json
import string
import neurokit2 as nk
import csv


# Reading the signals from the EDF file
edfFileName = 'C:/Users/Ricardo\source/enac-eog-analysis/data/EOG_EyeLink/RI02/Testdata0602.edf'
eyesData = readFiles.readEog(edfFileName)

freqSample = 2048

# Reading the trigger labels for the different parts of the experiment
# labelsCsvFile = 'C:/Users/Ricardo\source/enac-eog-analysis/data/EOG_EyeLink/RI02/labels_triggers_602.csv'

# triggerCsv = readFiles.readCsvTriggerLabels(labelsCsvFile)

# Pre-processing: noise removal using median filter
verticalEOG4, horizontalEOG4 = preProcessing.electrodesToVertHori(eyesData, 0, 1, 2, 3)

#verticalEogDenoised4 = ndimage.median_filter(verticalEOG4, size = 100)
#horizontalEogDenoised4 = ndimage.median_filter(horizontalEOG4, size = 100)
verticalEogDenoised4 = verticalEOG4
horizontalEogDenoised4 = horizontalEOG4

# Labeling the blinks
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.3)

t = np.arange(0, len(verticalEogDenoised4), 1)
s = verticalEogDenoised4
l, = plt.plot(t,s)
plt.axis([0, len(verticalEogDenoised4), -800, 800])

# Slider
axcolor = 'lightgoldenrodyellow'
axpos = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor=axcolor)
spos = Slider(axpos, 'Scroll', 0, len(verticalEogDenoised4))

startInds = []
endInds = []
areaSpan = []

# Buttons functions definition
def labelButtonClick(event):
    x = plt.ginput(2)
    if None not in x:
        startInd = np.round(x[0][0])
        endInd = np.round(x[1][0])
        if startInd < endInd:
            print('Start: {}\nEnd: {}'.format(startInd, endInd))
            areaSpan.append(ax.axvspan(startInd, endInd, color='red', alpha=0.4))
            startInds.append(startInd)
            endInds.append(endInd)

def unlabelButtonClick(event):
    print('Removed start and end index: {}, {}'.format(startInds[-1], endInds[-1]))
    if startInds:
        startInds.pop()
    if endInds:
        endInds.pop()
    if areaSpan:
        areaSpan[-1].remove()
        areaSpan.pop()

def update(val):
    pos = spos.val
    ax.axis([pos,pos+20000,-800,800])
    fig.canvas.draw_idle()

spos.on_changed(update)

axLabelButton = plt.axes([0.6, 0.15, 0.1, 0.075])
axUnlabelButton = plt.axes([0.72, 0.15, 0.1, 0.075])

labelButton = Button(axLabelButton, 'Label')
labelButton.on_clicked(labelButtonClick)

unlabelButton = Button(axUnlabelButton, 'Unlabel')
unlabelButton.on_clicked(unlabelButtonClick)

plt.show()

def labelingToCsv(filename, startInds, endInds):
    with open(filename, 'w', newline='') as f:
        write = csv.writer(f, delimiter=';')
        fields = ['start', 'end']
        write.writerow(fields)
        for startInd, endInd in zip(startInds, endInds):
            write.writerow([startInd, endInd])


labelingToCsv('blinkLabels_Test.csv', startInds, endInds)


def readingLabelCsv(filename):
    with open(filename, 'r', newline='') as f:
        read = csv.reader(f, delimiter=';')
        header = read.



def readCsvTriggerLabels(fileName):
    try:
        triggerCsv = pd.read_csv(fileName)
    except FileNotFoundError as e:
        print(e)
        print('\n The .csv file was not found, therefore the labels of the triggers will not be shown.')

    return triggerCsv
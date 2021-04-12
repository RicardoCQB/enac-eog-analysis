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


# Reading the signals from the EDF file

edfFileName = 'C:/Users/Ricardo\source/enac-eog-analysis/data/EOG_EyeLink/RI02/Testdata0602.edf'
eyesData = readFiles.readEog(edfFileName)

freqSample = 2048

# Reading the trigger labels for the different parts of the experiment

labelsCsvFile = 'C:/Users/Ricardo\source/enac-eog-analysis/data/EOG_EyeLink/RI02/labels_triggers_602.csv'

triggerCsv = readFiles.readCsvTriggerLabels(labelsCsvFile)

# Pre-processing: noise removal using median filter
verticalEOG4, horizontalEOG4 = preProcessing.electrodesToVertHori(eyesData, 0, 1, 2, 3)

#verticalEogDenoised4 = ndimage.median_filter(verticalEOG4, size = 100)
#horizontalEogDenoised4 = ndimage.median_filter(horizontalEOG4, size = 100)
verticalEogDenoised4 = verticalEOG4
horizontalEogDenoised4 = horizontalEOG4

# Labeling the blinks

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.45)

t = np.arange(0, len(verticalEogDenoised4), 1)
s = verticalEogDenoised4
l, = plt.plot(t,s)
plt.axis([0, len(verticalEogDenoised4), -700, 700])

# Slider
axcolor = 'lightgoldenrodyellow'
axpos = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor=axcolor)

spos = Slider(axpos, 'Pos', 0, len(verticalEogDenoised4))

startInds = []
endInds = []

# Buttons
def labelButtonClick(event):
    x = plt.ginput(2)
    if None not in x:
        print(x[0][0])
        print(x[1][0])
        startInds.append(x[0][0])
        endInds.append(x[1][0])

def unlabelButtonClick(event):
    print(startInds)
    print(endInds)
    if startInds:
        startInds.pop()
    if endInds:
        endInds.pop()

#
# def onclick(event, coords):
#     click = event.xdata, event.ydata
#     if None not in click:  # clicking outside the plot area produces a coordinate of None, so we filter those out.
#         print('x = {}, y = {}'.format(*click))
#         coords.append(click)



def update(val):
    pos = spos.val
    ax.axis([pos,pos+10000,-700,700])
    fig.canvas.draw_idle()

spos.on_changed(update)


axLabelButton = plt.axes([0.7, 0.05, 0.1, 0.075])
axUnlabelButton = plt.axes([0.81, 0.05, 0.1, 0.075])

labelButton = Button(axLabelButton, 'Label')
labelButton.on_clicked(labelButtonClick)

unlabelButton = Button(axUnlabelButton, 'Unlabel')
unlabelButton.on_clicked(unlabelButtonClick)

plt.show()
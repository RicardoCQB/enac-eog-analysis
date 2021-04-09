import os
import sys
sys.path.append('..')

import pyedflib
import numpy as np
from matplotlib.widgets import Slider
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
plt.subplots_adjust(bottom=0.25)

t = np.arange(0, len(verticalEogDenoised4), 1)
s = verticalEogDenoised4
l, = plt.plot(t,s)
plt.axis([0, len(verticalEogDenoised4), -500, 500])

axcolor = 'lightgoldenrodyellow'
axpos = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor=axcolor)

spos = Slider(axpos, 'Pos', 0, len(verticalEogDenoised4))

def update(val):
    pos = spos.val
    ax.axis([pos,pos+10000,-600,600])
    fig.canvas.draw_idle()

spos.on_changed(update)

plt.show()
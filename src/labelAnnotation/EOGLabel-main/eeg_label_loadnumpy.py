import os
import sys
sys.path.append('../..')

import databasePreparation

labelArray = databasePreparation.loadNumpyArray('C:\Users\Ricardo\source\enac-eog-analysis\src\labelAnnotation\EOGLabel-main\RI02_labeling\\bloc7_saccadeTimeStamp.npy')

print(labelArray)

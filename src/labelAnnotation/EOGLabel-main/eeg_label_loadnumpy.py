import os
import sys
sys.path.append('../..')

import databasePreparation

labelArray = databasePreparation.loadNumpyArray('saccadeTimeStamp.npy')

print(labelArray)

import unittest
import databasePreparation
import readFiles

class TestDataPreparation(unittest.TestCase):

    def setUp(self):
        self.signalFileName = 'C:/Users/Ricardo\source/enac-eog-analysis/data/EOG_EyeLink/RI02/Testdata0602.edf'
        self.labelsCsvFileName = 'C:/Users/Ricardo\source/enac-eog-analysis/data/EOG_EyeLink/RI02/labels_triggers_602.csv'
        self.signal = readFiles.readEog(self.signalFileName)
        self.triggerCsv = readFiles.readCsvTriggerLabels(self.labelsCsvFileName)

    def tearDown(self):
        pass

    def test_getEogLabelIndexes(self):
        resultStartIndexes, resultEndIndexes = databasePreparation.getEogLabelIndexes(self.triggerCsv, 'calibration_EOG_C_start','calibration_EOG_C_end')

        startIndexes = [116396, 120906, 125415, 129924, 134433, 138943, 143452, 147961, 152471]
        endIndexes = [118443, 122952, 127461, 131970, 136480, 140989, 145498, 150007, 154517]

        self.assertEqual(resultStartIndexes, startIndexes)
        self.assertEqual(resultEndIndexes, endIndexes)

    def test_getEogCalibrationPart(self):
        calibrationPart = databasePreparation.getEogCalibrationPart(self.signal, self.triggerCsv)
        self.assertEqual(calibrationPart.shape, (4, 38121))

    def test_getEogSeveralParts(self):
        semanticParts = databasePreparation.getEogSeveralParts(self.signal, self.triggerCsv,
                                           databasePreparation.labelDict['SemanticAcessStart'],
                                           databasePreparation.labelDict['SemanticDebriefingStart'])
        self.assertEqual(semanticParts[0].shape, (4, 27154))

    def test_getEogSAVParts(self):
        semanticParts, autobioParts, visualTaskParts = databasePreparation.getEogSAVParts(self.signal, self.triggerCsv)
        print(len(semanticParts))


if __name__ == '__main__':
    unittest.main()

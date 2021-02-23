import unittest
import databasePreparation
import pandas as pd

class TestDataPreparation(unittest.TestCase):

    def setUp(self):
        self.labelsCsvFile = 'C:/Users/Ricardo\source/enac-eog-analysis/data/EOG_EyeLink/RI02/labels_triggers_602.csv'
        try:
            self.triggerCsv = pd.read_csv(self.labelsCsvFile)
        except FileNotFoundError as e:
            print(e)
            print('\n The .csv file was not found, therefore the labels of the triggers will not be shown.')

    def tearDown(self):
        pass

    def test_getEogSection(self):
        resultStartIndexes, resultEndIndexes = databasePreparation.getEogSection(self.triggerCsv, 'calibration_EOG_C_start','calibration_EOG_C_end')
        #print(resultStartIndexes, resultEndIndexes)

        startIndexes = [116396.0, 120906.0, 125415.0, 129924.0, 134433.0, 138943.0, 143452.0, 147961.0, 152471.0]
        endIndexes = [118443.0, 122952.0, 127461.0, 131970.0, 136480.0, 140989.0, 145498.0, 150007.0, 154517.0]
        self.assertEqual(resultStartIndexes, startIndexes)
        self.assertEqual(resultEndIndexes, endIndexes)

if __name__ == '__main__':
    unittest.main()

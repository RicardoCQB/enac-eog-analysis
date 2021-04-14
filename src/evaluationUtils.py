'''This python file has some functions that help to evaluate the developed algorithms performance.'''

def countCorrectDetected(detected, groundTruth):
    '''
    Function to count the number of correct labels detected
    :param detected: list of indexes with the detected movements by an algorithm
    :param groundTruth: list of pairs of indexes with the ground truth labeling for a specific movement start and end index
    :return: number of correctly detected movements according to the labeling
    '''
    numCorrectDetected = 0
    for detectedInd in detected:
        for i, gtLabel in enumerate(groundTruth):
            if gtLabel[0] <= detectedInd <= gtLabel[1]:
                numCorrectDetected = numCorrectDetected + 1
                groundTruth.pop(i)

    return numCorrectDetected


def calculatePrecision(numCorrectDetected, numDetected):
    '''
    Calculates precision of the processing
    :param numCorrectDetected: number of correctly detected movements by an algorithm
    :param numDetected: number of movements detected by an algorithm
    :return: precision value of the detection
    '''
    precision = numCorrectDetected / numDetected

    return precision


def calculateRecall(numCorrectDetected, numGroundTruth):
    '''
    Calculates the recall of the processing
    :param numCorrectDetected: number of correctly detected movements by an algorithm
    :param numGroundTruth: number of movements that were manually labeled
    :return: recall value of the detection
    '''
    recall = numCorrectDetected / numGroundTruth

    return recall

'''This python file has some functions that help to evaluate the developed algorithms performance.'''
import numpy as np

import databasePreparation

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


def saccadeEvaluation(saccadeStartEnd, direction, groundTruth):
    correctSaccades = []
    wrongSaccades = []

    for i, saccade in enumerate(saccadeStartEnd):
        saccadeDuration = saccade[1] - saccade[0]
        saccadeMiddlePoint = saccade[0] + np.round(saccadeDuration/2)
        for j, saccadeGT in enumerate(groundTruth):
            if saccadeGT[0] <= saccadeMiddlePoint <= saccadeGT[1] and saccadeGT[3].find(direction) != -1:
                correctSaccades.append(saccadeGT)
                groundTruth.pop(j)
            else:
                wrongSaccades.append(saccadeGT)
                groundTruth.append(j)

    return correctSaccades, wrongSaccades

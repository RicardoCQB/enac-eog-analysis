'''This python file has some functions that help to evaluate the developed algorithms performance.'''
import numpy as np
import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt

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
    '''
    This function takes a list with the start and end indexes of a type of saccade, for example an upwards saccade.
    And compares this list with the groundtruth labels made by hand.
    :param saccadeStartEnd: list of list compromised of start and end index [ [start, end] ... ]
    :param direction: string with the direction of the saccade, e.g: "up"
    :param groundTruth: list with the saccade labeling: [ [start end center "direction" ] ... ]
    :return: it returns a list of the correctly guessed and wrongly guessed saccades
    '''
    correctSaccades = []
    wrongSaccades = []

    for i, saccade in enumerate(saccadeStartEnd):
        saccadeDuration = saccade[1] - saccade[0]
        saccadeMiddlePoint = saccade[0] + np.round(saccadeDuration / 2)
        for j, saccadeGT in enumerate(groundTruth):
            saccadeStartGT = int(float(saccadeGT[0]))
            saccadeEndGT = int(float(saccadeGT[1]))
            if saccadeStartGT <= saccadeMiddlePoint <= saccadeEndGT and saccadeGT[3].find(direction) != -1:
                correctSaccades.append(saccadeGT)

    return correctSaccades, wrongSaccades


def saccadeConfusion(allDirSaccadeStartEnd, groundTruth):
    '''
    This function analyses the saccades that were detected by the algorithm and compares them to the groundTruth.
    :param allDirSaccadeStartEnd: this a list that should contain the up, down, left and right list of saccades start and end
    :param groundTruth: this ground truth is the saccade output of the labeling tool made by Guillaume that is present the file
    eeg_label
    :return: for every direction of a saccade it returns a list of its true positive, false negative and false positive saccades.
    '''
    upSaccadeStartEnd = allDirSaccadeStartEnd[0]
    downSaccadeStartEnd = allDirSaccadeStartEnd[1]
    leftSaccadeStartEnd = allDirSaccadeStartEnd[2]
    rightSaccadeStartEnd = allDirSaccadeStartEnd[3]

    upSaccadeTP = []
    upSaccadeFN = []
    upSaccadeFP = []

    downSaccadeTP = []
    downSaccadeFN = []
    downSaccadeFP = []

    leftSaccadeTP = []
    leftSaccadeFN = []
    leftSaccadeFP = []

    rightSaccadeTP = []
    rightSaccadeFN = []
    rightSaccadeFP = []

    # The predicted saccade was not found yet
    found = False

    # For the Up Saccades
    for i, upSaccade in enumerate(upSaccadeStartEnd):
        saccadeDuration = upSaccade[1] - upSaccade[0]
        saccadeMiddlePoint = upSaccade[0] + np.round(saccadeDuration / 2)
        for j, saccadeGT in enumerate(groundTruth):
            saccadeStartGT = int(float(saccadeGT[0]))
            saccadeEndGT = int(float(saccadeGT[1]))
            if saccadeStartGT <= saccadeMiddlePoint <= saccadeEndGT and saccadeGT[3].find('up') != -1:
                upSaccadeTP.append(upSaccade)
                found = True
            if saccadeStartGT <= saccadeMiddlePoint <= saccadeEndGT and saccadeGT[3].find('down') != -1:
                upSaccadeFN.append(upSaccade)
                found = True
        if found:
            # Reset the found flag
            found = False
        elif not found:
            # Add the not found saccade fo the False Positives List
            upSaccadeFP.append(upSaccade)

    # For the down Saccades
    for i, downSaccade in enumerate(downSaccadeStartEnd):
        saccadeDuration = downSaccade[1] - downSaccade[0]
        saccadeMiddlePoint = downSaccade[0] + np.round(saccadeDuration / 2)
        for j, saccadeGT in enumerate(groundTruth):
            saccadeStartGT = int(float(saccadeGT[0]))
            saccadeEndGT = int(float(saccadeGT[1]))
            if saccadeStartGT <= saccadeMiddlePoint <= saccadeEndGT and saccadeGT[3].find('down') != -1:
                downSaccadeTP.append(downSaccade)
                found = True
            if saccadeStartGT <= saccadeMiddlePoint <= saccadeEndGT and saccadeGT[3].find('up') != -1:
                downSaccadeFN.append(downSaccade)
                found = True
        if found:
            # Reset the found flag
            found = False
        elif not found:
            # Add the not found saccade fo the False Positives List
            downSaccadeFP.append(downSaccade)

    # For the left Saccades
    for i, leftSaccade in enumerate(leftSaccadeStartEnd):
        saccadeDuration = leftSaccade[1] - leftSaccade[0]
        saccadeMiddlePoint = leftSaccade[0] + np.round(saccadeDuration / 2)
        for j, saccadeGT in enumerate(groundTruth):
            saccadeStartGT = int(float(saccadeGT[0]))
            saccadeEndGT = int(float(saccadeGT[1]))
            if saccadeStartGT <= saccadeMiddlePoint <= saccadeEndGT and saccadeGT[3].find('left') != -1:
                leftSaccadeTP.append(leftSaccade)
                found = True
            if saccadeStartGT <= saccadeMiddlePoint <= saccadeEndGT and saccadeGT[3].find('right') != -1:
                leftSaccadeFN.append(leftSaccade)
                found = True
        if found:
            # Reset the found flag
            found = False
        elif not found:
            # Add the not found saccade fo the False Positives List
            leftSaccadeFP.append(leftSaccade)

    # For the right Saccades
    for i, rightSaccade in enumerate(rightSaccadeStartEnd):
        saccadeDuration = rightSaccade[1] - rightSaccade[0]
        saccadeMiddlePoint = rightSaccade[0] + np.round(saccadeDuration / 2)
        for j, saccadeGT in enumerate(groundTruth):
            saccadeStartGT = int(float(saccadeGT[0]))
            saccadeEndGT = int(float(saccadeGT[1]))
            if saccadeStartGT <= saccadeMiddlePoint <= saccadeEndGT and saccadeGT[3].find('right') != -1:
                rightSaccadeTP.append(rightSaccade)
                found = True
            if saccadeStartGT <= saccadeMiddlePoint <= saccadeEndGT and saccadeGT[3].find('left') != -1:
                rightSaccadeFN.append(rightSaccade)
                found = True
        if found:
            # Reset the found flag
            found = False
        elif not found:
            # Add the not found saccade fo the False Positives List
            rightSaccadeFP.append(rightSaccade)

    return [upSaccadeTP, upSaccadeFN, upSaccadeFP, downSaccadeTP, downSaccadeFN, downSaccadeFP,
            leftSaccadeTP, leftSaccadeFN, leftSaccadeFP, rightSaccadeTP, rightSaccadeFN, rightSaccadeFP]


def confusionMatrix(allDirSaccadeStartEnd, groundTruth):
    '''
    This function uses the true positives, false negatives and false positive saccades of every direction and calculates
    the scores of the algorithm and plots a confusion matrix for horizontal and vertical saccades.
    :param allDirSaccadeStartEnd: this a list that should contain the up, down, left and right list of saccades start and end
    :param groundTruth: this ground truth is the saccade output of the labeling tool made by Guillaume that is present the file
    eeg_label
    :return: nothing
    '''
    [upSaccadeTP, upSaccadeFN, upSaccadeFP, downSaccadeTP, downSaccadeFN, downSaccadeFP, leftSaccadeTP,
     leftSaccadeFN, leftSaccadeFP, rightSaccadeTP, rightSaccadeFN, rightSaccadeFP] = saccadeConfusion(
        allDirSaccadeStartEnd, groundTruth)

    upTP = len(upSaccadeTP)
    upFN = len(upSaccadeFN)
    upFP = len(upSaccadeFP)

    downTP = len(downSaccadeTP)
    downFN = len(downSaccadeFN)
    downFP = len(downSaccadeFP)

    leftTP = len(leftSaccadeTP)
    leftFN = len(leftSaccadeFN)
    leftFP = len(leftSaccadeFP)

    rightTP = len(rightSaccadeTP)
    rightFN = len(rightSaccadeFN)
    rightFP = len(rightSaccadeFP)

    upDownConfMatrix = [[upTP, upFN],
                        [downFN, downTP]]
    upDownConfMatrixDF = pd.DataFrame(upDownConfMatrix, range(2), range(2))
    plt.figure(figsize=(10, 7))
    sn.set(font_scale=1.4)  # for label size
    xAxisLabels = ['Up GT', 'Down GT']
    yAxisLabels = ['Up CWT', 'Down CWT']
    sn.heatmap(upDownConfMatrixDF, xticklabels=xAxisLabels, yticklabels=yAxisLabels, annot=True, fmt='d', annot_kws={"size": 16})  # font size
    plt.show()

    leftRightConfMatrix = [[leftTP, leftFN],
                           [rightFN, rightTP]]
    leftRightConfMatrixDF = pd.DataFrame(leftRightConfMatrix, range(2), range(2))
    plt.figure(figsize=(10, 7))
    sn.set(font_scale=1.4)  # for label size
    xAxisLabels = ['Left GT', 'Right GT']
    yAxisLabels = ['Left CWT', 'Right CWT']
    sn.heatmap(leftRightConfMatrixDF, xticklabels=xAxisLabels, yticklabels=yAxisLabels, annot=True, fmt='d', annot_kws={"size": 16})  # font size

    plt.show()

    totalTP = upTP + downTP + leftTP + rightTP
    totalFP = upFP + downFP + leftFP + rightFP
    totalFN = upFN + downFN + leftFN + rightFN

    precision = totalTP / (totalTP + totalFP)
    recall = totalTP / (totalTP + totalFN)

    f1Score = 2 * (precision * recall) / (precision + recall)

    print('\nPrecision: ', np.around(precision, decimals=2))
    print('\nRecall: ', np.around(recall, decimals=2))
    print('\nF1 Score:', np.around(f1Score, decimals=2))

    print('\nFalse Positives (up, down, left, right)s: ', upFP, downFP, leftFP, rightFP)



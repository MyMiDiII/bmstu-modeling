import numpy as np
import scipy as sp

from markov.probabilities import GetKolmogorovEquations

TIME_MAX = 20
TIME_STEP = 0.01
EPS = 1e-4


def GetProbabilitiesDerivatives(probabilities, _, matrix):
    derivatives = np.zeros(len(probabilities))

    for i, probability in enumerate(probabilities):
        derivatives[i] = np.dot(probabilities, matrix[i, :])

    return derivatives


def CalculateStabilizationTime(matrix, marginalProbabilities):
    timeList = np.arange(0, TIME_MAX, TIME_STEP)

    statesNumber = matrix.shape[0]
    probabilities0 = np.array([1] + [0] * (statesNumber - 1))

    kolmogorovMatrix = GetKolmogorovEquations(matrix)
    probabilitiesTable = sp.integrate.odeint(
                                GetProbabilitiesDerivatives,
                                probabilities0,
                                timeList,
                                (kolmogorovMatrix,))

    stabilizationTimes = np.zeros(statesNumber)

    for state in range(statesNumber):
        currentStateProbabilitiesTable = probabilitiesTable[:, state]

        found = False

        for i in range(1, len(currentStateProbabilitiesTable)):
            previousProbability = currentStateProbabilitiesTable[i - 1]
            currentProbability = currentStateProbabilitiesTable[i]

            if (abs(currentProbability - previousProbability) < EPS
               and abs(currentProbability - marginalProbabilities[state]) < EPS):
                found = True
                break

        stabilizationTimes[state] = timeList[i] if found else None

    return stabilizationTimes, probabilitiesTable

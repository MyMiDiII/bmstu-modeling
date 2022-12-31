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
    probabilities0 = np.array([0] * statesNumber)
    probabilities0[0] = 1

    kolmogorovMatrix = GetKolmogorovEquations(matrix)
    probabilities = sp.integrate.odeint(
                                GetProbabilitiesDerivatives,
                                probabilities0,
                                timeList,
                                (kolmogorovMatrix,))

    stabilizationTimes = np.zeros(statesNumber)

    for state in range(statesNumber):
        curStateProbabilities = probabilities[:, state]

        found = False

        for i in range(1, len(curStateProbabilities)):
            previousProbability = curStateProbabilities[i - 1]
            curProbability = curStateProbabilities[i]

            if (abs(curProbability - previousProbability) < EPS
               and abs(curProbability
                       - marginalProbabilities[state]) < EPS):
                found = True
                break

        stabilizationTimes[state] = (timeList[i] if found
                                                 else None)

    return stabilizationTimes, timeList, probabilities

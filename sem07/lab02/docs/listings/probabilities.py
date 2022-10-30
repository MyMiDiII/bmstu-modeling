import numpy as np
import scipy as sp

def GetKolmogorovEquations(matrix):
    statesNumber = matrix.shape[0]

    rightSide = np.zeros([statesNumber] * 2)

    for state in range(statesNumber):
        rightSide[state][state] = -sum(matrix[state, :])
        rightSide[state] += matrix[:, state]

    return rightSide


def GetNormalizationEquation(statesNumber):
    return 1, np.zeros(statesNumber) + 1


def CalculateMarginalProbabilities(matrix):
    statesNumber = matrix.shape[0]

    leftSide = np.zeros(statesNumber)
    rightSide = GetKolmogorovEquations(matrix)

    leftSide[-1], rightSide[-1] = GetNormalizationEquation(statesNumber)

    return sp.linalg.solve(rightSide, leftSide)

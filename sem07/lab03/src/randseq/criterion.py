import numpy as np
np.seterr('raise')

#from algorithmic import CoveyouGenerator

class RandomnessCriterion:

    def __init__(self):
        pass

    def vectorAngle(self, vector1, vector2):
        dotProduct = vector1.dot(vector2)
        normsProduct = np.linalg.norm(vector1) * np.linalg.norm(vector2)

        try:
            angle = np.rad2deg(np.arccos(dotProduct / normsProduct))
        except:
            angle = 0

        return angle


    def GetCoefficient(self, sequence):
        points = [np.array([x, y]) for x, y in zip(sequence[:-1], sequence[1:])]

        vectors = [points[i + 1] - point for i, point in enumerate(points[:-1])]

        angles = []
        score = 0
        for i, vector1 in enumerate(vectors[:-1]):
            end  = i + 11
            if end > len(vectors):
               end = len(vectors)

            for j, vector2 in enumerate(vectors[i + 1:end]):
                angle = self.vectorAngle(vector1, vector2)
                angles.append(angle)

                firstQuarterAngle = 180 - angle if angle > 90 else angle
                score += (firstQuarterAngle / 45
                        if firstQuarterAngle < 45
                        else - firstQuarterAngle / 90 + 1.5)

        return score / len(angles) if angles else 0


if __name__ == "__main__":
    print("1", RandomnessCriterion().GetCoefficient([0] * 10))
    print()
    print("2", RandomnessCriterion().GetCoefficient([i for i in range(10)]))
    print()
    print("3", RandomnessCriterion().GetCoefficient([10 - i - 1 for i in range(10)]))
    print()
    print("4", RandomnessCriterion().GetCoefficient([9,8,6,3,0]))
    print()
    print("5", RandomnessCriterion().GetCoefficient([1, 9, 1, 9, 1, 9, 1, 9, 1, 9]))
    print()
    print("6", RandomnessCriterion().GetCoefficient([4,1,8,5,1,4]))
    print()
    print("7", RandomnessCriterion().GetCoefficient([1,1,6,6,3,3,8,8]))
    print()
    print("square", RandomnessCriterion().GetCoefficient([0, 1, 4, 9, 16, 25, 36, 49, 64]))
    print()
    print("cube", RandomnessCriterion().GetCoefficient([125, 64, 27, 8, 1, 0]))
    print()
    print("lin", RandomnessCriterion().GetCoefficient([- 1.5 * i + 3 for i in range(10)]))
    print()
    print("coveyou",
    RandomnessCriterion().GetCoefficient(CoveyouGenerator(0,
                                                          9).GenerateSequence(5000)))

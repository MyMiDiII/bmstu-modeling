class RandomnessCriterion:

    def vectorAngle(self, vector1, vector2):
        dotProduct = vector1.dot(vector2)
        normsProduct = np.linalg.norm(vector1) * np.linalg.norm(vector2)

        return np.rad2deg(np.arccos(dotProduct / normsProduct))


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

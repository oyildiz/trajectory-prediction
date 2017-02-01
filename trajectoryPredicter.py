import numpy as np
from random import shuffle
def _consumeEntries(entries):
    # helper function for TrajectoryPredicter._loadTrajectories
    # entries non empty list of lines containing comma separated time index, and x, y coordinates
    result = []
    for t, line in enumerate(entries):
        timeIndex, x, y = map(float, line.split(','))
        if timeIndex < t:
            # new sequence
            t -= 1
            break
        result.append((x, y))
    return result, entries[t+1:]

class TrajectoryPredicter:
    def __init__(self, Regressor, *args, **kwargs):
        # Regressor is a class for regression, Regressor class should have fit and predict methods
        #   predict method should return Nx2 matrix where N is number of predicted coordinates
        # args and kwargs are parameters for Regressor class

        self._regressor = Regressor(*args, **kwargs)



    def train(self, samplesPath, *args, **kwargs):
        # samplesPath is the path to a csv file containing sample trajectories
        # args and kwargs are parameters for fit method of Regressor class
        # Returns L2 loss on training data
        trajectories = self._loadTrajectories(samplesPath)
        numberOfTrajectories = len(trajectories)
        numberOfEntries = sum(map(len, trajectories))
        X = np.zeros((numberOfEntries-2*numberOfTrajectories, 4))
        y = np.zeros((numberOfEntries-2*numberOfTrajectories, 2))
        index = 0
        for trajectory in trajectories:
            for (x0, y0), (x1, y1), coordinate in zip(trajectory[:-2], trajectory[1:-1], trajectory[2:]):
                X[index] = [x0, y0, x1, y1]
                y[index] = coordinate
                index += 1

        self._regressor.fit(X, y, *args, **kwargs)

        py = self._regressor.predict(X)

        return ((y-py)**2).sum()

    def _loadTrajectories(self, samplesPath):
        # samplesPath is the path to a csv file containing sample trajectories
        # Loads and returns sample trajectories. A trajectory is a sequence of coordinate pairs

        with open(samplesPath, 'r') as f:
            # load content
            content = f.read()
        # remove spaces ('\r', ' ', '\t')
        for c in '\t\r ':
            content = content.replace(c, '')
        # divide into lines
        entries = content.split('\n')
        # get rid of trailing empty lines
        while entries[-1] is '':
            entries = entries[:-1]

        sequences = []
        # while there exist entry, extract entries
        while len(entries):
            sequence, entries = _consumeEntries(entries)
            sequences.append(sequence)
        return sequences

    def _predictTrajectory(self, x0, y0, maxIter=-1):
        # predicts sequence with first two coordinates
        # (0, 0) and (x0, y0)
        # if maxIter is positive number, then at most maxIter many elements will be generated
        sequence = [(0, 0)]
        t, x, y, px, py = 1, x0, y0, 0, 0
        while y >= 0 and (maxIter <= 0 or t <= maxIter):
            sequence.append((x, y))
            data = [[px, py, x, y]]
            px, py, (x, y) = x, y, self._regressor.predict(data)[0]
            t += 1
        return sequence

    def predictTrajectory(self, outputFile, x0, y0, maxIter=100):
        # predict the trajectory whose displacement at first time instance is (x0, y0)
        # and save its result into outputFile (it is a string)
        sequence = self._predictTrajectory(x0, y0, maxIter=maxIter)
        with open(outputFile, 'w') as f:
            for t, (x, y) in enumerate(sequence):
                f.write('%d , %f , %f\n' % (t, x, y))
        return sequence

from trajectoryPredicter import TrajectoryPredicter as TP
from trueModel import estimateProjection as ET
from sklearn.linear_model import LinearRegression as LR
from sklearn.neural_network import MLPRegressor as MLP
import numpy as np

tp0 = TP(LR)
tp1 = TP(MLP, hidden_layer_sizes=[10], activation='relu', max_iter=10000, solver='lbfgs')

for t, tp in enumerate([tp0, tp1]):
    print t, tp.train('projectiles.csv')

print 'trained'
log = open("log.txt", 'w')
for v, t in [[5, 15], [20, 30], [10, 45], [25, 60], [10, 75]]:
    path = ET(v, t)
    log.write("%d & %d " % (v, t))
    for id, tp in enumerate([tp0, tp1]):
        print id, v, t
        ppath = tp.predictTrajectory('logs/%d_%d_%d.txt' % (id, v, t), *path[1])
        dists = [((x0-x1)**2+(y0-y1)**2)**0.5 for (x0, y0), (x1, y1) in zip(path, ppath)]
        if len(path) > len(ppath):
            dists += [(x**2+y**2)**0.5 for x, y in path[len(ppath):]]
        elif len(ppath) > len(path):
            dists += [(x**2+y**2)**0.5 for x, y in ppath[len(path):]]
        log.write('& $%.4e \\pm %.4e$' %  (np.mean(dists), np.std(dists)))
    log.write("\\\\\n")

import matplotlib.pyplot as plt
fig = plt.figure()
path = ET(10, 45)
p0 = tp0._predictTrajectory(*path[1])
p1 = tp1._predictTrajectory(*path[1])

ax = fig.add_subplot(1,1,1)
ax.plot([x for (x, y) in path], [y for (x, y) in path], '--', label='Theoretical')
ax.plot([x for (x, y) in p0], [y for (x, y) in p0], 'bo', label='Linear Regression')
ax.plot([x for (x, y) in p1], [y for (x, y) in p1], 'r*', label='MLP')
ax.legend(8)
fig.savefig('45_10.png')

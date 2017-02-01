import argparse
from trajectoryPredicter import TrajectoryPredicter as TP

if __name__ == '__main__':
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--outputFile', default='prediction.csv')
    parser.add_argument('-i', '--inputFile', default='projectiles.csv')
    parser.add_argument('-x', '--x', default=0.7071067811865476)
    parser.add_argument('-y', '--y', default=0.6581067811865474)
    parser.add_argument('-m', '--mode', default=1)
    cmd_args = parser.parse_args()
    if cmd_args.mode is 1:
        from sklearn.linear_model import LinearRegression as Reg
        args = []
        kwargs = {}
    elif cmd_args.mode is 2:
        from sklearn.neural_network import MLPRegressor as Reg
        args = []
        kwargs = {
                'hidden_layer_sizes':[10],
                'activation':'relu',
                'max_iter':10000,
                'solver':'lbfgs'}
    tp = TP(Reg, *args, **kwargs)
    print 'Training error', tp.train(cmd_args.inputFile)
    tp.predictTrajectory(cmd_args.outputFile, cmd_args.x, cmd_args.y)

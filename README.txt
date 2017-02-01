This project written with python 2.7.12, sklearn package (v0.18.1), and numpy package (v1.12.0).

There are 4 script files.

    - trueModel is the implementation of theoretical model. Two methods implemented in this script.
    
        - estimateTimeInstace. It computes the coordinate of a projectile at given time instance using its initial velocity and angle.
        - estimateProjection. It computes trajectory of a projectile from initial velocity and angle. This method used for evaluating implemented predicter model.
    
    - run is the script I used for computing and reporting my results.
    
    - trajectoryPredicter contains my implementation of predicter. It takes a regressor class and trains it with features constructed from sample trajectories. It also makes predictions and save their results given first coordinate in the trajectory.
    
    - main is the script for running implemented predicter. It takes five optional named command line arguments.
    
        - outputFile, is the path for storing predicted trajectory. Its default value is "./prediction.csv" and can be specified with -o flag.
        - inputFile, is the path for csv file containing sample trajectories. Its default value is "./projectiles.csv" and can be specified with -i flag.
        - mode specifies which machine learning method will be used. It can be 1 or 2. 1 means use Linear regression, and 2 means use MLP. Its default value is 1, and can be specified with -m flag.

    This script constructs a predicter and trains it. Afterwards, it predicts the trajectory of a missile launched at 45 degrees with an initial velocity 10m/s. Different trajectories can be predicted with this script using coordinates of first displacement. x and y coordinates should be given to script through -x and -y flags, respectively.

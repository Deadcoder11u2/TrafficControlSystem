import numpy as np

'''
parameters used
D => distance matrix where d(u, v) time required moving from edge u to edge v
f => this a matrix which denotes the number of vehicles moving from signal u to signal v in one T cycle
B => boolean matrix which denotes the corresponding color of the signal of the traffic light at time t(v)
'''



D = np.matrix([])
f = np.matrix([])
B = np.matrix([])
t = np.array([])

T = 4

# def heurestic(i, v):
    
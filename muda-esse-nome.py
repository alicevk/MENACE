import numpy as np

def encolhe(arr):
    return np.ravel(arr)
    # return np.flatten(arr) para cópia
    # return np.reshape(arr,-1) tbm funciona

def desencolhe(arr):
    return np.reshape(arr, (3,3))
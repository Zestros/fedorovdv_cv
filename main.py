import numpy as np
from skimage.measure import label

struct = np.ones((3,3))
def erosion(arr):
    result = np.zeros_like(arr)
    for y in range(1,arr.shape[0]-1):
        for x in range(1,arr.shape[1]-1):
            sub = arr[y-1:y+2,x-1:x+2]
            if np.all(sub==struct):
                result[y,x] = 1
    return result

date = np.load("stars.npy")
labeled = label(date)
eros = erosion(date)
labeled_eros = label(eros)
print("Звездочек всего:",np.max(labeled)-np.max(labeled_eros))

import numpy as np
import matplotlib.pyplot as plt


external = np.diag([1, 1, 1, 1]).reshape(4, 2, 2)

internal = np.logical_not(external)

cross = np.array([[[1, 0], [0, 1]], [[0, 1], [1, 0]]])


def has_color_channel(image):
    return len(image.shape) == 3 and image.shape[-1] >= 3


def match(sub, masks):
    for mask in masks:
        if np.all((sub > 0) == mask):
            return True
    return False


def count_objects(image):
    E = 0
    for y in range(0, image.shape[0] - 1):
        for x in range(0, image.shape[1] - 1):
            sub = image[y : y + 2, x : x + 2]
            if match(sub, external):
                E += 1
            elif match(sub, internal):
                E -= 1
            elif match(sub, cross):
                E += 2
    return E / 4

image = np.load("files/example2.npy")

if has_color_channel(image):
    print(np.sum([count_objects(image[:,:,i]) for i in range(image.shape[-1])]))
else:
    print(count_objects(image))
    
plt.imshow(image)
plt.show()

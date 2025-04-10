import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops

def count_holes(region):
    shape = region.image.shape
    new_image = np.zeros((shape[0] +2,shape[1] +2))
    new_image[1:-1,1:-1] = region.image
    new_image = np.logical_not(new_image)
    labeled = label(new_image)
    return np.max(labeled)-1

def extractor(region):
    area = region.area / region.image.size
    cy, cx = region.centroid_local
    cy /= region.image.shape[0]
    cx /= region.image.shape[1]
    perimeter = region.perimeter
    perimeter /= region.image.size
    eccentricity = region.eccentricity
    vlines = np.sum(region.image, 0) == region.image.shape[0]
    vlines = np.sum(vlines) / region.image.shape[1]
    x= region.image.mean(axis=0) == 1
    holes = count_holes(region)
    ratio = region.image.shape[1] / region.image.shape[0]
    return np.array([area,cy, cx, perimeter, eccentricity, vlines,
                     holes, abs(cx-cy),ratio, cx <0.44,
                     ])

def norm_l1(v1, v2):
    return ((v1 - v2)**2).sum() ** 0.5

def classificator(v, templates):
    result = "_"
    min_dist = 10**16
    for key in templates:
        d = norm_l1(v, templates[key])
        if d<min_dist:
            result = key
            min_dist=d
    return result

image = plt.imread("alphabet-small.png")#[:,:,:-1]

gray = image.mean(axis=2)
binary = gray<1
labeled = label(binary)
regions = regionprops(labeled)


templates = {'A': extractor(regions[2]), 'B': extractor(regions[3]),
             '8': extractor(regions[0]), '0': extractor(regions[1]),
             '1': extractor(regions[4]), 'W': extractor(regions[5]),
             'X': extractor(regions[6]), '*': extractor(regions[7]),
             '-': extractor(regions[9]), '/': extractor(regions[8])}


symbols = plt.imread("alphabet.png")[:,:,:-1]
gray = symbols.mean(axis=2)
binary = gray>0
labeled = label(binary)
regions = regionprops(labeled)

plt.figure()

v = extractor(regions[87])
plt.title(classificator(v,templates))
plt.imshow(regions[87].image)
plt.show()

result ={}
for i,region in enumerate(regions):
    v = extractor(region)
    symbol = classificator(v,templates)
    if symbol not in result:
        result[symbol] = 0
    result[symbol] +=1
print(result)

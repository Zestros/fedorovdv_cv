import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from skimage.morphology import binary_dilation
from pathlib import Path

def recognize(region):
    if np.all(region.image):
        return "-"
    else: # 9 symbols
        holes = count_holes(region)
        if holes==2: # B or 8:
            cy, cx = region.centroid_local
            cx /= region.image.shape[1]
            if  cx<0.44:
                return "B"
            return "8"
        elif holes==1: # A or 0
            cy, cx = region.centroid_local
            cx /= region.image.shape[1]
            cy /= region.image.shape[0]
            if count_vlines(region) >=3:
                if abs(cx-cy) > 0.034 and region.eccentricity<0.60:
                    return "D"
                else:
                    return "P"
            else:
                if abs(cx-cy) < 0.029:
                    return "0"
                return "A"
        else: # 1, *, /, X, W
            if count_vlines(region) >=3:
                return "1"
            else: # *,/,X,W
                if region.eccentricity <0.5:
                    return "*"
                else: # /,X,W
                    inf_image = ~region.image
                    inf_image = binary_dilation(inf_image, np.ones((3,3)))
                    labeled = label(inf_image, connectivity=1)
                    match np.max(labeled):
                        case 2: return "/"
                        case 4: return "X"
                        case _: return "W"

    return "_"

def count_vlines(region):
    return np.all(region.image, axis=0).sum()

def count_holes(region):
    shape = region.image.shape
    new_image = np.zeros((shape[0] +2,shape[1] + 2))
    new_image[1:-1,1:-1] = region.image
    new_image = np.logical_not(new_image)
    labeled = label(new_image)
    return np.max(labeled)-1

image = plt.imread(Path(__file__).parent / "symbols.png")[:,:,:-1]

gray = image.mean(axis=2)
binary = gray>0
labeled = label(binary)
regions = regionprops(labeled)

result ={}
out_path = Path(__file__).parent/ "out_next"
out_path.mkdir(exist_ok=True)
plt.figure()
for i,region in enumerate(regions):
    symbol = recognize(region)
    cy, cx = region.centroid_local
    cx /= region.image.shape[1]
    cy /= region.image.shape[0]
    if symbol not in result:
        result[symbol] = 0
    result[symbol] +=1
    plt.cla()
    plt.title(symbol)
    plt.imshow(region.image)
    plt.savefig(out_path / f"{i:03d}.png")
print(result)
        

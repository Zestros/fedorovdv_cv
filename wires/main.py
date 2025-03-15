import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label
from skimage.morphology import (binary_closing,binary_erosion
                                ,binary_dilation,binary_opening)
date = np.load("task3/wires6npy.txt")
labeled = label(date)
result = binary_erosion(date,np.ones(3).reshape(3,1))
resulted = label(result)

print("Количество проводов равно: ",np.max(labeled))
for i in range(np.max(labeled)):
    labeled1 = (labeled==i+1)
    res = binary_erosion(labeled1,np.ones(3).reshape(3,1))
    resd = label(res)
    if (np.max(resd)==1):
        print(f"Провод {1+i} не порван ")
    elif (np.max(resd)==0):
        print(f"Провод {1+i} не существовал ")
    else:
        print(f"Провод {1+i} порван на частей: {np.max(resd)} ")
plt.imshow(date)
plt.show()

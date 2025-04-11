import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label, regionprops
from skimage.morphology import binary_erosion
from skimage.color import rgb2hsv
from collections import defaultdict


def find_indices(arr):
    diff = np.diff(arr) 
    std = np.std(diff) * 2 
    indices = np.where(diff > std)[0] + 1  
    return indices
def colors(region, image):
    
    y, x = region.centroid
    hue_value = rgb2hsv(image[int(y),int(x)])[0]
    
    # Определяем цвет на основе порогов
    if 0.0 <= hue_value < 0.19202898:
        return "Красный"
    elif 0.19202898 <= hue_value < 0.30476192:
        return "Оранжевый"
    elif 0.30476192 <= hue_value < 0.41509435:
        return "Желтый"
    elif 0.41509435 <= hue_value < 0.60897434:
        return "Зеленый"
    elif 0.60897434 <= hue_value < 0.8333333:
        return "Синий"
    else:
        return "Фиолетовый"
    
image = plt.imread("balls_and_rects.png")

binary = image.mean(axis=2)
binary[binary>0] = 1
labeled = label(binary)
regions = regionprops(labeled)

dict_balls = {}
dict_rects = {}
for region in regions:
    color = colors(region, image)
    if region.eccentricity == 0:
        if color not in dict_balls:
            dict_balls[color] = 0
        dict_balls[color]+=1
    else:
        if color not in dict_rects:
            dict_rects[color] = 0
        dict_rects[color]+=1
        
total_objects = sum(dict_balls.values()) + sum(dict_rects.values())
print("Общее число фигур:",total_objects)
print("Шары:",dict_balls)
print("Прямоугольники:",dict_rects)


#colors =[]
#for region in regions:
#    if region.eccentricity==0:
#        c+=1
#        y,x = region.centroid
#        colors.append(rgb2hsv(image[int(y),int(x)])[0])
#    if region.eccentricity!=0:
#        p+=1
#        y,x = region.centroid
#        colors.append(rgb2hsv(image[int(y),int(x)])[0])
#k=sorted(colors)
#for i in find_indices(k):
#    print(k[i-1],k[i])


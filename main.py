import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from pathlib import Path
from skimage.color import rgb2gray
from skimage.filters import sobel, threshold_otsu
from skimage.morphology import (binary_closing,binary_erosion
                                ,binary_dilation,binary_opening)


image_path = Path(__file__).parent / 'images'
total_pen=0
for i in range(1,13):
    image = plt.imread(image_path / f"img ({i}).jpg")

    gray_image = rgb2gray(image)

    s = sobel(gray_image)
    thresh = threshold_otsu(s)

    s[s< thresh] =0
    s[s>= thresh] =1


    labeled = label(binary_dilation(binary_erosion(binary_dilation(s,
                           np.ones((10,10))),np.ones((3,3))),np.ones((10,10))))
    regions = regionprops(labeled)

    height, width = gray_image.shape[:2]
    total_area = height * width
    min_area = total_area * 0.005

    ratio_threshold = 10
    selected_regions = []
    for region in regions:
        major_axis_length = region.major_axis_length
        minor_axis_length = region.minor_axis_length
        ratio = major_axis_length / minor_axis_length
        
        if ratio >= ratio_threshold and ratio <= ratio_threshold*2 and region.area > min_area:
            selected_regions.append(region)
    print(f"Количество карандашей на картинке {i}: {len(selected_regions)}")
    total_pen +=len(selected_regions)
print(f"Количество карандашей на всех картинках: {total_pen}")

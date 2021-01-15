import sys

import cv2
from PIL import Image

from utils.show_Image_1 import get_color_2, get_color_3
from utils.util import lab2rgb, rgb2lab
import numpy as np

#将rgb转换为lab格式
def get_lab_info(color):

    result = [];
    result_width = 200;
    result_height_per_center = 80;
    n_channels = 3;
    k_palette = len(color)
    for i in range(k_palette):
            result.append(
                np.full((result_width * result_height_per_center, n_channels), color[i], dtype=int))
    result = np.array(result)

    result = result.reshape((result_height_per_center * (k_palette), result_width, n_channels))
    file_name = r'../use_get_.jpg'
    file_name01 = file_name

    cv2.imwrite(file_name01, result)
    img1 = Image.open(file_name01);

    lab_ = rgb2lab(img1)

    lab_pixels = lab_.load();
    pixels_lab = np.zeros([result.shape[0],result.shape[1],n_channels])
    print(pixels_lab.shape)
    for i in range(result.shape[1]):
        for j in range(result.shape[0]):
            pixels_lab[j,i] = lab_pixels[i,j];
    color_centers = get_color_2(pixels_lab, k_palette)
    centers = np.array(color_centers);
    return centers;

def get_rgb(centers,labels,n_channels,k_palette):
    center_counts = {}
    for i in range(k_palette):
        center_counts[ i ] = labels[i];

    centers_index_sorted = [center[0] for center in
                            sorted(center_counts.items(), key=lambda center: center[1], reverse=True)]
    result = [];
    result_width = 200
    result_height_per_center = 80
    centers_index_sorted = np.array(centers_index_sorted);
    for center_index in centers_index_sorted:
            result.append(
                np.full((result_width * result_height_per_center, n_channels), centers[center_index], dtype=int))

    result = np.array(result)

    result = result.reshape((result_height_per_center * (k_palette), result_width, n_channels))
    file_name = r'../get_rgb_use.png';
    file_name = file_name;
    cv2.imwrite(file_name, result)
    img1 = Image.open(file_name);

    result1 = Image.new('LAB', img1.size)
    result_pixels = result1.load()

    for i in range(img1.width):
        for j in range(img1.height):
            x = tuple(result[j, i, :])
            result_pixels[i, j] = x;
    rgb = lab2rgb(result1)
    rgb.save(file_name)

    img_ = cv2.imread(file_name, 1);
    img_weight = img_.shape[0];
    img_height = img_.shape[1];
    n_pixel = img_weight * img_height;

    img_ori = img_.reshape(n_pixel, 3);

    # 获得最多的五个像素点
    color_centers = get_color_3(img_ori, k_palette)
    centers = np.array(color_centers);
    # print('原图按顺序的RGB')
    # print(centers)

    return centers


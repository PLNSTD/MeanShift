import cv2 as cv
import math
import utils
import numpy as np
import time


def colordistance(color_a, color_b):
    blue = int(color_a[0]) - int(color_b[0])
    green = int(color_a[1]) - int(color_b[1])
    red = int(color_a[2]) - int(color_b[2])
    distance = math.sqrt((blue ** 2) + (green ** 2) + (red ** 2))
    return distance


def pointdistance(point_a, point_b):
    distance = math.sqrt((point_b[0] - point_a[0]) ** 2 + (point_b[1] - point_a[1]) ** 2)
    return distance


def shift2(img, center_point, center_color, point_band, color_band):
    n = blue = green = red = x_shift = y_shift = 0
    bgrArray = [
        [img[row][column][0], img[row][column][1], img[row][column][2], row, column]
        for row in range(center_point[0] - point_band, center_point[0] + point_band)
            for column in range(center_point[1] - point_band, center_point[1] + point_band)
                if 0 <= row < img.shape[0]
                if 0 <= column < img.shape[1]
                if pointdistance(center_point, [row, column]) < point_band
                if colordistance(center_color, img[row][column]) < color_band]
    # print("ARRAY: ")
    n = len(bgrArray)
    if n != 0:
        # axis = 0 sum columns with [index]
        # axis = 1 sum rows with [index]
        blue = np.sum(bgrArray, axis=0)[0]
        green = np.sum(bgrArray, axis=0)[1]
        red = np.sum(bgrArray, axis=0)[2]
        y_shift = np.sum(bgrArray, axis=0)[3]
        x_shift = np.sum(bgrArray, axis=0)[4]
        x_shift = x_shift / n
        y_shift = y_shift / n
        blue = blue / n
        green = green / n
        red = red / n
        center_point[0] = y_shift
        center_point[1] = x_shift
        center_color[0] = blue
        center_color[1] = green
        center_color[2] = red
    return np.copy(center_point), np.copy(center_color)


def shift(img, center_point, center_color, point_band, color_band):
    n = blue = green = red = x_shift = y_shift = 0
    for row in range(center_point[0] - point_band, center_point[0] + point_band):
        for column in range(center_point[1] - point_band, center_point[1] + point_band):
            if 0 <= row < img.shape[0] and 0 <= column < img.shape[1] \
                    and pointdistance(center_point, [row, column]) < point_band:
                neighbour_point = np.array([row, column])
                b, g, r = np.array(img[neighbour_point[0]][neighbour_point[1]])
                neigh_color = np.array([b, g, r])
                if colordistance(center_color, img[row][column]) < color_band:
                    x_shift = x_shift + column
                    y_shift = y_shift + row
                    blue = blue + neigh_color[0]
                    green = green + neigh_color[1]
                    red = red + neigh_color[2]
                    n = n + 1
    x_shift = x_shift / n
    y_shift = y_shift / n
    blue = blue / n
    green = green / n
    red = red / n
    center_point[0] = y_shift
    center_point[1] = x_shift
    center_color[0] = blue
    center_color[1] = green
    center_color[2] = red
    return np.copy(center_point), np.copy(center_color)


def meanshift(src, point_band, color_band): # img, spatial radius, color radius
    print("Start: %s" % (time.asctime(time.localtime(time.time()))))
    start_time = time.time()
    img = np.copy(src)
    rows = img.shape[0]
    cols = img.shape[1]
    for x in range(cols):
        for y in range(rows):
            center_point = np.array([y, x])
            b, g, r = np.copy(img[y][x])
            center_color = np.array([b, g, r])
            curr_point = np.copy(center_point)
            prev_color = np.copy(center_color)
            iter_count = 0
            while True:
                prev_color = np.copy(center_color)
                curr_point, center_color = shift(img, curr_point, center_color, point_band, color_band) # 2
                iter_count = iter_count + 1
                if colordistance(center_color, prev_color) < 0.3 \
                        or pointdistance(center_point, curr_point) < 0.3 \
                        or iter_count == 10:
                    break
            img[y][x][0] = center_color[0]
            img[y][x][1] = center_color[1]
            img[y][x][2] = center_color[2]
            '''if x % 50 == 0 and y % 50 == 0:
                print("%d-%d" % (x,y))'''
    print("\tSecondi: %s" % (time.time() - start_time))
    print("Finish: %s" % (time.asctime(time.localtime(time.time()))))
    return img

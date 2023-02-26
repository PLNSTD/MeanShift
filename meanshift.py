import cv2 as cv
import numpy as np
import math
import time


def color_distance(color_a, color_b):
    blue = int(color_a[0]) - int(color_b[0])
    green = int(color_a[1]) - int(color_b[1])
    red = int(color_a[2]) - int(color_b[2])
    distance = math.sqrt((blue ** 2) + (green ** 2) + (red ** 2))
    return distance


def point_distance(point_a, point_b):
    distance = math.sqrt((point_b[0] - point_a[0]) ** 2 + (point_b[1] - point_a[1]) ** 2)
    return distance


def meanshift(src, point_radius, color_radius):
    print("Start: %s" % (time.asctime(time.localtime(time.time()))))
    start_time = time.time()
    img = np.copy(src)
    d = 3
    rows = img.shape[0]
    cols = img.shape[1]
    curr_img = np.copy(img)
    step = 0
    images = []
    while True:
        prev_img = np.copy(curr_img)
        shift = 0
        for i in range(rows):
            for j in range(cols):
                val_sum = [0] * d
                count = 0
                for m in range(i - point_radius, i + point_radius):
                    if 0 <= m < rows:
                        for n in range(j - point_radius, j + point_radius):
                            if 0 <= n < cols:
                                if point_distance((i, j), (m, n)) < point_radius \
                                        and color_distance(prev_img[i][j], prev_img[m][n]) < color_radius:
                                    for k in range(d):
                                        val_sum[k] += int(prev_img[m][n][k])
                                    count += 1
                for k in range(d):
                    curr_img[i][j][k] = int(val_sum[k] / count)
                    shift += abs(int(curr_img[i][j][k]) - int(prev_img[i][j][k]))
        step += 1
        images.append(curr_img)
        if shift < rows*cols or step == 40:
            print("Difference-iter: %d-%d" % (shift, step))
            break
    exec_time = time.time() - start_time
    print("\tSecondi: %s" % exec_time)
    print("Finish: %s" % (time.asctime(time.localtime(time.time()))))
    '''for x in images:
        cv.imshow('AfterMs', x)
        cv.waitKey(0)'''
    return [curr_img, exec_time]

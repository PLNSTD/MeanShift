import os

import cv2 as cv
import numpy as np
import cProfile
import MeanShift as ms
import Segmentation as seg

def main():
    img = cv.imread('../data/baboon.jpg', cv.IMREAD_COLOR)

    if img.shape[0] > 256 or img.shape[1] > 256:
        img = cv.resize(img, (256, 256), None, None, None, None)
    '''cv.imshow('Original', img)
    cv.waitKey(0)'''
    filtered = ms.meanshift(img, 8, 75)
    '''filename = 'savedImage.jpg'
    segmentedImg = cv.imread('../savedImage.jpg', cv.IMREAD_COLOR)
    if segmentedImg is None:
        # Saving the image
        # cv.imwrite(filename, filtered)
        # List files and directories
        print("After saving image:")
        directory = r'D:\PythonWorkspace\Projects\OpenCV'
        os.chdir(directory)
        print(os.listdir(directory))
        print('Successfully saved')
        segmentedImg = cv.imread('../savedImage.jpg', cv.IMREAD_COLOR)
    # segmentedImg = np.copy(filtered)
    cv.imshow("Filtered2", segmentedImg)
    cv.waitKey(0)
    segmented = seg.segmentation_ms(segmentedImg, 75)'''


if __name__ == '__main__':
    main()

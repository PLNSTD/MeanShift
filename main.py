import cv2 as cv
import meanshift as ms
import numpy as np
from os import listdir
from os.path import join, isfile


def main():
    wantImgGray = False
    mypath = '../images/'
    im_dirs = [f for f in listdir(mypath)]
    for im_dir in im_dirs:
        im_dir = join(mypath, im_dir)
        images = [f for f in listdir(im_dir) if isfile(join(im_dir, f))]
        h = 0
        scale_factor = 3/2
        if '15' in im_dir:
            h = 15 * scale_factor
        elif '20' in im_dir:
            h = 20 * scale_factor
        elif '25' in im_dir:
            h = 25 * scale_factor
        elif '17' in im_dir:
            h = 17 * scale_factor
        for image in images:
            print('H value: %d' % h)
            image_path = join(im_dir, image)
            img = cv.imread(image_path, cv.IMREAD_COLOR)
            if wantImgGray:
                img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
                img = np.stack((img,) * 3, axis=-1)
            img = cv.resize(img, (720, 480))
            mspp_img = ms.meanshift(img, 8, h)
            filename = 'resultnt/seg_gray720x480' + image
            status = cv.imwrite(filename, mspp_img[0])
            print('Image written: %s - Status: %s' % (image, status))
            with open('resultnt/record.txt', 'a') as f:
                exec_time = mspp_img[1]
                result = 'H value: ' + str(h) + ' ' + image + ': ' + str(exec_time) + '\n'
                f.write(result)
                f.close()
    '''img = cv.imread('../dataset/vegetables.jpg')
    dataset.append(img)
    if img.shape[0] > 256 or img.shape[1] > 256:
        img = cv.resize(img, (256, 256))
    cv.imshow('Original', img)
    cv.waitKey(0)
    filtered = ms.meanshift(img, 8, 37.5)'''
    # cs.segmentation_ms(filtered, 30)


if __name__ == '__main__':
    main()

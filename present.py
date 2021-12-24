import cv2
import numpy as np


def show1():
    raw_image = cv2.imread('/home/palm/PycharmProjects/ocr/redstamp/doc 126.png')
    cv2.imshow('ori', raw_image)
    image = raw_image.copy()
    h = image.shape[0]
    w = image.shape[1]
    blue = raw_image[int(h/2.9):int(h/1.4), :, 0]
    red = raw_image[int(h/2.9):int(h/1.4), :, 2]
    cv2.imshow('b1', blue)
    cv2.imshow('r1', red)
    blue[blue > 100] = 255
    blue[blue < 100] = 0
    red[red > 100] = 255
    red[red < 100] = 0
    cv2.imshow('b', blue)
    cv2.imshow('r', red)
    blue[red == blue] = 0
    cv2.imshow('!=', 255-blue)


def show2():
    raw_image = cv2.imread('/home/palm/PycharmProjects/ocr/redstamp/doc 185.png')
    cv2.imshow('ori', raw_image)
    image = raw_image.copy()
    h = image.shape[0]
    w = image.shape[1]
    image = image[int(h/2.9):int(h/1.4)]
    cv2.imshow('a', image)
    im2 = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    low_red = np.array([100, 100, 90])
    high_red = np.array([130, 255, 255])
    blue_mask = cv2.inRange(im2, low_red, high_red)
    im2 = 255 - cv2.cvtColor(blue_mask, cv2.COLOR_GRAY2BGR)
    cv2.imshow('blue_m', blue_mask)
    cv2.imshow('blue', im2)


def show3():
    im = cv2.imread('/home/palm/PycharmProjects/project-1/data/processed/png/doc 128.png')
    im = im[0:int(im.shape[0] * 25 / 160), ]
    cv2.imshow('im', im)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    cv2.imshow('hsv', im)
    low_blue = np.array([100, 24, 30])
    high_blue = np.array([140, 255, 255])
    blue_mask = cv2.inRange(im, low_blue, high_blue)
    im2 = im.copy()
    im2[blue_mask >= 200] = [0, 0, 0]
    cv2.imshow('mask', blue_mask)
    im3 = 255 - cv2.cvtColor(blue_mask, cv2.COLOR_GRAY2BGR)
    cv2.imshow('blue', im3)
    low_red = np.array([140, 24, 30])
    high_red = np.array([180, 255, 255])
    red_mask1 = cv2.inRange(im, low_red, high_red)
    im2[red_mask1 >= 200] = [0, 0, 0]
    low_red = np.array([0, 24, 30])
    high_red = np.array([20, 255, 255])
    red_mask2 = cv2.inRange(im, low_red, high_red)
    im2[red_mask2 >= 200] = [0, 0, 0]
    cv2.imshow('hsv_masked', im2)

    im = cv2.cvtColor(im, cv2.COLOR_HSV2BGR)
    im[blue_mask >= 200] = 255
    im[red_mask1 >= 200] = 255
    im[red_mask2 >= 200] = 255
    cv2.imshow('im_masked', im)


if __name__ == '__main__':
    show3()
    cv2.waitKey()

import cv2
import numpy as np

if __name__ == '__main__':
    image = cv2.imread('/home/palm/PycharmProjects/project-1/data/processed/png/doc 128.png')
    image = image[0:int(image.shape[0] * 25 / 160), ]
    filter = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    image[np.where(image[:, :, 0] > 180)] = 255
    image[np.where(image[:, :, 2] > 180)] = 255
    cv2.imshow('1', image)
    im2 = cv2.filter2D(image, -1, filter)
    im2[np.where(im2[:, :, 0] > 170)] = 255
    im2[np.where(im2[:, :, 2] > 170)] = 255
    cv2.imshow('2', im2)
    cv2.waitKey()

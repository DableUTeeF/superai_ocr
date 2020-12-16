import cv2
import pytesseract
import os

if __name__ == '__main__':
    root = 'redstamp'
    for file in os.listdir(root):
        image = cv2.imread(os.path.join(root, file))
        # image = cv2.boxFilter(image, -1, (5, 5))
        image[image[..., 2] > 100] = 255
        image[image[..., 2] < 100] = 0

        image = image[image.shape[0] // 3:, :]
        cv2.imshow('r', image[..., 2])
        text = pytesseract.image_to_string(image[..., 2], lang='tha')
        count = 0
        for char in text:
            if 47 < ord(char) < 58:
                print(char, end='')
                count += 1
            if count >= 4:
                print()
                break
        cv2.waitKey()

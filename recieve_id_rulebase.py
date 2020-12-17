import cv2
import pytesseract
import os
from PIL import Image
import numpy as np
import easyocr
reader = easyocr.Reader(['en'])

if __name__ == '__main__':
    root = 'redstamp'
    for file in os.listdir(root):
        # if '196' not in file:
        #     continue

        raw_image = cv2.imread(os.path.join(root, file))
        raw_image = raw_image[raw_image.shape[0] // 3:, :]
        image = raw_image.copy()
        # image = cv2.boxFilter(image, -1, (5, 5))
        image[image[..., 2] > 100] = 255
        # image[image[..., 2] < 100] = 0

        # pil_image = Image.fromarray(image[..., 2])
        # pil_image.show()
        k = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]], np.uint8)
        red = 255-cv2.morphologyEx(255-image[..., 2], cv2.MORPH_CLOSE, k)
        red = 255-cv2.morphologyEx(255-red, cv2.MORPH_CLOSE, k)
        cv2.imshow('r', red)
        res = reader.recognize(red)
        print(res)
        result = pytesseract.image_to_data(red, lang='tha', output_type=pytesseract.Output.DICT)
        count = 0
        x1 = float('inf')
        y1 = float('inf')
        x2 = -float('inf')
        y2 = -float('inf')
        line_num = 100
        for i in range(len(result['text'])):
            for char in result['text'][i]:
                if result['line_num'][i] > line_num:
                    # print()
                    break
                if 47 < ord(char) < 58:
                    if result['top'][i] + result['height'][i] > y2:
                        y2 = result['top'][i] + result['height'][i]
                    # print(char, end='')
                    if line_num == 100:
                        line_num = result['line_num'][i]
            if count >= 4:
                break
        cv2.line(raw_image, (0, y2), (image.shape[1], y2), (0, 255, 0))
        # pil_image = Image.fromarray(raw_image[..., ::-1])
        # pil_image.show()
        cv2.imshow('raw', raw_image)
        blue = raw_image[y2:, :, 2]
        blue[raw_image[y2:, :, 2] > 100] = 255
        blue[raw_image[y2:, :, 2] < 100] = 0
        # cv2.imshow('blue', blue)
        # k = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]], np.uint8)
        # blue = 255-cv2.morphologyEx(255-blue, cv2.MORPH_CLOSE, k)
        # blue = 255-cv2.morphologyEx(255-blue, cv2.MORPH_CLOSE, k)
        text = pytesseract.image_to_string(blue, lang='tha')
        print(text)

        # pil_image = Image.fromarray(blue)
        # pil_image.show()
        cv2.imshow('closed', blue)
        cv2.waitKey()
        # break

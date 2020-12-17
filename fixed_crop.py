import cv2
import os
import pytesseract
import numpy as np
import easyocr
reader = None

if __name__ == '__main__':
    root = 'redstamp'
    for file in os.listdir(root):
        # if '131' not in file:
        #     continue

        raw_image = cv2.imread(os.path.join(root, file))
        cv2.imshow('ori', raw_image)
        image = raw_image.copy()
        # image[image[..., 2] > 100] = 255
        # image[image[..., 2] < 100] = 0

        height = image.shape[0]
        width = image.shape[1]
        im1 = image[int(height/3.2):int(height/1.75), int(width*0.25):].copy()
        im2 = image[height//2:int(height/1.25)].copy()
        cv2.imshow('color1', im1)
        im1[im1[..., 2] > 100] = 255
        im1[im1[..., 0] > 100] = 255
        im1[im1[..., 2] < 100] = 0
        k = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]], np.uint8)
        im1 = 255-cv2.morphologyEx(255-im1, cv2.MORPH_CLOSE, k)
        im1 = 255-cv2.morphologyEx(255-im1, cv2.MORPH_CLOSE, k)

        # tha_id = pytesseract.image_to_string(im1, lang='tha').split('\n')[0]
        eng_id = pytesseract.image_to_data(im1, output_type='dict')
        selected_id = ''
        for i in range(len(eng_id['text'])):
            word = eng_id['text'][i]
            if len(word) > len(selected_id):
                selected_id = word
        if len(selected_id) == 0:
            tha_id = pytesseract.image_to_data(im1, lang='tha', output_type='dict')
            for i in range(len(tha_id['text'])):
                word = tha_id['text'][i]
                if len(word) > len(selected_id):
                    selected_id = word
        if len(selected_id) == 0:
            if reader is None:
                reader = easyocr.Reader(['en'])
            res = reader.recognize(im1)
            for result in res:
                word = result[1]
                if len(word) > len(selected_id):
                    selected_id = word
        print(selected_id)

        # cv2.imshow('1', im1)
        cv2.imshow('color2', im2)
        im2 = cv2.cvtColor(im2, cv2.COLOR_BGR2HSV)
        low_red = np.array([100, 80, 90])
        high_red = np.array([130, 255, 255])
        blue_mask = cv2.inRange(im2, low_red, high_red)
        im2 = 255-cv2.cvtColor(blue_mask, cv2.COLOR_GRAY2BGR)
        # im2 = 255-cv2.morphologyEx(im2, cv2.MORPH_CLOSE, k)
        # im2 = 255-cv2.morphologyEx(255-im2, cv2.MORPH_CLOSE, k)
        thai_date = pytesseract.image_to_string(im2, lang='tha').split(' ')
        eng_date = pytesseract.image_to_string(im2).split(' ')
        selected_day = eng_date[-3]
        selected_month = thai_date[-2]
        selected_year = eng_date[-1]
        selected_year = selected_year.replace('\n', '')
        selected_year = selected_year.replace('\f', '')
        print(f'{selected_day} {selected_month} {selected_year}')

        # print(pytesseract.image_to_string(im2, lang='tha').split('\n')[0])
        # print(pytesseract.image_to_string(im2).split('\n')[0])
        # print(pytesseract.image_to_string(im2, lang='tha').split('\n')[0])
        # print(pytesseract.image_to_string(im2).split('\n')[0])
        print()
        cv2.imshow('1', im1)
        cv2.imshow('2', im2)
        cv2.waitKey()

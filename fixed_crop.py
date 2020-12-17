import cv2
import os
import pytesseract
import numpy as np
import easyocr
from fuzzywuzzy import process

reader = None
months = ["ม.ค.","ก.พ.","มี.ค.","เม.ย.","พ.ค.","มิ.ย.","ก.ค.","ส.ค.","ก.ย.","ต.ค.","พ.ย.","ธ.ค."]
similarToNum = {"A":'4',"B":'3',"C":'0',"D":'0',"E":'8',"F": '',"G":'0',"H":'5',"I":'1',"J":'1',"K":'',
            "L":'1',"M":'',"N":'',"O":'0',"P":'0',"Q":'0',"R":'0',"S":'5',"T":'1',"U":'0',"V":'0',"W":'',
            "X":"","Y":'1',"Z":'2',"a":'0',"b":'0',"c":'0',"d":'0',"e":'0',"f":'1',"g":'8',"h":'5',"i":'1',"j":'1',
            "k":'8',"l":'1',"m":'',"n":'0',"o":'0',"p":'9',"q":'9',"r": '1',"s":'5',"t":'1',"u":'0',"v":'0',"w":'',
            "x":'',"y":'',"z":'2',"$":'0',"!":'1',"@":'8',"§":'0'}

def findMonth(str2Match):

  Ratios = process.extract(str2Match,months)
  print(Ratios)

  closest = process.extractOne(str2Match,months)
  return(closest[0])

def mapToNum(str):
  final_str = ""
  for s in str:
    try:
      to_num = similarToNum[s]
      final_str = final_str + to_num
    except:
      final_str = final_str + s
  return final_str

if __name__ == '__main__':
    root = 'redstamp'
    for file in os.listdir(root):

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
        thai_date = pytesseract.image_to_string(im2, lang='tha').split('\n')[0].split(' ')
        eng_date = pytesseract.image_to_string(im2).split('\n')[0].split(' ')
        selected_day = mapToNum(eng_date[-3])
        selected_month = findMonth(thai_date[-2])
        selected_year = mapToNum(eng_date[-1])
        # selected_year = selected_year.replace('\n', '')
        # selected_year = selected_year.replace('\f', '')
        print(f'{selected_day} {selected_month} {selected_year}')

        # print(pytesseract.image_to_string(im2, lang='tha').split('\n')[0])
        # print(pytesseract.image_to_string(im2).split('\n')[0])
        # print(pytesseract.image_to_string(im2, lang='tha').split('\n')[0])
        # print(pytesseract.image_to_string(im2).split('\n')[0])
        print()
        cv2.imshow('1', im1)
        cv2.imshow('2', im2)
        cv2.waitKey()

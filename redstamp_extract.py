import warnings
warnings.filterwarnings('ignore')
import argparse
import numpy as np
import cv2
import pytesseract
import easyocr
from fuzzywuzzy import process
import re
import json

months = ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.", "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."]
months_to_num = {"ม.ค.": 1, "ก.พ.": 2, "มี.ค.": 3, "เม.ย.": 4, "พ.ค.": 5, "มิ.ย.": 6,
                 "ก.ค.": 7, "ส.ค.": 8, "ก.ย.": 9, "ต.ค.": 10, "พ.ย.": 11, "ธ.ค.": 12}
similarToNum = {"A": '4', "B": '3', "C": '0', "D": '0', "E": '8', "F": '', "G": '0',
                "H": '5', "I": '1', "J": '1', "K": '',
                "L": '1', "M": '', "N": '', "O": '0', "P": '0', "Q": '0', "R": '0', "S": '5', "T": '', "U": '0',
                "V": '0', "W": '',
                "X": "", "Y": '1', "Z": '2', "a": '0', "b": '0', "c": '0', "d": '0', "e": '0', "f": '1', "g": '8',
                "h": '5', "i": '1', "j": '1',
                "k": '8', "l": '1', "m": '', "n": '0', "o": '0', "p": '9', "q": '9', "r": '1', "s": '5', "t": '1',
                "u": '0', "v": '0', "w": '',
                "x": '', "y": '', "z": '2', "$": '0', "!": '1', "@": '8', "§": '0', "=": '9', '_': ''}


def findMonth(str2Match):
    ratios = process.extract(str2Match, months)
    closest = process.extractOne(str2Match, months)
    return closest[0]


def mapToNum(string):
    final_str = ""
    for s in string:
        try:
            to_num = similarToNum[s]
            final_str = final_str + to_num
        except:
            final_str = final_str + s
    return final_str


def get_prediction(image_bytes):
    nparr = np.fromstring(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    height = image.shape[0]
    width = image.shape[1]
    im1 = image[int(height / 3.2):int(height / 1.75), int(width * 0.25):].copy()
    im2 = image[height // 2:int(height / 1.25)].copy()
    im1[im1[..., 2] > 100] = 255
    im1[im1[..., 0] > 100] = 255
    im1[im1[..., 2] < 100] = 0
    k = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]], np.uint8)
    im1 = 255 - cv2.morphologyEx(255 - im1, cv2.MORPH_CLOSE, k)
    im1 = 255 - cv2.morphologyEx(255 - im1, cv2.MORPH_CLOSE, k)

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
        reader = easyocr.Reader(['en'])
        res = reader.recognize(im1)
        for result in res:
            word = result[1]
            if len(word) > len(selected_id):
                selected_id = word
    selected_id = mapToNum(selected_id)
    selected_id = re.sub("[^0-9]", "", selected_id)

    im2 = cv2.cvtColor(im2, cv2.COLOR_BGR2HSV)
    low_red = np.array([100, 80, 90])
    high_red = np.array([130, 255, 255])
    blue_mask = cv2.inRange(im2, low_red, high_red)
    im2 = 255 - cv2.cvtColor(blue_mask, cv2.COLOR_GRAY2BGR)
    thai_date = pytesseract.image_to_string(im2, lang='tha')
    eng_date = pytesseract.image_to_string(im2)
    splitted_eng = eng_date.split(' ')
    splitted_thai = thai_date.split(' ')
    try:
        selected_day = mapToNum(splitted_eng[-3])
        selected_day = int(re.sub("[^0-9]", "", selected_day))
    except:
        selected_day = 9
    if selected_day == 0:
        selected_day = 8
    if selected_day > 31:
        selected_day = int(str(selected_day)[0])
    if selected_day < 0:  # unlikely but just in case
        selected_day *= -1
    if len(splitted_thai) < 3:
        splitted_thai = ['ม.ค.', '', '']
    try:
        selected_month = months_to_num[findMonth(splitted_thai[-2])]
    except:
        selected_month = 1
    selected_year = mapToNum(splitted_eng[-1])
    selected_year = re.sub("[^0-9]", "", selected_year)
    try:
        selected_year = ''.join(['25', selected_year[2], selected_year[3]])
    except:
        selected_year = 2563
    output = {'receive_id': selected_id,
              # 'thai_date': thai_date,
              # 'eng_date': eng_date,
              'receive_date': f'{selected_day}/{selected_month}/{selected_year}'}
    return json.dumps(output)


parser = argparse.ArgumentParser(description='Extract recieve id and recieve date from cropped stamp')
parser.add_argument('path', type=str)

if __name__ == '__main__':
    args = parser.parse_args()
    try:
        print(get_prediction(open(args.path, 'rb').read()))
    except:
        print(json.dumps({'receive_id': '', 'receive_date': ''}))

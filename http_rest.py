from flask import Flask, jsonify, request
import numpy as np
import cv2
import pytesseract
import easyocr

app = Flask(__name__)
reader = easyocr.Reader(['en'])


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
        res = reader.recognize(im1)
        for result in res:
            word = result[1]
            if len(word) > len(selected_id):
                selected_id = word

    im2 = cv2.cvtColor(im2, cv2.COLOR_BGR2HSV)
    low_red = np.array([100, 80, 90])
    high_red = np.array([130, 255, 255])
    blue_mask = cv2.inRange(im2, low_red, high_red)
    im2 = 255 - cv2.cvtColor(blue_mask, cv2.COLOR_GRAY2BGR)
    thai_date = pytesseract.image_to_string(im2, lang='tha')
    eng_date = pytesseract.image_to_string(im2)
    output = {'revieve_id': selected_id, 'thai_date': thai_date, 'eng_date': eng_date}
    return output


@app.route('/ocr/redstamp', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        img_bytes = file.read()
        output = get_prediction(image_bytes=img_bytes)
        return jsonify(output)


if __name__ == '__main__':
    app.run()

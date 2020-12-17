import requests
from http_rest import get_prediction
import os

# resp = requests.post("http://localhost:5000/ocr/redstamp",
#                      files={"file": open('/home/palm/PycharmProjects/ocr/redstamp/doc 187.png', 'rb')})
# print(resp.json())
print(get_prediction(open('/home/palm/PycharmProjects/ocr/redstamp/doc 187.png', 'rb').read()))


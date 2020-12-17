import requests

resp = requests.post("http://localhost:5000/ocr/redstamp",
                     files={"file": open('/home/palm/PycharmProjects/ocr/redstamp/doc 135.png', 'rb')})
print(resp.json())

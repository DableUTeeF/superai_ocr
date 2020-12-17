import requests

resp = requests.post("http://localhost:5000/ocr/redstamp",
                     files={"file": open('/home/palm/PycharmProjects/ocr/redstamp/doc 133.png', 'rb')})
print(resp.json())

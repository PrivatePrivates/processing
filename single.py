import json
import requests
from werkzeug.datastructures import Headers

URL = "http://127.0.0.1:5000"

base_image = "../img-1.jpg"
comparison_image = "../img-2.jpg"

data = {"image1": base_image, "image2": comparison_image}
headers = {'content-type': 'application/json'}

res = requests.post(URL, data=json.dumps(data), headers=headers)
print(res.json())

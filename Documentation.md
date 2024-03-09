# Moroccan Automatic Number Plate Recognition (ANPR) API

## Introduction
Welcome to the Automatic Number Plate Recognition (ANPR) API documentation. Our state-of-the-art software equips your applications with advanced ANPR capabilities, facilitating efficient license plate detection and recognition. This solution enhances security and provides seamless integration for diverse applications.

## Getting Started
To effortlessly integrate this powerful tool into your applications or systems, utilize a framework capable of interacting with a REST API. Whether your preference is Python, JavaScript, Java, or tools like NodeRed, the ANPR API seamlessly integrates into your workflow.

> Note: In this guide, we'll be providing examples using Python.

To access the software, an API Key is essential for authorization. Obtain your key from the [Platform](https://platform.siinlab.com/active_products).

Once you have your API Key, the following Python code demonstrates how to use the ANPR API with this image:
<img src="https://siin.b-cdn.net/images/moroccan-license-plate.jpeg" height="300px">

```python
from os import getenv
from PIL import Image
import requests
import json

image_url = 'https://siin.b-cdn.net/images/moroccan-license-plate.jpeg'
api_url = "http://ai.siinlab.com/anpr/v1/detection/?model_type=anpr" # ?model_type=cars, ?model_type=license_plates, ?model_type=license_plates_characters
image_path = 'image.png'
api_key = getenv('SIIN_API_KEY') # export SIIN_API_KEY=xxxxx
assert api_key, 'Please set the API Key'

image = Image.open(requests.get(image_url, stream=True).raw)
image.save(image_path)

files = {'file': ('image.jpg', open(image_path, 'rb').read())}
payload = {"token": api_key}

response = requests.post(url=api_url, files=files, data=payload)
if response.status_code != 200:
    print('Error')

print(response.json())
```

The API response will return ANPR information in a JSON format:

```
[
  {
    "x1": 460.95635986328125,
    "y1": 297.60076904296875,
    "x2": 761.37451171875,
    "y2": 447.0316467285156,
    "score": 0.8074601888656616,
    "label": "6290أ44"
  }
]
```

The ANPR API exposes the following endpoints:

- GET `/status` - Check Status:  
By accessing this endpoint, users can check the status of the server. The server's status message is returned in a JSON format with a 200 status.

- POST `/v1/detection/` - Upload for detection:  
This endpoint is dedicated to uploading images for ANPR detection. The request is formatted as multipart/form-data, and successful detections return a JSON response. Validation errors are communicated with a 422 status.

- GET `/v1/detection/` - Python example:  
This endpoint now provides a Python example illustrating the proper utilization of the POST /v1/detection/ endpoint.

- POST `/v2/detection/` - Upload for detection:  
This endpoint replicates the functionality of the V1 version outlined previously, albeit with a revised input format. It mandates the input image to be presented as a byte array.

- GET `/v2/detection/` - Python example:  
This endpoint now provides a Python example illustrating the proper utilization of the POST /v2/detection/ endpoint.

Feel free to explore the functionality of both endpoints to seamlessly integrate ANPR capabilities into your applications and systems.

## API version
{{api-version}}

## ChangeLog
{{change-log}}
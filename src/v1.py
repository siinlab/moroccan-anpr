from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from typing import List


from engine_utils import ApiKeyException
from engine_utils.requests import api_key_is_valid

from os.path import join, abspath, dirname

from contextlib import asynccontextmanager

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse
from typing import List

from engine_utils import ApiKeyException
from config import BoxOutput
from utils import ModelType
from yolo_utils import process_detection_request

router = APIRouter(prefix='/v1')

@router.post("/detection/", response_model=List[BoxOutput])
async def upload(model_type: ModelType = ModelType.ANPR,
                token: str = Form(...),
                file: UploadFile = File(...)):
    """ Formatted as (x1, y1, x2, y2, encodings) """
    try:
        if not api_key_is_valid(token):
            raise ApiKeyException("Invalid API key")
        
        output = process_detection_request(model_type=model_type,
                                     file=file)
        return output
    except ApiKeyException as e:
        raise HTTPException(detail=str(e), status_code=401)
    except Exception as e:
        # Handle exceptions appropriately
        raise HTTPException(detail="An error occurred during processing.", status_code=500)
    
@router.get('/detection/', response_class=PlainTextResponse)
async def v1_example():
    return """
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
"""
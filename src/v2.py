from fastapi import HTTPException
from typing import List


from engine_utils.pydantic_models import Image, ApiKey, Status
from engine_utils.dependencies import validate_api_key, get_pil_image

from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse

from yolo_utils import process_detection_request
from utils import ModelType
from config import BoxOutput

router = APIRouter(prefix='/v2')


@router.post("/detection/", response_model=List[BoxOutput], response_model_exclude_none=True)
async def upload(model_type: ModelType = ModelType.ANPR,
                 api_key: ApiKey = Depends(validate_api_key),
                 image: Image = Depends(get_pil_image)):
    """ Formatted as (x1, y1, x2, y2, score, license plate number)
    """
    try:
        output = process_detection_request(model_type=model_type,
                                            image=image)
        return output
    except Exception as e:
        # Handle exceptions appropriately
        raise HTTPException(detail="An error occurred during processing.", status_code=500)
    
@router.get('/detection/', response_class=PlainTextResponse)
async def v2_example():
    return """
from os import getenv
from PIL import Image
import numpy as np
import requests

image_url = 'https://siin.b-cdn.net/images/moroccan-license-plate.jpeg'
api_url = "http://ai.siinlab.com/anpr/v1/detection/?model_type=anpr" # ?model_type=cars, ?model_type=license_plates, ?model_type=license_plates_characters
image_path = 'image.png'
api_key = getenv('SIIN_API_KEY') # export SIIN_API_KEY=xxxxx
assert api_key, 'Please set the API Key'

headers = {'x-api-key': api_key}

# Prepare input data
image = Image.open(requests.get(image_url, stream=True).raw).convert('RGB')
array = np.array(image).astype('uint8')
height, width, channels = array.shape
payload = {'image': array.tobytes().decode('latin1'), 'height': height, 'width': width, 'channels': channels}

response = requests.post(url=api_url, json=payload, headers=headers)
if response.status_code != 200:
    print(response.text)
    print('Error')
    exit(1)
    
# Read response
print(response.json())
"""
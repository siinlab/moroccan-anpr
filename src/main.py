from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse

from fastapi import FastAPI, HTTPException
from fastapi import File, UploadFile, Form
from lgg import logger
from os.path import abspath, dirname, join

from yolo_utils import process_detection_request
from utils import ModelType
from config import Status, BoxOutput

from engine_utils import load_api_keys, api_key_router, ApiKeyException, validate_api_key, html_documentation


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_api_keys('anpr')
        
    yield # this is where the rest of the app would go
    
    print('Shutting down ...')

app = FastAPI(lifespan=lifespan)
app.include_router(api_key_router)

@app.get('/')
async def get_documentation():
    html = html_documentation(join(abspath(dirname(__file__)), '..', 'Documentation.md'))
    return HTMLResponse(content=html)

@app.get("/status", response_model=Status)
async def check_status():
    """ Check the status of the server.
    Returns:
        str: A message indicating if the server is running.
    """
    return Status(status='ok')


@app.post("/detection/", response_model=list[BoxOutput])
async def upload(model_type: ModelType,
                 token: str = Form(...),
                 file: UploadFile = File(...),
                 ):
    """ Upload an image and detect cars in it.

    Args:
        token: A token to authenticate the user.
        file: The image to be uploaded.
    """
    if not validate_api_key(token):
        raise HTTPException(detail="Invalid API key", status_code=401)
    
    return process_detection_request(model_type=model_type,
                                     file=file)

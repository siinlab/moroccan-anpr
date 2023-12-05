from fastapi.responses import JSONResponse

from fastapi import FastAPI
from fastapi import File, UploadFile, Form
from lgg import logger

from yolo_utils import process_detection_request
from utils import ModelType
from config import Status, BoxOutput

app = FastAPI()


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
    return process_detection_request(model_type=model_type,
                                     token=token,
                                     file=file)

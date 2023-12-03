import traceback
from typing import List
from typing import Tuple, Union

import PIL
import numpy as np
from PIL import Image
from PIL import Image
from fastapi import File, UploadFile, Form, HTTPException
from lgg import logger
from ultralytics import YOLO

from config import CARS_MODEL_PATH, LP_MODEL_PATH, LPC_MODEL_PATH, BoxOutput
from utils import save_uploaded_image, ModelType
from engine_utils import validate_api_key

# Map latin characters to moroccan characters
__CHARACTERS_MAPPING = {
    '0': '0',
    '1': '1',
    '2': '2',
    '3': '3',
    '4': '4',
    '5': '5',
    '6': '6',
    '7': '7',
    '8': '8',
    '9': '9',

    'a': 'أ',
    'b': 'ب',
    'c': 'و',
    'd': 'د',
    'e': 'ه',
    'f': 'ض',
    'w': 'W',

}


def __predict(model_type: ModelType, input_source: Union[str, Image.Image]) -> Tuple[
    Image.Image, Tuple[List[np.array], List[dict]]]:
    """
    Predict the bounding boxes in an image.

    Args:
        model_type: The type of model to use.
        input_source: The source of the image to make predictions on. Can be a path to an image or a PIL.Image object.

    Returns:
        - img: A PIL.Image object containing the image with the bounding boxes
        - bboxes: A list of np.array containing the xyxysc bounding boxes (N, 6) per image
        - labels: A list of dictionary containing the labels names (N, C) per image
    """
    detection_functions = {
        ModelType.CARS: detect_cars,
        ModelType.LICENSE_PLATES: detect_lp,
        ModelType.LICENSE_PLATE_CHARACTERS: detect_lpc,
        ModelType.ANPR: anpr_detection,
    }

    detection_func = detection_functions.get(model_type)
    if detection_func:
        return detection_func(input_source)
    else:
        logger.error(f"Invalid model type: {model_type}")
        raise ValueError(f"Invalid model type: {model_type}")



def validate_token(token: str):
    if not validate_api_key(token):
        logger.error(f"Token `{token}` is invalid")
        raise HTTPException(status_code=498, detail="Invalid token")

def handle_json_response(bboxes: List[np.array], labels_map: List[dict]):
    logger.debug(f"Returning json response")
    bboxes = bboxes[0] # TODO: handle multiple images
    labels_map = labels_map[0]
    return [BoxOutput(x1=bbox[0], y1=bbox[1], x2=bbox[2], y2=bbox[3], score=bbox[4], label=labels_map[int(bbox[5])]) for bbox in bboxes]

def process_detection_request(model_type: ModelType,
                              token: str = Form(...),
                              file: UploadFile = File(...)):
    """ Process a detection request. """

    logger.info(f"Detecting `{model_type}` in {file.filename}...")

    validate_token(token)

    logger.debug(f"Loading model {model_type}")

    try:
        path = save_uploaded_image(file)
        logger.info(f"Successfully uploaded {file.filename}")

        bboxes, label_names = __predict(model_type=model_type, input_source=path)
        
        return handle_json_response(bboxes, label_names)
    except Exception as e:
        tb = traceback.format_exc()
        logger.error(f"There was an error uploading the file: {tb}")
        raise HTTPException(status_code=500, detail="There was an error running inference on the image")
    finally:
        file.file.close()


def anpr_detection(input_source: Union[str, Image.Image]) -> Tuple[
    Image.Image, Tuple[List[np.array], List[dict]]]:
    """ Detect cars in an image.

    Args:
        input_source: The source of the image to make predictions on. Can be a path to an image or a PIL.Image object.

    Returns:
        - img: A PIL.Image object containing the image with the bounding boxes
        - bboxes: A list of np.array containing the xyxysc bounding boxes (N, 6) per image
        - labels: A list of dictionary containing the labels names (N, C) per image
    """
    original_image = Image.open(input_source).convert("RGB")

    # detect one car
    car_index = 0  # TODO: get the car index from the labels json
    bboxes, labels = detect_cars(input_source)
    bboxes = bboxes[0]
    # check if array is empty
    if bboxes.size == 0:
        bboxes = np.array([0,0, original_image.width, original_image.height, 0.5, 0]).reshape(1, 6)
    bboxes = bboxes[bboxes[:, 5] == car_index]  # keep only the car
    
    # keep only the car with highest probability
    bboxes = bboxes[np.argmax(bboxes[:, 4])]
    clean_img = original_image
    clean_img = clean_img.crop(bboxes[0:4])
    car_bbox = bboxes[0:4]

    # detect one license plate
    bboxes, labels = detect_lp(clean_img)
    bboxes = bboxes[0]
    if bboxes.size == 0:
        logger.info("No license plates detected")
        return np.array([[]]), [{}]
    
    bboxes = bboxes[np.argmax(bboxes[:, 4])]
    clean_img = clean_img.crop(bboxes[0:4])
    lp_bbox = bboxes[0:4] + car_bbox[[0, 1, 0, 1]]
    score = bboxes[4]

    bboxes, labels = detect_lpc(clean_img)
    bboxes = bboxes[0]
    lp_string = convert_characters_to_string(bboxes, labels[0])

    return [np.array([[*lp_bbox.tolist(), score, 0]])], [{0: lp_string}]

def detect_cars(input_source: Union[str, PIL.Image.Image]) -> Tuple[
    PIL.Image.Image, Tuple[List[np.ndarray], List[dict]]]:
    """ Detect cars in an image.

    Args:
        input_source: The source of the image to make predictions on. Can be a path to an image or a PIL.Image object.

    Returns:
        - img: A PIL.Image object containing the image with the bounding boxes
        - bboxes: A list of np.array containing the xyxysc bounding boxes (N, 6) per image
        - labels: A list of dictionary containing the labels names (N, C) per image
    """
    return predict(CARS_MODEL_PATH, input_source)


def detect_lp(input_source: Union[str, PIL.Image.Image]) -> Tuple[PIL.Image.Image, Tuple[List[np.ndarray], List[dict]]]:
    """ Detect license plates in an image.

    Args:
        input_source: The source of the image to make predictions on. Can be a path to an image or a PIL.Image object.

    Returns:
        - img: A PIL.Image object containing the image with the bounding boxes
        - bboxes: A list of np.array containing the xyxysc bounding boxes (N, 6) per image
        - labels: A list of dictionary containing the labels names (N, C) per image
    """
    return predict(LP_MODEL_PATH, input_source)

def detect_lpc(input_source: Union[str, PIL.Image.Image]) -> Tuple[
    PIL.Image.Image, Tuple[List[np.ndarray], List[dict]]]:
    """ Detect license plate characters in an image.

    Args:
        input_source: The source of the image to make predictions on. Can be a path to an image or a PIL.Image object.

    Returns:
        - img: A PIL.Image object containing the image with the bounding boxes
        - bboxes: A list of np.array containing the xyxysc bounding boxes (N, 6) per image
        - labels: A list of dictionary containing the labels names (N, C) per image
    """
    return predict(LPC_MODEL_PATH, input_source)


def predict(model_path: str, input_source: Union[str, PIL.Image.Image]) -> \
        Tuple[PIL.Image.Image, Tuple[List[np.ndarray], List[dict]]]:
    """ Predict the bounding boxes in an image.

    Args:
        model_path: Path to the trained model
        input_source: The source of the image to make predictions on. Can be a path to an image or a PIL.Image object.

    Returns:
        + img: A PIL.Image object containing the image with the bounding boxes
        + (bboxes, label_names): A tuple containing the bounding boxes and the label names
    """

    bboxes, label_names = predict_bbox(model_path, input_source)
    return bboxes, label_names
 

def predict_bbox(model_path: str, input_source: Union[str, PIL.Image.Image]) -> Tuple[List[np.ndarray], List[dict]]:
    """ Predict the bounding boxes in an image.

    Args:
        model_path: Path to the trained model
        input_source: The source of the image to make predictions on. Can be a path to an image or a PIL.Image object.

    Returns:
        - bboxes: A list of np.array containing the xyxysc bounding boxes (N, 6) per image
        - labels: A list of dictionary containing the labels names (N, C) per image
    """
    model = YOLO(model_path)
    results = model(input_source)
    bboxes = [result.boxes.data.cpu().numpy() for result in results]
    labels = [result.names for result in results]
    return bboxes, labels

def convert_characters_to_string(bboxes: np.ndarray, label_names: dict):
    """ Convert the characters in the license plate to a string.

    Args:
        bboxes:
        label_names:

    Returns:
        lp_string: A string containing the characters in the license plate.
    """
    if len(bboxes) == 0:
        return ""
    # sort bboxes based on x value
    bboxes = bboxes[bboxes[:, 0].argsort()]
    # Convert class index to character
    lp_string = ""
    for bbox in bboxes:
        lp_string += __CHARACTERS_MAPPING[label_names[int(bbox[5])]]

    logger.debug(f"The detected license plate is `{lp_string}`")
    return lp_string
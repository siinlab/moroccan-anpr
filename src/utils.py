# src/utils.py

import os
from os.path import join, dirname
from pydantic import BaseModel
from typing import Union, List, Tuple
from enum import Enum

import numpy as np
import cv2
from PIL import Image
from ultralytics import YOLO
from fastapi import UploadFile

# Define the path where uploaded files will be saved
UPLOAD_FOLDER = "uploaded_images"

class ModelType(Enum):
    """Enum for the different types of models."""
    CARS = "cars"
    LICENSE_PLATES = "license_plates"
    LICENSE_PLATE_CHARACTERS = "license_plate_characters"
    ANPR = "anpr"

class BoxOutput(BaseModel):
    """A class to hold the output of the model."""
    x1: float
    y1: float
    x2: float
    y2: float
    score: float
    label: str

class Status(BaseModel):
    """A class to hold the status of the server."""
    status: str

# Define the models path
__MODELS_PATH = join(dirname(__file__), '..', 'models')

def __get_model_path(model_name: str) -> str:
    """Get the path to the model.

    Args:
        model_name (str): The name of the model.

    Returns:
        str: The path to the model.
    """
    return join(__MODELS_PATH, model_name, 'best.pt')

CARS_MODEL_PATH = __get_model_path('cars-model')
LP_MODEL_PATH = __get_model_path('lp-model')
LPC_MODEL_PATH = __get_model_path('ocr-model')

def save_uploaded_image(uploaded_file: UploadFile) -> str:
    """
    Save an uploaded image to the server.

    Args:
        uploaded_file (UploadFile): The uploaded image file.

    Returns:
        str: The path to the saved image.
    """
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    image_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
    with open(image_path, "wb") as f:
        f.write(uploaded_file.file.read())
    return image_path

def draw_bounding_boxes(image: np.ndarray, bboxes: List[np.ndarray], labels: dict, color=(0, 255, 0)) -> np.ndarray:
    """
    Draw bounding boxes on an image.

    Args:
        image (np.ndarray): The input image.
        bboxes (List[np.ndarray]): List of bounding boxes (each in the format [x1, y1, x2, y2, score, class_id]).
        labels (dict): Mapping from class_id to label.
        color (tuple): Color for the bounding box.

    Returns:
        np.ndarray: Image with bounding boxes drawn.
    """
    if not bboxes or len(bboxes[0]) == 0:
        print("No bounding boxes to draw.")
        return image

    for bbox in bboxes[0]:  # Iterate over bounding boxes
        if len(bbox) < 6:
            print(f"Invalid bounding box: {bbox}")
            continue  # Skip invalid boxes

        x1, y1, x2, y2, score, class_id = bbox
        x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
        label = f"{labels.get(int(class_id), 'N/A')}: {score:.2f}"
        image = cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        image = cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                            0.5, color, 1, cv2.LINE_AA)

    return image

def crop_bounding_box(image: np.ndarray, bbox: np.ndarray) -> np.ndarray:
    """
    Crop the region specified by the bounding box from the image.

    Args:
        image (np.ndarray): The input image.
        bbox (np.ndarray): Bounding box in the format (x1, y1, x2, y2, score, class_id).

    Returns:
        np.ndarray: Cropped image region.
    """
    x1, y1, x2, y2 = map(int, bbox[:4])
    return image[y1:y2, x1:x2]

def convert_characters_to_string(bboxes: np.ndarray, label_names: dict, characters_mapping: dict) -> str:
    """
    Convert detected characters from bounding boxes into a string.

    Args:
        bboxes (np.ndarray): Array of bounding boxes with character class IDs.
        label_names (dict): Mapping from class ID to label.
        characters_mapping (dict): Mapping from detected class to desired character.

    Returns:
        str: String representing the detected license plate.
    """
    # Sort bounding boxes by their x1-coordinate for left-to-right reading
    if len(bboxes) == 0:
        print("No characters to convert.")
        return ""
    
    bboxes = bboxes[bboxes[:, 0].argsort()]  # Sort by x-coordinate
    print(f"Sorted OCR bounding boxes: {bboxes}")

    lp_string = ""

    for bbox in bboxes:
        class_id = int(bbox[5])
        character = characters_mapping.get(class_id, "")
        
        # Append character to the license plate string
        lp_string += character  # Directly append the character

    # At this point, all characters are appended; handle special placements if needed
    print(f"Final License Plate String: {lp_string}")
    return lp_string


# Define the characters mapping with integer keys
CHARACTERS_MAPPING = {
    0: '0',
    1: '1',
    2: '2',
    3: '3',
    4: '4',
    5: '5',
    6: '6',
    7: '7',
    8: '8',
    9: '9',
    10: 'أ',
    11: 'ب',
    12: 'و',
    13: 'د',
    14: 'ه',
    15: 'ض',
    16: 'W',
}

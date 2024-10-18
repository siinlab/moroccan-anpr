# anpr_app.py

import streamlit as st
import numpy as np
from PIL import Image
from ultralytics import YOLO
import traceback

from src.utils import (
    draw_bounding_boxes,
    crop_bounding_box,
    convert_characters_to_string,
    CHARACTERS_MAPPING
)
from src.config import CARS_MODEL_PATH, LP_MODEL_PATH, LPC_MODEL_PATH

# Set Streamlit page configuration
st.set_page_config(
    page_title="Moroccan ANPR System",
    layout="centered",
    initial_sidebar_state="auto"
)

# Load models with caching for performance
@st.cache_resource
def load_models():
    """Load YOLO models for car detection, license plate detection, and OCR."""
    car_detector = YOLO(CARS_MODEL_PATH)      # Car detector
    lp_detector = YOLO(LP_MODEL_PATH)         # License plate detector
    ocr_detector = YOLO(LPC_MODEL_PATH)       # OCR model for characters
    return car_detector, lp_detector, ocr_detector

car_detector, lp_detector, ocr_detector = load_models()

# App Title
st.title("Moroccan ANPR System")

# File Uploader
uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

def display_detected_bboxes(image: Image.Image, bboxes: list, labels: dict, title: str):
    """
    Display an image with bounding boxes using Streamlit.

    Parameters:
    - image (PIL.Image): The image to display.
    - bboxes (list): List of bounding boxes.
    - labels (dict): Mapping of class IDs to label names.
    - title (str): Title for the image.
    """
    image_np = np.array(image)

    if not bboxes or len(bboxes[0]) == 0:
        st.write(f"No {title.lower()} detected.")
        st.image(image, caption=f"No {title} found.", use_column_width=True, width=300)
        return

    # Draw bounding boxes on the image
    image_with_boxes = draw_bounding_boxes(image_np, bboxes, labels, color=(0, 255, 0))
    st.image(image_with_boxes, caption=title, use_column_width=True, width=300)

if uploaded_file:
    # Load and display the uploaded image
    try:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded Image", use_column_width=True, width=300)
    except Exception as e:
        st.error(f"Failed to load image: {e}")
        st.stop()

    st.write("Running end-to-end ANPR...")
    try:
        # Detect cars in the image
        car_results = car_detector(image)
        car_bboxes = [result.boxes.data.cpu().numpy() for result in car_results]
        car_labels = car_detector.names

        if len(car_bboxes[0]) == 0:
            st.write("No cars detected.")
        else:
            # Process each detected car
            for i, car_bbox in enumerate(car_bboxes[0]):
                if len(car_bbox) < 6:
                    st.write(f"Invalid car bounding box: {car_bbox}")
                    continue

                x1, y1, x2, y2, score, class_id = car_bbox
                cropped_car = image.crop((int(x1), int(y1), int(x2), int(y2)))

                # Detect license plates within the cropped car image
                lp_results = lp_detector(cropped_car)
                lp_bboxes = [result.boxes.data.cpu().numpy() for result in lp_results]
                lp_labels = lp_detector.names

                if len(lp_bboxes[0]) == 0:
                    st.write(f"No license plates detected in Car {i + 1}.")
                    continue

                # Process each detected license plate
                for j, lp_bbox in enumerate(lp_bboxes[0]):
                    if len(lp_bbox) < 6:
                        st.write(f"Invalid license plate bounding box: {lp_bbox}")
                        continue

                    x1_lp, y1_lp, x2_lp, y2_lp, score_lp, class_id_lp = lp_bbox
                    cropped_lp = cropped_car.crop((int(x1_lp), int(y1_lp), int(x2_lp), int(y2_lp)))
                    st.image(cropped_lp, caption=f"Cropped License Plate {j + 1} in Car {i + 1}", use_column_width=True, width=300)

                    # Detect characters using OCR model
                    ocr_results = ocr_detector(cropped_lp)
                    ocr_bboxes = [result.boxes.data.cpu().numpy() for result in ocr_results]
                    ocr_labels = ocr_detector.names

                    if len(ocr_bboxes[0]) == 0:
                        st.write("No characters detected.")
                    else:
                        # Sort characters left-to-right based on x1 coordinate
                        ocr_bboxes_sorted = ocr_bboxes[0][ocr_bboxes[0][:, 0].argsort()]

                        # Convert detected characters to string
                        lp_string = convert_characters_to_string(
                            ocr_bboxes_sorted, 
                            ocr_detector.names, 
                            CHARACTERS_MAPPING
                        )

                        # Display the recognized license plate string
                        st.markdown(f"""
                            <div style='text-align: center; direction: rtl;'>
                                <h3 style='color: black;'>License Plate :</h3>
                                <h3 style='color: black;'>{lp_string}</h3>
                            </div>
                            """, unsafe_allow_html=True)    

                        # Optionally display cropped license plate with character bounding boxes
                        display_detected_bboxes(
                            cropped_lp,
                            ocr_bboxes,
                            ocr_labels,
                            "Detected Characters"
                        )

    except Exception as e:
        st.error(f"Error during processing:\n{traceback.format_exc()}")

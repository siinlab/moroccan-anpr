# Moroccan ANPR System

This project is an Automatic Number Plate Recognition (ANPR) system tailored for Moroccan license plates. It leverages **YOLO models** for detecting cars, license plates, and individual characters, integrated with **Streamlit** for a user-friendly web interface.

---

## 📑 Project Structure

```bash
MOROCCAN_ANPR_SYSTEM/
│
├── models/
│   ├── cars-model/  # YOLO model for car detection
│   │   └── best.pt
│   ├── lp-model/    # YOLO model for license plate detection
│   │   └── best.pt
│   └── ocr-model/   # YOLO model for OCR (character recognition)
│       └── best.pt
│
├── src/             # Source code for utility functions and configurations
│   ├── config.py
│   └── utils.py
│
├── anpr_app.py      # Streamlit app for end-to-end ANPR
├── requirements.txt # Python dependencies
├── Dockerfile       # Docker configuration file
├── .gitignore       # Files and directories to ignore in Git
└── README.md        # Project documentation (this file)
```
## 🚀 How to Run the Application

### 1. Clone the Repository
Open a terminal and run the following command:

```bash
git clone https://github.com/siinlab/moroccan-anpr.git
cd MOROCCAN_ANPR_SYSTEM
```
### 2. Install Dependencies
Make sure you have `Python 3.9+` installed. Install the required dependencies:

```bash
pip install -r requirements.txt
```
### 3. Run the Application
Use the following command to run the Streamlit application:

```bash
streamlit run anpr_app.py
```
Open your browser and go to:

```bash
http://localhost:8501
```
## 🐳 Using Docker
### 1. Build the Docker Image
Ensure Docker is installed and running on your system. Build the Docker image with:

```bash
docker build -t moroccan-anpr-app .
```
### 2. Run the Docker Container
Run the container and expose the app on port 8501:

```bash
docker run -p 8501:8501 moroccan-anpr-app
```
### 3. Access the Application
Open your browser and navigate to:

```bash
http://localhost:8501
```
## 📋 Features
- **Car Detection**: Detects cars in uploaded images.
- **License Plate Detection**: Detects Moroccan license plates on cars.
- **OCR**: Recognizes characters from detected license plates and converts them into readable text.
- **End-to-End Flow**: Processes an image to detect cars, extract license plates, and display the recognized text.

## ⚙️ Configuration
### YOLO Models:
- **Car Detection Model**: `models/cars-model/best.pt`
- **License Plate Detection Model**: `models/lp-model/best.pt`
- **OCR Model**: `models/ocr-model/best.pt`
### Configuration File:
- `src/config.py` contains paths to the models and other configurations.

## 🛠️ Tech Stack
- **Python 3.9+**: Programming language for backend development.
- **Streamlit**: Web-based UI framework for creating the application interface.
- **YOLO (Ultralytics)**: Object detection models used for detecting cars, license plates, and characters.
- **Pillow**: Image processing library for handling and manipulating images.
- **Docker**: Containerization platform to package the application for deployment.


## 📄 License
This project is licensed under the MIT License.

## ✨ Contributing
- Fork the repository.
- Create a new branch (git checkout -b feature-branch).
- Make your changes and commit them (git commit -m 'Add feature').
- Push the branch (git push origin feature-branch).
- Open a Pull Request.

## 🧑‍💻 Authors
Your Name

## 📞 Contact
If you have any questions or issues, feel free to reach out at:

Email: ayoub@siinlab.com


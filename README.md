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

## 🚀 How to Run the Application

1. Clone the Repository
Open a terminal and run the following command:

```bash
Copy code
git clone <your-repository-url>
cd MOROCCAN_ANPR_SYSTEM
```

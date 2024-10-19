# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose the port that Streamlit will run on
EXPOSE 8501

# Set environment variables to avoid Streamlit's interactive prompts
ENV STREAMLIT_SERVER_HEADLESS true
ENV STREAMLIT_SERVER_PORT 8501
ENV STREAMLIT_SERVER_ENABLE_CORS false

# Command to run the Streamlit app
CMD ["streamlit", "run", "anpr_app.py"]

from flask import Flask, render_template, request, send_from_directory
import os
from rembg import remove
from PIL import Image
import cv2
import numpy as np

app = Flask(__name__)

# Folder to save processed files
UPLOAD_FOLDER = './static/uploads'
OUTPUT_FOLDER = './static/outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    
    # Remove background from image
    if file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        output_path = os.path.join(OUTPUT_FOLDER, f"processed_{file.filename}")
        process_image(filepath, output_path)
    elif file.filename.lower().endswith(('.mp4', '.avi')):
        output_path = os.path.join(OUTPUT_FOLDER, f"processed_{file.filename}")
        process_video(filepath, output_path)
    else:
        return "Unsupported file format", 400

    return send_from_directory(OUTPUT_FOLDER, f"processed_{file.filename}", as_attachment=True)

def process_image(input_path, output_path):
    with open(input_path, 'rb') as input_file:
        input_data = input_file.read()
        output_data = remove(input_data)
        with open(output_path, 'wb') as output_file:
            output_file.write(output_data)

def process_video(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (640, 480))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Example: Replace with actual background removal code for each frame
        # For now, we are just writing the same frames as output.
        out.write(frame)

    cap.release()
    out.release()

if __name__ == "__main__":
    app.run(debug=True)

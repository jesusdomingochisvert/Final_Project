# import os
# import requests
# from flask import Flask, request, jsonify, send_from_directory, render_template

# app = Flask(__name__)

# IA_SERVICE_URL = "http://ia_container:5001/process_images"
# INPUT_IMAGES_DIR = os.path.join(os.getcwd(), 'shared', 'entrada')
# PROCESSED_IMAGES_DIR = os.path.join(os.getcwd(), 'shared', 'salida')
# for directory in [INPUT_IMAGES_DIR, PROCESSED_IMAGES_DIR]:
#     if not os.path.exists(directory):
#         os.makedirs(directory)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/api/process_images', methods=['POST'])
# def process_image():
#     if 'image' not in request.files:
#         return "No image provided", 400

#     image_file = request.files['image']
#     image_path = os.path.join(INPUT_IMAGES_DIR, image_file.filename)
#     image_file.save(image_path)

#     if not os.path.exists(image_path):
#         return "Image not saved correctly", 500

#     response = requests.post(IA_SERVICE_URL, json={"image_path": image_path})

#     if response.status_code != 200:
#         return jsonify({'error': 'Failed to process image', 'details': response.text}), response.status_code

#     data = response.json()
#     processed_image_path = data.get('processed_image_path')
#     relative_path = os.path.relpath(processed_image_path, PROCESSED_IMAGES_DIR)

#     return jsonify({'processed_image_path': f'/uploads/{relative_path}'}), 200

# @app.route('/uploads/<path:filename>')
# def download_file(filename):
#     return send_from_directory(PROCESSED_IMAGES_DIR, filename)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)

import os
import requests
from flask import Flask, request, jsonify, send_from_directory, render_template

app = Flask(__name__)

IA_SERVICE_URL = "http://ia_container:5001/process_images"
INPUT_IMAGES_DIR = os.path.join(os.getcwd(), 'shared', 'entrada')
PROCESSED_IMAGES_DIR = os.path.join(os.getcwd(), 'shared', 'salida')
for directory in [INPUT_IMAGES_DIR, PROCESSED_IMAGES_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/process_images', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return "No image provided", 400

    image_file = request.files['image']
    image_path = os.path.join(INPUT_IMAGES_DIR, image_file.filename)
    image_file.save(image_path)

    if not os.path.exists(image_path):
        return "Image not saved correctly", 500

    response = requests.post(IA_SERVICE_URL, json={"image_path": image_path})

    if response.status_code != 200:
        return jsonify({'error': 'Failed to process image', 'details': response.text}), response.status_code

    data = response.json()
    processed_image_path = data.get('processed_image_path')
    relative_path = os.path.relpath(processed_image_path, PROCESSED_IMAGES_DIR)

    return jsonify({'processed_image_path': f'/uploads/{relative_path}'}), 200

@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(PROCESSED_IMAGES_DIR, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

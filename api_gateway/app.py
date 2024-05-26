import os

import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

IA_SERVICE_URL = "http://ia_container:5001/process_images"


@app.route('/api/process_images', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return "No image provided", 400

    image_file = request.files['image']
    image_path = os.path.join('./shared', image_file.filename)
    image_file.save(image_path)

    if not os.path.exists(image_path):
        return "Image not saved correctly", 500

    #response = requests.post(IA_SERVICE_URL, files={'image': (image_file.filename, image_file.read(), image_file.content_type)})
    response = requests.post(IA_SERVICE_URL, json={"image_path": image_path})

    if response.status_code != 200:
        return jsonify({'error': 'Failed to process image', 'details': response.text}), response.status_code

    return jsonify(response.json()), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

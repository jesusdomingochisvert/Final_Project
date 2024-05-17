from flask import Flask, request, jsonify
from io import BytesIO

import os
import subprocess

app = Flask(__name__)

IA_SERVICE_URL = "http://ia_container:5001/process_image"


@app.route('/api/process_images', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return "No image provided", 400

    image_file = request.files['image']
    image_path = 'temp_image.jpg'
    image_file.save(image_path)

    result = subprocess.run(['docker', 'exec', 'ia_container', 'python', 'PxCaraRandom.py', image_path], capture_output=True)

    if result.returncode != 0:
        return jsonify({'error': result.stderr}), 500

    output = result.stdout.decode('utf-8').strip()

    return jsonify({'result': output}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

import os
import cv2
from ultralytics import YOLO
from keras.saving import load_model
from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np

app = Flask(__name__)

# Ruta del volumen compartido para guardar las imágenes procesadas
PROCESSED_IMAGES_DIR = './shared/processed_images'
if not os.path.exists(PROCESSED_IMAGES_DIR):
    os.makedirs(PROCESSED_IMAGES_DIR)

def load_face_detection_model():
    return YOLO("./shared/yolov8n-face.pt")

def detect_faces(image_path, model_face_detection):
    results = model_face_detection(image_path)
    return results[0].boxes

def read_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Image at path {image_path} could not be found or read.")
    return img

def resize_face(face, size=(200, 200)):
    return cv2.resize(face, size) if face.shape[:2] != size else face

def pixelate_face(face, pixel_percentage=0.3):
    pixel_size = max(1, int(min(face.shape[:2]) * pixel_percentage))
    small = cv2.resize(face, (face.shape[1] // pixel_size, face.shape[0] // pixel_size), interpolation=cv2.INTER_LINEAR)
    return cv2.resize(small, face.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)

def preprocess_face_for_model(face):
    face = cv2.resize(face, (200, 200))
    face = np.expand_dims(face, axis=0)
    return face

def process_faces(img, boxes, age_model):
    resized_faces = []
    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        face = img[y1:y2, x1:x2]
        face = resize_face(face)
        resized_faces.append(face)
    
    for i, face in enumerate(resized_faces):
        face_resized = preprocess_face_for_model(face)
        is_minor = age_model.predict(face_resized)[0][0] > 0.5
        if is_minor:
            resized_faces[i] = pixelate_face(face)
    
    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        resized_face = cv2.resize(resized_faces[i], (x2 - x1, y2 - y1))
        img[y1:y2, x1:x2] = resized_face

    return img

def process_image_with_face_detection_and_age_classification(image_path, age_model):
    model_face_detection = load_face_detection_model()
    boxes = detect_faces(image_path, model_face_detection)
    img = read_image(image_path)
    return process_faces(img, boxes, age_model)

@app.route('/process_images', methods=['POST'])
def process_image():
    data = request.get_json()
    image_path = data.get('image_path')

    if not image_path or not os.path.exists(image_path):
        return jsonify({'error': 'La imagen no existe o no se proporcionó image_path'}), 400

    age_model = load_model('./modelos/modelo_mnet.keras')

    try:
        processed_image = process_image_with_face_detection_and_age_classification(image_path, age_model)
        processed_image_name = os.path.basename(image_path).rsplit('.', 1)[0] + '_processed.jpg'
        processed_image_path = os.path.join(PROCESSED_IMAGES_DIR, processed_image_name)
        cv2.imwrite(processed_image_path, processed_image)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'processed_image_path': processed_image_path}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
import os
import cv2
from ultralytics import YOLO
from keras.saving import load_model
from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)

# Rutas de los directorios de entrada y salida
INPUT_IMAGES_DIR = './shared/entrada'
PROCESSED_IMAGES_DIR = './shared/salida'
for directory in [INPUT_IMAGES_DIR, PROCESSED_IMAGES_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

def load_face_detection_model():
    return YOLO("./shared/yolov8n-face.pt")

def detect_faces(image_path, model_face_detection):
    results = model_face_detection(image_path)
    return results[0].boxes

def read_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Imagen en ruta {image_path} no ha sido encontrada / no se ha podido leer.")
    return img

def resize_face(face, size=(200, 200)):
    return cv2.resize(face, size) if face.shape[:2] != size else face

def pixelate_face(face, pixel_percentage=0.15):
    pixel_size = max(1, int(min(face.shape[:2]) * pixel_percentage))
    small = cv2.resize(face, (face.shape[1] // pixel_size, face.shape[0] // pixel_size), interpolation=cv2.INTER_LINEAR)
    return cv2.resize(small, face.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)

def expand_box(box, img_width, img_height, expansion_factor=1.3):
    # Calcula el nuevo tamaño de la caja expandiéndola por el factor dado
    width = box[2] - box[0]
    height = box[3] - box[1]
    new_width = width * expansion_factor
    new_height = height * expansion_factor
    
    # Calcula las nuevas coordenadas de la caja, asegurándose de que no se salga de los límites de la imagen
    x1 = max(0, int(box[0] - (new_width - width) / 2))
    y1 = max(0, int(box[1] - (new_height - height) / 2))
    x2 = min(img_width, int(box[2] + (new_width - width) / 2))
    y2 = min(img_height, int(box[3] + (new_height - height) / 2))
    
    return [x1, y1, x2, y2]

def process_faces(img, boxes, age_model):
    img_height, img_width = img.shape[:2]
    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        expanded_box = expand_box([x1, y1, x2, y2], img_width, img_height)
        x1, y1, x2, y2 = expanded_box
        face = img[y1:y2, x1:x2]
        face = resize_face(face)

        face_resized = np.expand_dims(face, axis=0)
        is_minor = age_model.predict(face_resized)[0][0] > 0.5
        if is_minor:
            pixelated_face = pixelate_face(face)
            img[y1:y2, x1:x2] = cv2.resize(pixelated_face, (x2 - x1, y2 - y1))

    return img

def process_image_with_face_detection_and_age_classification(image_path, age_model):
    model_face_detection = load_face_detection_model()
    boxes = detect_faces(image_path, model_face_detection)
    img = read_image(image_path)
    return process_faces(img, boxes, age_model)

@app.route('/process_images', methods=['POST'])
def process_image():
    data = request.get_json()
    image_path = data['image_path']

    if not os.path.exists(image_path):
        return jsonify({'error': 'La imagen no existe o no se proporcionó image_path'}), 400

    age_model = load_model('./modelos/modelo_mnet.keras')

    try:
        processed_image = process_image_with_face_detection_and_age_classification(image_path, age_model)
        processed_image_name = os.path.basename(image_path).rsplit('.', 1)[0] + '_procesado.jpg'
        processed_image_path = os.path.join(PROCESSED_IMAGES_DIR, processed_image_name)
        cv2.imwrite(processed_image_path, processed_image)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'processed_image_path': processed_image_path}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
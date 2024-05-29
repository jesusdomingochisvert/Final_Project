import os
import cv2
import time
from ultralytics import YOLO
from keras.saving import load_model
from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)

# Declarar modelos
model_face_detection = YOLO("./shared/yolov8n-face.pt")
age_model = load_model('./modelos/modelo_mnet.keras')

# Rutas de los directorios de entrada y salida
INPUT_IMAGES_DIR = './shared/entrada'
PROCESSED_IMAGES_DIR = './shared/salida'
for directory in [INPUT_IMAGES_DIR, PROCESSED_IMAGES_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

def detect_faces(image_path):
    results = model_face_detection(image_path)
    return results[0].boxes

def read_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Imagen en ruta {image_path} no ha sido encontrada / no se ha podido leer.")
    return img

def resize_face(face, size=(200, 200)):
    return cv2.resize(face, size) if face.shape[:2] != size else face

def pixelate_face(face, pixel_percentage=0.1):
    pixel_size = max(1, int(min(face.shape[:2]) * pixel_percentage))
    small = cv2.resize(face, (face.shape[1] // pixel_size, face.shape[0] // pixel_size), interpolation=cv2.INTER_LINEAR)
    return cv2.resize(small, face.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)

def cuadrar_extender_area_cara(img, top_left_x, top_left_y, bottom_right_x, bottom_right_y, extension_percentage):
    ancho = bottom_right_x - top_left_x
    largo = bottom_right_y - top_left_y
    max_side = max(ancho, largo)
    center_x = top_left_x + ancho // 2
    center_y = top_left_y + largo // 2

    extended_side = int(max_side * (1 + extension_percentage))
    new_top_left_x = max(0, center_x - extended_side // 2)
    new_top_left_y = max(0, center_y - extended_side // 2)
    new_bottom_right_x = min(img.shape[1], center_x + extended_side // 2)
    new_bottom_right_y = min(img.shape[0], center_y + extended_side // 2)

    return new_top_left_x, new_top_left_y, new_bottom_right_x, new_bottom_right_y

def draw_prediction_text(face, prediction):
    text = f"{prediction:.2f}"
    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)[0]
    text_x = (face.shape[1] - text_size[0]) // 2
    text_y = (face.shape[0] + text_size[1]) // 2
    cv2.putText(face, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
    return face

def process_faces(img, boxes, age_model, extension_percentage=0.26):
    resized_faces = []
    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        new_top_left_x, new_top_left_y, new_bottom_right_x, new_bottom_right_y = cuadrar_extender_area_cara(
            img, x1, y1, x2, y2, extension_percentage)

        face = img[new_top_left_y:new_bottom_right_y, new_top_left_x:new_bottom_right_x]
        face = resize_face(face)
        resized_faces.append((face, (new_top_left_x, new_top_left_y, new_bottom_right_x, new_bottom_right_y)))

    for i, (face, (new_top_left_x, new_top_left_y, new_bottom_right_x, new_bottom_right_y)) in enumerate(resized_faces):
        face_resized = np.expand_dims(face, axis=0)
        prediction = age_model.predict(face_resized)[0][0]
        is_minor = prediction > 0.4

        if is_minor:
            face = pixelate_face(face)
        else:
            cv2.rectangle(face, (0, 0), (199, 199), (0, 255, 0), 2) # que hace esto (el '2' del final)?????????

        face = draw_prediction_text(face, prediction)
        resized_faces[i] = (face, (new_top_left_x, new_top_left_y, new_bottom_right_x, new_bottom_right_y))

    for i, (face, (new_top_left_x, new_top_left_y, new_bottom_right_x, new_bottom_right_y)) in enumerate(resized_faces):
        resized_face = cv2.resize(face, (new_bottom_right_x - new_top_left_x, new_bottom_right_y - new_top_left_y))
        img[new_top_left_y:new_bottom_right_y, new_top_left_x:new_bottom_right_x] = resized_face

    return img

def process_image_with_face_detection_and_age_classification(image_path, age_model):
    start_time = time.time()
    boxes = detect_faces(image_path)
    img = read_image(image_path)
    img = process_faces(img, boxes, age_model)
    end_time = time.time()
    total_time = end_time - start_time
    print(f'Tiempo ejecucion: {total_time}') # -> en proceso de desarollo
    return img, total_time

@app.route('/process_images', methods=['POST'])
def process_image():
    data = request.get_json()
    image_path = data['image_path']

    if not os.path.exists(image_path):
        return jsonify({'error': 'La imagen no existe o no se proporciono image_path'}), 400

    try:
        processed_image, total_time = process_image_with_face_detection_and_age_classification(image_path, age_model)
        processed_image_name = os.path.basename(image_path).rsplit('.', 1)[0] + '_procesado.jpg'
        processed_image_path = os.path.join(PROCESSED_IMAGES_DIR, processed_image_name)
        cv2.imwrite(processed_image_path, processed_image)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'processed_image_path': processed_image_path, 'total_time': total_time}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
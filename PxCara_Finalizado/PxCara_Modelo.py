import io
import os

import cv2
from PIL import Image
from ultralytics import YOLO
from keras.saving import load_model
import tensorflow as tf
from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)


def process_image_with_face_detection_and_age_classification(image_path, age_model):
    # Cargar el modelo YOLOv8 para detección de caras
    model_face_detection = YOLO("./shared/yolov8n-face.pt")

    # Realizar la detección de caras en la imagen
    results = model_face_detection(image_path)
    boxes = results[0].boxes

    # Leer la imagen original
    img_original = cv2.imread(image_path)

    # Lista para almacenar las imágenes de caras redimensionadas
    resized_faces = []
    
    # Iterar sobre las caras detectadas
    for i, box in enumerate(boxes):
        top_left_x = int(box.xyxy.tolist()[0][0])
        top_left_y = int(box.xyxy.tolist()[0][1])
        bottom_right_x = int(box.xyxy.tolist()[0][2])
        bottom_right_y = int(box.xyxy.tolist()[0][3])

        # Recortar la cara de la imagen
        face = img_original[top_left_y:bottom_right_y, top_left_x:bottom_right_x]

        # Redimensionar la cara a 200x200 si no lo es
        if face.shape[0] != 200 or face.shape[1] != 200:
            face = cv2.resize(face, (200, 200))

        # Guardar la cara redimensionada en la lista
        resized_faces.append(face)
    
    # Clasificar la edad para cada cara redimensionada
    for face in resized_faces:
        # Redimensionar la imagen para que coincida con el formato del modelo (1, 200, 200, 3)
        face_resized = tf.expand_dims(tf.cast(face, tf.float32) / 255., axis=0)

        # Predecir la edad con el modelo
        is_minor = age_model.predict(face_resized)[0][0] > 0.5  # Suponemos que si la probabilidad es mayor a 0.5 es menor de edad

        # Si la cara se clasifica como menor de edad, aplicar pixelado
        if is_minor:
            # Definir el porcentaje de la resolución de la imagen que será el tamaño de los píxeles
            pixel_percentage = 0.1  # 1%

            # Calcular el tamaño de los píxeles en función de la resolución de la imagen
            pixel_size = max(1, int(min(face.shape[0], face.shape[1]) * pixel_percentage))

            # Reducir la resolución de la imagen
            small = cv2.resize(face, (face.shape[1] // pixel_size, face.shape[0] // pixel_size), interpolation=cv2.INTER_LINEAR)

            # Aumentar la resolución de la imagen a su tamaño original
            pixelated = cv2.resize(small, (face.shape[1], face.shape[0]), interpolation=cv2.INTER_NEAREST)

            # Actualizar la cara redimensionada con el pixelado
            face[:] = pixelated

    # Redimensionar las caras pixeladas a sus dimensiones originales y colocarlas en la imagen procesada
    for i, box in enumerate(boxes):
        top_left_x = int(box.xyxy.tolist()[0][0])
        top_left_y = int(box.xyxy.tolist()[0][1])
        bottom_right_x = int(box.xyxy.tolist()[0][2])
        bottom_right_y = int(box.xyxy.tolist()[0][3])

        # Redimensionar la cara a su tamaño original
        resized_face = cv2.resize(resized_faces[i], (bottom_right_x - top_left_x, bottom_right_y - top_left_y))

        # Reasignar la cara redimensionada a su posición original en la imagen
        img_original[top_left_y:bottom_right_y, top_left_x:bottom_right_x] = resized_face

    # Devolver la imagen original con las caras procesadas reasignadas
    return img_original


@app.route('/process_images', methods=['POST'])
def process_image():
    #image_file = request.files['image']
    #img = cv2.imdecode(np.frombuffer(image_file.read(), dtype=np.uint8), cv2.IMREAD_COLOR)

    data = request.get_json()
    print(data)

    image_path = data['image_path']
    print(image_path)

    img = cv2.imread(image_path)

    if img is None:
        return jsonify({'error': 'No se pudo leer la imagen'}), 400

    model = './modelos/modelo_mnet.keras'
    age_model = load_model(model)

    processed_image = process_image_with_face_detection_and_age_classification(img, age_model)

    return jsonify(processed_image), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

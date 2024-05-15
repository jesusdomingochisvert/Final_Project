import cv2
from ultralytics import YOLO
import random

def process_image_with_face_detection_and_age_simulation(image_path):
    # Cargar el modelo YOLOv8 para detección de caras
    model_face_detection = YOLO("yolov8n-face.pt")
    
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
    
    # Simular la clasificación de edad para cada cara redimensionada
    for face in resized_faces:
        
        # Simular la clasificación de edad (50% de probabilidad de ser clasificado como menor)
        is_minor = random.choice([True, False])

        # Si la cara se clasifica como menor de edad, aplicar pixelado
        if is_minor:
            # Definir el porcentaje de la resolución de la imagen que será el tamaño de los píxeles
            pixel_percentage = 0.15  # 1%

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

# Ejemplo de uso de la función
image_path = 'imagenes_prueba/meeting-business-leaders.jpg'
processed_image = process_image_with_face_detection_and_age_simulation(image_path)

# Guardar la imagen procesada
cv2.imwrite("imagen_resultado/imagen_procesada.jpg", processed_image)

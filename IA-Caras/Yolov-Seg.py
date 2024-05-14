import ultralytics
import cv2
from ultralytics import YOLO
import os
import glob

ultralytics.checks()


-----------------------------------------------------------------------------------------------------------------


model = YOLO("yolov8n-face.pt")

img_path = 'imagenes_prueba\meeting-business-leaders.jpg'
results = model(img_path)
boxes = results[0].boxes

img = cv2.imread(img_path)

# Crear la carpeta 'imagenes_recortadas' si no existe
if not os.path.exists('imagenes_recortadas'):
    os.makedirs('imagenes_recortadas')

for i, box in enumerate(boxes):
    top_left_x = int(box.xyxy.tolist()[0][0])
    top_left_y = int(box.xyxy.tolist()[0][1])
    bottom_right_x = int(box.xyxy.tolist()[0][2])
    bottom_right_y = int(box.xyxy.tolist()[0][3])

    # Recortar la cara de la imagen
    face = img[top_left_y:bottom_right_y, top_left_x:bottom_right_x]

    # Guardar la cara recortada como una imagen individual
    cv2.imwrite(f"imagenes_recortadas\cara_{i}.jpg", face)


-------------------------------------------------------------------------------------------------------------------


# Definir el porcentaje de la resolución de la imagen que será el tamaño de los píxeles
pixel_percentage = 0.1  # 1%

# Obtener todas las imágenes en la carpeta 'imagenes_recortadas'
image_paths = glob.glob('imagenes_recortadas\*.jpg')

# Leer la imagen original
img_original = cv2.imread("imagenes_prueba\meeting-business-leaders.jpg")

for i, image_path in enumerate(image_paths):
    # Leer la imagen
    img = cv2.imread(image_path)

    # Calcular el tamaño de los píxeles en función de la resolución de la imagen
    pixel_size = max(1, int(min(img.shape[0], img.shape[1]) * pixel_percentage))

    # Reducir la resolución de la imagen
    small = cv2.resize(img, (img.shape[1] // pixel_size, img.shape[0] // pixel_size), interpolation=cv2.INTER_LINEAR)

    # Aumentar la resolución de la imagen a su tamaño original
    pixelated = cv2.resize(small, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_NEAREST)

    # Guardar la imagen pixelada
    cv2.imwrite(f"imagenes_recortadas\rostro_pixelado_{i}.jpg", pixelated)

    # Reasignar el rostro pixelado a su posición original en la imagen
    top_left_x = int(boxes[i].xyxy.tolist()[0][0])
    top_left_y = int(boxes[i].xyxy.tolist()[0][1])
    bottom_right_x = int(boxes[i].xyxy.tolist()[0][2])
    bottom_right_y = int(boxes[i].xyxy.tolist()[0][3])

    img_original[top_left_y:bottom_right_y, top_left_x:bottom_right_x] = pixelated

# Guardar la imagen original con los rostros pixelados reasignados
cv2.imwrite("imagen_resultado\imagen_procesada.jpg", img_original)




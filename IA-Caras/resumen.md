Directorio relativo a pruebas de la IA para la detección de rostros YolovFacev8.

* Se importa del modelo "yolov8n-face.pt".
* Se le pasa el path de la imagen deseada.
* Se preparan los delimitadores para el rostro detectado.
* Se guardan las caras de la imagen en base a los delimitadores.
* Se guarda una imagen con los marcos de los rostros detectados.

Futuras acciones:
* Pixelar/Tapar los rostros catalogados como menores.
* Reasignar la posición original de los rostros en la imagen de salida tras su procesamiento.

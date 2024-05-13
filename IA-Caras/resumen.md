Directorio relativo a pruebas de la IA para la detección de rostros YolovFacev8.

* Se importa del modelo "yolov8n-face.pt".
* Se le pasa el path de la imagen deseada.
* Se preparan los delimitadores para el rostro detectado.
* Se guardan las caras de la imagen en base a los delimitadores.
* Se guarda una imagen con los marcos de los rostros detectados.

Futuras acciones: **Estas funciones ya tienen su respectivo codigo, abajo explico los principales bloques del notebook**
* Pixelar/Tapar los rostros catalogados como menores.
* Reasignar la posición original de los rostros en la imagen de salida tras su procesamiento.


Los dos grandes bloques del notebook son:
* **Primer Bloque**: llama al modelo - carga la imagen que se va a someter al proceso - define los vertices del area del rostro detectado - crea la carpeta 'imagenes_recortadas' si no existe - guarda los rostros detectados en la imagen procesada a traves de la definición de la propia area.
* **Segundo Bloque**: 

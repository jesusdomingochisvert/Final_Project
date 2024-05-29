# Proyecto de Detección de Menores de Edad en Imágenes

## Introducción

Este proyecto se enfoca en desarrollar un sistema que detecte si una persona
en una imagen es menor de edad. El sistema se implementa utilizando dos modelos
de IA: uno entrenado desde cero y otro utilizando MobileNetV2 mediante
transferencia de conocimiento. Los contenedores Docker se utilizan para 
orquestar los diferentes servicios.

## Estructura del Proyecto

- **api-gateway**: Servicio para manejar las solicitudes de los usuarios y redirigirlas a los otros servicios.
- **ia_container**: Servicio que contiene la lógica de procesamiento de imágenes y detección de rostros.
- **shared**: Volumen compartido para almacenar imágenes procesadas.

## Instalación

Siga los pasos a continuación para configurar y ejecutar el proyecto:

1. Clonar el repositorio `git clone https://github.com/jesusdomingochisvert/Final_Project.git`.
2. Construir y ejecutar los contenedores Docker utilizando docker-compose `docker-compose up --build`.

## Modelos de IA Utilizados

### Modelo Entrenado Desde Cero

El modelo entrenado desde cero utiliza una arquitectura de red neuronal 
convolucional (CNN) con múltiples capas convolucionales, de pooling y densas.

### Modelo MobileNetV2

MobileNetV2 se utiliza como base para el modelo mediante transferencia de 
conocimiento. Este modelo congela las capas del modelo base inicialmente y 
luego descongela las capas superiores para un ajuste fino.

## Contenedores Docker

El proyecto se compone de dos contenedores Docker:

### 1. API Gateway Container

Este contenedor expone públicamente el API para los clientes y enruta las 
peticiones al "IA Container". Recibe una imagen, la envía al "IA Container" 
y devuelve la imagen procesada.

### 2. IA Container

Este contenedor procesa las imágenes para detectar rostros y edades, 
pixelando los rostros de menores de edad y generando un log con detalles 
de las peticiones y el procesamiento.

## IAs Utilizadas

1. **IA Caras**: Encargada de detectar las caras en una foto usando Yolov8. Más información en: ultralytics.
2. **IA Menor Edad**: Desarrollada desde cero para determinar si un rostro es de una persona menor de 18 años usando 
datos de entrenamiento de Kaggle.

## Desarrollo de "IA Menor Edad"

- Entrada de imagen: 200x200.
- Cuatro bloques convolucionales con filtros y capas específicas.
- Doce modelos diferentes probados con distintas configuraciones.
- Gráficas y análisis para seleccionar el mejor modelo y ajustar el umbral adecuado.
- Implementación de transferencia de conocimiento con MobileNetV2.
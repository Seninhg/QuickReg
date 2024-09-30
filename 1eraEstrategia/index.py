import cv2
import numpy as np

# Cargar la imagen
image_path = 'zoom.png'
image = cv2.imread(image_path)

# Convertir a escala de grises
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Aplicar un desenfoque para suavizar la imagen y reducir el ruido
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Utilizar el detector de bordes de Canny
edges = cv2.Canny(blurred, 50, 150)

cv2.imshow('Edges', edges)

# Encontrar contornos a partir de la imagen binaria basada en bordes
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filtrar y extraer cuadros
cuadros = []
for contour in contours:
    # Obtener el rectángulo delimitador para cada contorno
    x, y, w, h = cv2.boundingRect(contour)
    
    # Filtrar por tamaño para descartar elementos pequeños o grandes no deseados
    if w > 40 and h > 40:  # Ajustar estos valores según el tamaño de los cuadros
        cuadro = image[y:y+h, x:x+w]
        cuadros.append(cuadro)
        cv2.rectangle(image, (x - 70, y - 10), (x + w + 50, y + h + 30), (0, 255, 0), 2)  # Dibujar un rectángulo para visualización
    

# Mostrar la imagen con los cuadros detectados
cv2.imshow('Cuadros Detectados', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Aquí podrías implementar el reconocimiento de dígitos u otras características
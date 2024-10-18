import easyocr
import cv2
from scripts.excelGen import GenExcel

class ScanearCaptura:
    def __init__(self, nombreCurso, checkHandUp=False):
        self.nombreCurso = nombreCurso
        self.checkHandUp = checkHandUp
        self.reader = easyocr.Reader(['en', 'es'], gpu=False)

    def getStudents(self, imagePath):
        # VARIABLES
        image = cv2.imread(imagePath)

        if image is None:
            return {
                "status": "error",
                "message": "No se pudo cargar la imagen. Comprueba que la ruta sea correcta. Esto puede deberse al uso de caracteres especiales en la ruta del archivo.",
            }

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Umbralización
        _, thresholded_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY_INV)

        # Parámetros de filtro
        media_ancho = 167.33
        desviacion_estandar_ancho = 21.23
        media_alto = 17.11
        desviacion_estandar_alto = 2.51

        # Rango de valores aceptados para ancho y alto
        min_ancho = media_ancho - 4 * desviacion_estandar_ancho
        max_ancho = media_ancho + 2 * desviacion_estandar_ancho
        min_alto = media_alto - 2 * desviacion_estandar_alto
        max_alto = media_alto + 3 * desviacion_estandar_alto

        # Inicializar generación de Excel
        genExcel = GenExcel(self.checkHandUp)

        result = self.reader.readtext(image)
        estudiantes = []

        for res in result:
            # Convertir las coordenadas a tuplas (x, y)
            pt1 = tuple(map(int, res[0][0]))  # Convertir a tupla (x, y)
            pt3 = tuple(map(int, res[0][2]))  # Convertir a tupla (x, y)
            ancho = pt3[0] - pt1[0]
            alto = pt3[1] - pt1[1]

            if min_ancho <= ancho <= max_ancho and min_alto <= alto <= max_alto:
                cv2.rectangle(image, pt1, pt3, (0, 0, 255), 2)
                student = {"name": res[1]}
                if self.checkHandUp:
                    # Implementar lógica de mano levantada
                    pass  # Aquí iría tu código para verificar la mano levantada
                estudiantes.append(student)
            else:
                cv2.rectangle(image, pt1, pt3, (255, 0, 0), 2)

        # Generar Excel con el nombre del curso y lista de estudiantes
        genExcel.generar(self.nombreCurso, estudiantes)

        # Mostrar imagen (opcional)
        cv2.imshow('image', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return {
            "status": "success",
            "message": "Estudiantes registrados correctamente, el archivo Excel con la asistencia ha sido generado.",
        }


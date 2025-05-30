# Importamos los módulos necesarios
from fastapi import APIRouter, UploadFile, File  # Para crear rutas y manejar archivos subidos
from fastapi.responses import JSONResponse       # Para retornar respuestas JSON personalizadas
from ultralytics import YOLO                     # Cargamos el modelo de detección YOLOv8
import cv2                                       # Usamos OpenCV para procesar el video
import shutil                                    # Para copiar el archivo subido al servidor
import os                                        # Para eliminar el archivo después de procesarlo

# Creamos un router que se puede incluir en el main
router = APIRouter()

# Cargamos el modelo YOLO. Asegurate de tener yolov8m.pt en tu sistema.
model = YOLO('scripts/yolov8m.pt')

# Diccionario con pesos promedio y área de referencia para estimar el peso
PESO_PROMEDIO = {
    'cow': {'peso': 600, 'area_ref': 12000},
    'sheep': {'peso': 70, 'area_ref': 3000},
    'horse': {'peso': 500, 'area_ref': 10000}
}

# Traducción de nombres en inglés a español
TRADUCCION = {
    'cow': 'Vaca',
    'sheep': 'Oveja',
    'horse': 'Caballo'
}

# Umbrales de filtrado: confianza mínima y área mínima para considerar una detección
UMBRAL_CONFIANZA = 0.5
AREA_MINIMA = 1000

# Ruta POST para procesar el video subido
@router.post("/procesar-video/")
async def procesar_video(file: UploadFile = File(...)):
    # Guardamos el archivo subido en la carpeta static/videos
    video_path = f"static/videos/{file.filename}"
    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Abrimos el video con OpenCV
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        # Si no se puede abrir, devolvemos un error
        return JSONResponse(content={"error": "No se pudo abrir el video."}, status_code=400)

    resultados = []  # Lista para guardar las detecciones válidas

    # Procesamos cada frame del video
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # Salimos si no hay más frames

        # Ejecutamos el modelo en el frame actual
        results = model(frame)[0]
        class_names = results.names  # Nombres de clases detectadas

        # Iteramos sobre cada detección (caja)
        for box in results.boxes:
            conf = float(box.conf[0])  # Confianza de la detección
            if conf < UMBRAL_CONFIANZA:
                continue  # Ignoramos detecciones poco confiables

            cls_id = int(box.cls[0])          # ID de la clase detectada
            nombre = class_names[cls_id]      # Nombre de la clase (ej. 'cow')

            if nombre not in PESO_PROMEDIO:
                continue  # Ignoramos animales no considerados

            # Coordenadas de la bounding box
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            area = (x2 - x1) * (y2 - y1)  # Calculamos el área del objeto

            if area < AREA_MINIMA:
                continue  # Ignoramos objetos muy pequeños

            # Estimación de peso basada en el área y el valor de referencia
            ref = PESO_PROMEDIO[nombre]
            peso_estimado = (area / ref['area_ref']) * ref['peso']
            peso_estimado = round(max(peso_estimado, 1), 1)  # Redondeamos y evitamos 0

            # Traducción al español
            nombre_es = TRADUCCION.get(nombre, nombre)

            # Agregamos el resultado a la lista
            resultados.append({
                "animal": nombre_es,
                "peso_estimado": peso_estimado,
                "confianza": round(conf, 2),
                "bounding_box": [x1, y1, x2, y2]
            })

    # Cerramos el video y eliminamos el archivo temporal
    cap.release()
    os.remove(video_path)

    # Devolvemos los resultados al frontend
    return {"resultados": resultados}



# const formData = new FormData();
# formData.append("file", fileInput.files[0]);

# fetch("http://localhost:8000/yolo/procesar-video/", {
#   method: "POST",
#   body: formData
# })
#   .then(res => res.json())
#   .then(data => console.log(data));

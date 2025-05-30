# from ultralytics import YOLO
# import cv2

# # Carga el modelo
# model = YOLO('scripts/yolov12n.pt')

# video_path = 'static/videos/vacas.mp4'
# # https://res.cloudinary.com/demo/video/upload/v1467809362/bb_bunny.mp4
# cap = cv2.VideoCapture(video_path)

# if not cap.isOpened():
#     print(f"No se pudo abrir el video en {video_path}")
#     exit()

# # Máximos detectados
# max_vacas = 0
# max_ovejas = 0

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     results = model(frame)[0]

#     # Lista de clases detectadas en este frame
#     class_names = results.names
#     class_ids = results.boxes.cls.tolist()

#     # Contadores temporales para este frame
#     count_vacas = sum(1 for cls_id in class_ids if class_names[int(cls_id)] == 'cow')
#     count_ovejas = sum(1 for cls_id in class_ids if class_names[int(cls_id)] == 'sheep')

#     # Actualizar máximos
#     max_vacas = max(max_vacas, count_vacas)
#     max_ovejas = max(max_ovejas, count_ovejas)

#     # Mostrar resultados
#     annotated_frame = results.plot()
#     cv2.imshow('Detección de Vacas', annotated_frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()

# # Imprimir resultados máximos
# print(f"Máximo de vacas detectadas en un solo frame: {max_vacas}")
# print(f"Máximo de ovejas detectadas en un solo frame: {max_ovejas}")

from ultralytics import YOLO
import cv2

# Modelo más preciso (descargalo si no lo tenés)
model = YOLO('yolov8m.pt')  # Alternativas: yolov8l.pt o entrenado propio

video_path = 'static/videos/cow6.mp4'
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print(f"No se pudo abrir el video en {video_path}")
    exit()

# Constantes calibradas manualmente (aproximadas)
PESO_PROMEDIO = {
    'cow':   {'peso': 600, 'area_ref': 12000},
    'sheep': {'peso': 70,  'area_ref': 3000},
    'horse': {'peso': 500, 'area_ref': 10000}
}

# Traducción al español
TRADUCCION = {
    'cow': 'Vaca',
    'sheep': 'Oveja',
    'horse': 'Caballo'
}

# Colores por clase
COLORES = {
    'cow': (0, 255, 0),
    'sheep': (255, 140, 0),
    'horse': (0, 0, 255)
}

# Umbrales
UMBRAL_CONFIANZA = 0.5
AREA_MINIMA = 1000  # px²

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)[0]
    class_names = results.names

    for box in results.boxes:
        conf = float(box.conf[0])
        if conf < UMBRAL_CONFIANZA:
            continue  # Ignorar detecciones poco confiables

        cls_id = int(box.cls[0])
        nombre = class_names[cls_id]

        if nombre not in PESO_PROMEDIO:
            continue

        x1, y1, x2, y2 = map(int, box.xyxy[0])
        area = (x2 - x1) * (y2 - y1)
        if area < AREA_MINIMA:
            continue  # Ignorar objetos muy pequeños

        ref = PESO_PROMEDIO[nombre]
        peso_estimado = (area / ref['area_ref']) * ref['peso']
        peso_estimado = round(max(peso_estimado, 1), 1)

        # Traducción al español
        nombre_es = TRADUCCION.get(nombre, nombre)

        # Dibujar bounding box
        color = COLORES.get(nombre, (255, 255, 255))
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        # Texto con peso estimado
        label = f"{nombre_es} - Peso: {peso_estimado} kg"
        cv2.putText(frame, label, (x1, y1 - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    cv2.imshow('Detección y Estimación de Peso', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

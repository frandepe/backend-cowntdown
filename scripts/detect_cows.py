from ultralytics import YOLO
import cv2

# Carga el modelo (asegúrate de tener yolov12n.pt en la carpeta o se descargará)
model = YOLO('scripts/yolov12n.pt')

video_path = 'static/videos/vacas.mp4'  # Cambia por el path de tu video
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print(f"No se pudo abrir el video en {video_path}")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)[0]  # Detectar objetos en el frame
    annotated_frame = results.plot()  # Dibuja las cajas y etiquetas en la imagen

    cv2.imshow('Detección de Vacas', annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Presiona 'q' para salir
        break

cap.release()
cv2.destroyAllWindows()

# python scripts/detect_cows.py
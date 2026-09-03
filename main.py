import cv2
import yaml
from ultralytics import YOLO
from src.privacy import apply_face_blur
from src.tracker import PhoneTracker
from src.alerts import dispatch_alert

def carregar_config():
    with open("config/settings.yaml", "r") as file:
        return yaml.safe_load(file)

def main():
    config = carregar_config()
    model = YOLO(config["model_path"])
    tracker = PhoneTracker(time_threshold=config["time_threshold_seconds"])
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erro: Não foi possível abrir a webcam.")
        return

    print("Iniciando Worker Local... Pressione ESC para sair.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        height, width = frame.shape[:2]
        scale = config["frame_width"] / width
        frame = cv2.resize(frame, (config["frame_width"], int(height * scale)))
        frame = apply_face_blur(frame)
        results = model.track(frame, persist=True, verbose=False)
        
        current_detections = []

        if results[0].boxes.id is not None:
            boxes = results[0].boxes
            for i in range(len(boxes)):
                class_id = int(boxes.cls[i])
                conf = float(boxes.conf[i])
                
                if class_id == 67 and conf >= config["confidence_threshold"]:
                    track_id = int(boxes.id[i])
                    current_detections.append((track_id, conf))
                    
                    x1, y1, x2, y2 = map(int, boxes.xyxy[i])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 165, 255), 2)
                    cv2.putText(frame, f"ID:{track_id} | Celular", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 165, 255), 2)

        alertas_disparados = tracker.update(current_detections)
      
        for track_id, duration, conf in alertas_disparados:
            dispatch_alert(
                room_id=config["room_id"],
                camera_id=config["camera_id"],
                track_id=track_id,
                duration=duration,
                confidence=conf
            )
            cv2.putText(frame, "ALERTA ENVIADO AO PROFESSOR!", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow("Sistema Escolar - Monitoramento de Borda", frame)

        if cv2.waitKey(1) & 0xFF == 27: 
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

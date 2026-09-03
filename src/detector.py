import cv2
from ultralytics import YOLO

MODEL_PATH = "yolov8n.pt"
CONFIDENCE = 0.45
FRAME_WIDTH = 640

def main():
    try:
        model = YOLO(MODEL_PATH)

        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            raise RuntimeError("Não foi possível abrir a webcam.")

        while True:
            ret, frame = cap.read()

            if not ret:
                print("Falha ao capturar frame.")
                break

            height, width = frame.shape[:2]
            scale = FRAME_WIDTH / width
            frame = cv2.resize(
                frame,
                (FRAME_WIDTH, int(height * scale))
            )

            results = model(frame, verbose=False)

            for result in results:
                for box in result.boxes:
                    confidence = float(box.conf[0])
                    class_id = int(box.cls[0])

                    if class_id != 67 or confidence < CONFIDENCE:
                        continue

                    x1, y1, x2, y2 = map(
                        int, box.xyxy[0]
                    )

                    cv2.rectangle(
                        frame,
                        (x1, y1),
                        (x2, y2),
                        (0, 0, 255),
                        2
                    )

                    cv2.putText(
                        frame,
                        f"Celular: {confidence:.0%}",
                        (x1, max(y1 - 10, 20)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 0, 255),
                        2
                    )

                    cv2.putText(
                        frame,
                        "ALERTA: CELULAR DETECTADO",
                        (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 0, 255),
                        2
                    )

            cv2.imshow("Detector de Smartphones", frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break

    except RuntimeError as error:
        print(f"Erro: {error}")

    except Exception as error:
        print(f"Erro inesperado: {error}")

    finally:
        if "cap" in locals() and cap.isOpened():
            cap.release()

        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

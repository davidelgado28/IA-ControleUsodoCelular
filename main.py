import cv2
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
PERSON_CLASS = 0
PHONE_CLASS = 67

def phone_belongs_to_student(phone_box, person_box):
    cel_x1, cel_y1, cel_x2, cel_y2 = phone_box
    centro_x_celular = (cel_x1 + cel_x2) // 2
    centro_y_celular = (cel_y1 + cel_y2) // 2
    aluno_x1, aluno_y1, aluno_x2, aluno_y2 = person_box

    if (aluno_x1 <= centro_x_celular <= aluno_x2) and (aluno_y1 <= centro_y_celular <= aluno_y2):
        return True
    return False

def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Erro: Não foi possível acessar a câmera.")
        return

    print("Monitoramento iniciado (Perspectiva 45 graus). Pressione 'q' para sair.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, stream=True, verbose=False)
        persons = []
        phones = []

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls = int(box.cls[0])
                conf = float(box.conf[0])

                if cls == PERSON_CLASS and conf > 0.50:
                    persons.append([x1, y1, x2, y2])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1) 
                    
                elif cls == PHONE_CLASS and conf > 0.30:
                    phones.append([x1, y1, x2, y2])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2) 

        alerta_global = False

        for phone in phones:
            for person in persons:
                if phone_belongs_to_student(phone, person):
                    alerta_global = True
                    cv2.rectangle(frame, (person[0], person[1]), (person[2], person[3]), (0, 0, 255), 3)
                    cv2.putText(frame, 'ALERTA: Celular detectado!', (person[0], person[1] - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                    break 

        if alerta_global:
            cv2.putText(frame, "ATENCAO: USO DE CELULAR DETECTADO", (20, 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)

        cv2.imshow('Monitoramento Sala - Visão 45 Graus', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

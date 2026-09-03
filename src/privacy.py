import cv2

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def apply_face_blur(frame):
    """Detecta rostos e aplica desfoque Gaussiano para conformidade com a LGPD."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)
    
    for (x, y, w, h) in faces:
        roi = frame[y:y+h, x:x+w]
        blur = cv2.GaussianBlur(roi, (51, 51), 0)
        frame[y:y+h, x:x+w] = blur
        
    return frame

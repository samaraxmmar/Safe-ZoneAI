import cv2
import numpy as np
from facenet_pytorch import InceptionResnetV1, MTCNN
from ultralytics import YOLO
from torchvision import transforms
from PIL import Image
from face_db import load_face_database
from log import add_log

# === Variables globales, vides au début ===
yolo_model = None
face_model = None
mtcnn = None
face_db = None

# === Fonction d'initialisation ===
def init_models():
    global yolo_model, face_model, mtcnn, face_db
    yolo_model = YOLO("/home/ubuntu/SafeZone-AI/models/best.pt")
    face_model = InceptionResnetV1(pretrained='vggface2').eval()
    mtcnn = MTCNN(keep_all=True)
    face_db = load_face_database(face_model, mtcnn)

def detect(frame):
    global yolo_model, face_model, mtcnn, face_db
    if yolo_model is None:
        raise ValueError("Les modèles ne sont pas chargés. Appelle init_models() d'abord.")

    results = yolo_model(frame)[0]

    for det in results.boxes.data:
        x1, y1, x2, y2, score, class_id = det[:6]
        x1, y1, x2, y2 = map(int, (x1, y1, x2, y2))
        label = yolo_model.names[int(class_id)]
        confidence = float(score)

        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(frame, f'{label} {confidence:.2f}', (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        add_log(equipement=label)

    boxes, probs = mtcnn.detect(frame)

    if boxes is not None:
        for box in boxes:
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            faces = frame[y1:y2, x1:x2]
            if faces.size == 0:
                continue

            faces = cv2.cvtColor(faces, cv2.COLOR_BGR2RGB)
            face_image = Image.fromarray(faces)

            transform = transforms.Compose([
                transforms.ToTensor(),
                transforms.Resize((160, 160)),
                transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                     std=[0.229, 0.224, 0.225])
            ])
            face_tensor = transform(face_image).unsqueeze(0)
            face_embedding = face_model(face_tensor)

            identity = "Inconnu"
            min_distance = float("inf")

            for name, embedding in face_db.items():
                dist = np.linalg.norm(face_embedding.detach().numpy() - embedding.detach().numpy())
                if dist < min_distance:
                    min_distance = dist
                    identity = name

            cv2.putText(frame, identity, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            if identity != "Inconnu":
                add_log(personne=identity)

    return frame 
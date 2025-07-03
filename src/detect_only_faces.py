import cv2
import numpy as np
from PIL import Image
from torchvision import transforms
from facenet_pytorch import InceptionResnetV1, MTCNN
from face_db import load_face_database
from log import add_log

# === Variables globales ===
face_model = None
mtcnn = None
face_db = None

# === Initialisation des modèles ===
def init_models():
    global face_model, mtcnn, face_db
    face_model = InceptionResnetV1(pretrained='vggface2').eval()
    mtcnn = MTCNN(keep_all=True)
    face_db = load_face_database(face_model, mtcnn)

# === Fonction de détection et reconnaissance faciale ===
def detect_faces(frame):
    global face_model, mtcnn, face_db
    if face_model is None or mtcnn is None or face_db is None:
        raise ValueError("Les modèles ne sont pas chargés. Appelle init_models() d'abord.")

    boxes, probs = mtcnn.detect(frame)

    if boxes is not None:
        for box in boxes:
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            face_crop = frame[y1:y2, x1:x2]
            if face_crop.size == 0:
                continue

            face_rgb = cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB)
            face_image = Image.fromarray(face_rgb)

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
def main():
    init_models()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erreur : impossible d'ouvrir la webcam")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = detect_faces(frame)

        cv2.imshow("Face Detection & Recognition", frame)

        if cv2.waitKey(1) & 0xFF == 27:  # Échapp pour quitter
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

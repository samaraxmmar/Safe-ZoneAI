# face_db.py
import os
import cv2
import torch
import numpy as np
from torchvision import transforms

def load_face_database(face_model, mtcnn, known_faces_path="/home/ubuntu/SafeZone-AI/data/known_faces"):
    face_db = {}
    for person_name in os.listdir(known_faces_path):
        person_path = os.path.join(known_faces_path, person_name)
        if not os.path.isdir(person_path):
            continue  # Skip si ce n’est pas un dossier
        embeddings = []
        for img_name in os.listdir(person_path):
            img_path = os.path.join(person_path, img_name)
            img = cv2.imread(img_path)
            if img is None:
                continue
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            face = mtcnn(img_rgb)
            if face is not None and face.ndim == 3:
                face = face.unsqueeze(0)  # [1, 3, 160, 160]
            elif face is not None and face.ndim == 4:
                face = face[:1]  # prend le premier visage seulement
            else:
                continue
            with torch.no_grad():
                embedding = face_model(face).detach()
            embeddings.append(embedding)
        if embeddings:
            face_db[person_name] = torch.stack(embeddings).mean(dim=0)
    return face_db

import cv2
from detect_only_faces import init_models, detect_faces

def main():
    # Initialise les modèles et la base de données
    init_models()

    # Chemin de l’image test
    test_image_path = "C:/Users/samar/OneDrive/Desktop/pfe/known_faces/ahmed/ali.jpg"

    # Charge l’image
    frame = cv2.imread(test_image_path)
    if frame is None:
        print(f"Impossible de lire l'image {test_image_path}")
        return

    # Applique la détection + reconnaissance
    frame = detect_faces(frame)

    # Affiche le résultat
    cv2.imshow("Reconnaissance faciale", frame)
    cv2.waitKey(0)  # Attend une touche
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

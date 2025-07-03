from flask import Flask, render_template, Response, jsonify, stream_with_context
import cv2
import pandas as pd
from detect import detect,init_models
from log import read_logs

app = Flask(__name__, template_folder="../frontend")
init_models()
def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        frame = detect(frame)
        _, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/get_detections')
def get_detections():
    # Récupérer les détections les plus récentes depuis les logs
    recent_logs = read_logs()  # Récupérer les 10 derniers logs
    
    # Filtrer pour ne récupérer que les logs d'équipement
    equipment_logs = [log for log in recent_logs if log.get('equipement') != 'None' and log.get('equipement')]
    
    # Transformer les données pour le format front-end
    detections = []
    for log in equipment_logs:
        # Éviter les doublons en vérifiant si l'équipement est déjà dans la liste
        if not any(d['label'] == log['equipement'] for d in detections):
            detections.append({
                'label': log['equipement'],
                'confidence': 0.85 + (random.random() * 0.15)  # Simuler un niveau de confiance entre 85% et 100%
            })
    
    # Si on a des données de FPS ou de performance, on peut les ajouter ici
    # Pour l'instant, on utilise une valeur aléatoire
    fps = random.randint(22, 28)
    
    return jsonify({
        'detections': detections,
        'fps': fps,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

# N'oubliez pas d'ajouter cette importation en haut du fichier
import random


@app.route('/dashboard')
def dashboard():
    logs = read_logs()
    
    # Regroupement des détections par personne et équipement
    persons_data = {}
    equipment_counts = {
        "casque": {"porté": 0, "non-porté": 0},
        "gilet": {"porté": 0, "non-porté": 0},
        "gants": {"porté": 0, "non-porté": 0},
        "bottes": {"porté": 0, "non-porté": 0},
        "lunettes": {"porté": 0, "non-porté": 0}
    }
    
    # On transforme les logs bruts en données utilisables
    for log in logs:
        heure = log.get('heure')
        personne = log.get('personne')
        equipement = log.get('equipement')
        
        # On ignore les entrées vides
        if personne == 'None' and equipement == 'None':
            continue
        
        # Traitement des détections de personnes
        if personne != 'None' and personne:
            if personne not in persons_data:
                persons_data[personne] = {
                    "derniere_detection": heure,
                    "equipements": {
                        "casque": "non-porté",
                        "gilet": "non-porté",
                        "gants": "non-porté",
                        "bottes": "non-porté",
                        "lunettes": "non-porté"
                    }
                }
        
        # Traitement des détections d'équipements
        if equipement != 'None' and equipement:
            # Correspondance entre les noms de modèle et les noms français
            equipment_map = {
                "helmet": "casque",
                "vest": "gilet",
                "gloves": "gants", 
                "boots": "bottes",
                "goggles": "lunettes"
            }
            
            fr_equipment = equipment_map.get(equipement.lower(), equipement.lower())
            
            # Si c'est un des équipements que l'on suit
            if fr_equipment in ["casque", "gilet", "gants", "bottes", "lunettes"]:
                # On cherche la dernière personne détectée (dans une fenêtre de 5 secondes)
                last_person = None
                for person, data in persons_data.items():
                    time_diff = abs((datetime.strptime(heure, '%Y-%m-%d %H:%M:%S') -
                                    datetime.strptime(data["derniere_detection"], '%Y-%m-%d %H:%M:%S')).total_seconds())
                    if time_diff < 5:  # 5 secondes de tolérance
                        last_person = person
                        break
                
                if last_person:
                    persons_data[last_person]["equipements"][fr_equipment] = "porté"
                    equipment_counts[fr_equipment]["porté"] += 1
                else:
                    # Si on n'a pas de personne associée, on incrémente quand même le compteur
                    equipment_counts[fr_equipment]["porté"] += 1
    
    # Calcul des équipements non portés
    for person, data in persons_data.items():
        for eq, status in data["equipements"].items():
            if status == "non-porté":
                equipment_counts[eq]["non-porté"] += 1
    
    # On transforme le dictionnaire en liste pour le template
    processed_logs = []
    for person, data in persons_data.items():
        log_entry = {
            "heure": data["derniere_detection"],
            "personne": person,
            "equipements": data["equipements"]
        }
        processed_logs.append(log_entry)
    
    # Trier par heure de détection (plus récente en premier)
    processed_logs.sort(key=lambda x: x["heure"], reverse=True)
    
    now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    
    return render_template('dashboard.html', 
                          logs=processed_logs, 
                          equipment_counts=equipment_counts,
                          now=now)

# N'oubliez pas d'ajouter cette importation en haut du fichier
from datetime import datetime


if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0')


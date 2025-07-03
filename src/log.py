import csv
from datetime import datetime

LOG_FILE = 'log.csv'

def add_log(personne=None, equipement=None):
    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), personne, equipement])

def read_logs():
    logs = []
    try:
        with open(LOG_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) != 3:
                    continue
                logs.append({
                    'heure': row[0],
                    'personne': row[1],
                    'equipement': row[2]
                })
    except FileNotFoundError:
        # Si le fichier n'existe pas encore, retourne une liste vide
        pass
    return logs

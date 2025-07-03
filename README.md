# SafeZone AI – Real-Time Safety Detection System

## Project Overview

**SafeZone AI** is an innovative solution designed to enhance safety in industrial environments, particularly in companies dealing with chemical products. This system leverages artificial intelligence for real-time detection of personal protective equipment (PPE) and identification of authorized personnel in sensitive areas. The main objective is to prevent incidents by immediately alerting in case of non-compliance or unauthorized intrusion.

## Client Context

This project addresses the needs of a Tunisian industrial company aiming to strengthen on-site safety. The key requirements include:

* **Automated Monitoring:** Use of existing surveillance cameras for continuous detection.
* **Anomaly Detection:** Automatic identification of missing PPE (helmet, vest, glasses) and unauthorized individuals.
* **Centralized Dashboard:** A dashboard to visualize real-time alerts and track statistics by day and by area.
* **Local AI Processing:** AI processing is done locally or on a private server to ensure high data confidentiality, avoiding external cloud services.

## Key Features

* **PPE Detection:** Automatic recognition of helmet, safety vest, and safety glasses.
* **Facial Recognition:** Identification of authorized individuals in restricted areas.
* **Alert System:** Instant alert generation in case of safety rule violations or unauthorized access.
* **Interactive Dashboard:** Visualization of safety data, including number of alerts per day, violation videos, and list of unrecognized individuals.

## Technical Architecture

SafeZone AI is built with several interconnected components, ensuring robust performance and high confidentiality.

### AI Components

* **PPE Detection:** Uses **YOLOv8** for fast and accurate PPE detection.
* **Facial Recognition:** Combines **MTCNN** (Multi-task Cascaded Convolutional Networks) for face detection and **FaceNet** for generating facial embeddings and recognition.
* **Face Database:** A **SQLite** database stores embeddings of authorized employee faces, enabling fast and secure verification.

### Backend

The backend is developed using **Flask**, a lightweight Python web framework, to handle server-side logic and interactions with AI models and the database.

* **Video Stream:** Uses **Socket** or **WebRTC** for real-time video transmission from surveillance cameras.
* **REST API:** A RESTful API is provided for accessing alert data and statistics, enabling integration with other systems or applications.

### Frontend

The interactive dashboard is built using **Streamlit** or **Gradio** (in this implementation, an HTML/CSS/JS frontend is used).

* **Alert Visualization:** Displays number of alerts per day for quick incident monitoring.
* **Violation Videos:** Access to video recordings showing moments of safety rule violations.
* **Unrecognized People List:** Identification of unauthorized individuals entering sensitive areas.

### Storage

* **Database:** **SQLite** (or PostgreSQL for larger deployments) is used to store encoded faces, alert logs, and history of videos (or links to local files).

## Future Enhancements

Possible future improvements include integration with real-time alert systems via **Twilio** (for SMS/calls) or a **Telegram Bot** to instantly notify the security team of incidents.

## Dashboard Screenshots

Below are some previews of the SafeZone AI dashboard, showcasing its monitoring and reporting features.

### Overview

![Dashboard Overview](docs/images/dashboard_overview.png)

### Equipment Statistics

![Equipment Statistics](docs/images/dashboard_stats.png)

## Installation and Usage

### Prerequisites

* Python 3.x  
* pip (Python package manager)  
* OpenCV (for video processing)

### Installation Steps

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your_user/SafeZone-AI.git
    cd SafeZone-AI
    ```

2. **Install Python dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Prepare AI Models:**

    Ensure the YOLOv8 model (`best.pt`) is placed in the `models/` folder.

4. **Prepare the Face Database:**

    Place images of authorized personnel in the `data/known_faces/` directory.

### Launching the Application

1. **Start the Flask backend:**

    ```bash
    python src/app.py
    ```

2. **Access the dashboard:**

    Open your browser and go to `http://localhost:5000/dashboard` for the dashboard or `http://localhost:5000/` for the live video stream (if the camera is set up).

## Project Structure



```
SafeZone-AI/
├── src/
│ ├── app.py # Main Flask application
│ ├── detect.py # YOLOv8 detection logic
│ ├── detect_face.py # Face detection and recognition
│ ├── detect_only_faces.py # Face detection only
│ ├── face_db.py # Face database management
│ ├── log.py # Alert logging
├── frontend/
│ ├── dashboard.html # HTML template for dashboard
│ ├── index.html # HTML template for homepage (video stream)
│ ├── script.js # JavaScript for frontend interactions
│ ├── style.css # CSS styles for the frontend
├── models/
│ ├── best.pt # Trained YOLOv8 model
├── data/
│ ├── known_faces/ # Images of authorized individuals
│ ├── log.csv # Alert logs file
├── notebooks/
│ ├── model.ipynb # Jupyter notebook for training/experiments
├── docs/
│ ├── images/ # Documentation screenshots and images
├── requirements.txt # Python dependencies
├── README.md # This file
├── .gitignore # Git ignore rules
```

## Contribution

Contributions are welcome! Please follow these steps:

1. Fork the repository.  
2. Create a new branch (`git checkout -b feature/new-feature`).  
3. Make your changes and commit them (`git commit -am 'Add new feature'`).  
4. Push to the branch (`git push origin feature/new-feature`).  
5. Create a Pull Request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact

For any questions or suggestions, please open an issue on this GitHub repository.

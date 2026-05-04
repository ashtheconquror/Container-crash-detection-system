# Container Crash Detection System 🚢 (Pro Rebuild)

An ML-powered real-time monitoring and analysis system for container sensor data, featuring a modern decoupled architecture.

## 🚀 Overview

The system classifies container sensor events into "Normal", "Warning", or "Critical" using a Machine Learning model. This version features a high-performance **FastAPI** backend and a responsive **React + Vite** frontend.

### Key Features
- **📊 Signal Analysis**: Simulate and analyze event types with real-time ML feedback.
- **📡 Live Streaming**: Real-time telemetry via WebSockets.
- **📜 Event History**: Persistent SQLite logging of all anomalies.
- **💎 Modern UI**: React-based dashboard with Tailwind CSS and Recharts.

## 📂 Project Structure

```text
├── frontend/           # React + Vite application (TypeScript)
├── sensors/            # Signal generation and feature engineering
├── services/           # Core detection engine and alert logic
├── database/           # SQLite database logic and event logging
├── models/             # ML model training and saved artifacts
├── api_server.py       # FastAPI backend entry point
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## 🛠️ Setup & Installation

### 1. Backend Setup
1. Create a virtual environment: `python -m venv .venv`
2. Activate it: `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Mac/Linux)
3. Install dependencies: `pip install -r requirements.txt`

### 2. Frontend Setup
1. Navigate to the frontend folder: `cd frontend`
2. Install dependencies: `npm install`

## 🏃 How to Run

You will need to run the backend and frontend simultaneously.

### Start the Backend
```bash
python api_server.py
```
The API will be available at `http://localhost:8000`.

### Start the Frontend
```bash
cd frontend
npm run dev
```
The dashboard will be available at `http://localhost:5173`.

---
*Developed as part of a Final Year Project.*

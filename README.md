# CrowdCount

A real-time people-counting and crowd-monitoring application using FastAPI, SQLAlchemy, OpenCV, Ultralytics YOLOv8, React, Vite, TypeScript, Tailwind CSS, Recharts, and WebSockets.

## Features

- Webcam, RTSP/IP camera, and uploaded-video input
- Real YOLOv8 person detection
- Tracking IDs and zone occupancy
- Live dashboard and WebSocket updates
- Crowd-density heatmap overlay
- Camera, zone, alert, analytics, and admin APIs
- JWT login and role-based access
- SQLite persistence
- Automated zone and detection tests

## Demo Login

- Username: `admin`
- Password: `admin123`

Change or remove this demo account before deployment.

## Backend Setup

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item ..\.env.example ..\.env
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

- API: http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

## Frontend Setup

```powershell
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal, usually http://127.0.0.1:5173.

## Usage

1. Start the backend and frontend.
2. Sign in using the demo account.
3. Open **Camera management**.
4. Add webcam source `0`, an RTSP URL, or configure an uploaded video.
5. Start the camera.
6. Open **Zones** and configure a camera zone and threshold.

Uploaded videos must use `.mp4`, `.avi`, `.mov`, or `.mkv` format.

## Tests

```powershell
cd backend
python -m pytest -q
```

## Security

Copy `.env.example` to `.env`, set a strong `JWT_SECRET`, and never commit credentials, databases, uploads, or model weights.

## Project Structure

```text
backend/  FastAPI APIs, database, vision, tracking, and workers
frontend/ React TypeScript dashboard
models/   Optional local model storage
uploads/  Uploaded video files
reports/  Exported reports
```

# CrowdCount

Real-time FastAPI + SQLAlchemy + OpenCV + Ultralytics YOLOv8 + React people-counting system.

## Backend
```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item ..\.env.example ..\.env
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

API: http://127.0.0.1:8000/docs
Demo login: `admin` / `admin123`

## Frontend
Node.js must be installed and available on PATH.
```powershell
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal, usually http://127.0.0.1:5173.

## Use
1. Start the backend and frontend.
2. Sign in with the demo account.
3. Open Camera management and add camera source `0` for webcam.
4. Start the camera.
5. Configure zones and start processing.
6. Upload `.mp4`, `.avi`, `.mov`, or `.mkv` to replace a camera source with a video file.

## Tests
```powershell
cd backend
pytest -q
```

## Security
Copy `.env.example` to `.env` and set a secure `JWT_SECRET`. The database and uploaded files are excluded from Git.

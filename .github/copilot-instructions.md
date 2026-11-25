# CrowdCount workspace

- Build and preserve the FastAPI + SQLAlchemy backend and React TypeScript frontend.
- Use real Ultralytics YOLOv8 person detections and OpenCV; do not substitute fake detections.
- Keep API, database, vision, and UI concerns modular.
- Never commit .env secrets, database files, uploads, or model weights.

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .database.database import Base,engine,SessionLocal
from .models import models
from .api.routes import router
from .api.auth import hash_password
@asynccontextmanager
async def lifespan(app:FastAPI):
    Base.metadata.create_all(bind=engine)
    db=SessionLocal()
    if not db.query(models.User).filter(models.User.username=="admin").first():
        db.add(models.User(username="admin",password_hash=hash_password("admin123"),role="admin")); db.commit()
    db.close(); yield
app=FastAPI(title="CrowdCount API",version="1.0.0",lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.include_router(router,prefix="/api")
@app.websocket("/ws/live/{camera_id}")
async def live(websocket:WebSocket,camera_id:int):
    await websocket.accept()
    import asyncio
    try:
        while True:
            from .services.camera_manager import camera_manager
            await websocket.send_json(camera_manager.get_stats(camera_id)); await asyncio.sleep(1)
    except WebSocketDisconnect: pass
@app.get("/health")
def health(): return {"status":"healthy"}

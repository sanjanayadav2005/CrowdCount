from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
import os, shutil
from ..database.database import get_db
from ..models.models import *
from ..schemas.schemas import *
from .auth import current_user,admin_required,hash_password,verify_password,create_token
from ..services.camera_manager import camera_manager
router=APIRouter()
@router.post("/auth/login",response_model=Token)
def login(data:Login,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.username==data.username).first()
    if not user or not verify_password(data.password,user.password_hash): raise HTTPException(401,"Invalid username or password")
    return Token(access_token=create_token(user.username,user.role))
@router.post("/auth/register")
def register(data:UserCreate,db:Session=Depends(get_db)):
    if db.query(User).filter(User.username==data.username).first(): raise HTTPException(400,"Username already exists")
    user=User(username=data.username,password_hash=hash_password(data.password),role=data.role)
    db.add(user); db.commit(); return {"id":user.id,"username":user.username}
@router.get("/me")
def me(user=Depends(current_user)): return {"id":user.id,"username":user.username,"role":user.role}
@router.get("/cameras")
def cameras(db:Session=Depends(get_db),user=Depends(current_user)): return db.query(Camera).all()
@router.post("/cameras")
def create_camera(data:CameraCreate,db:Session=Depends(get_db),user=Depends(admin_required)):
    camera=Camera(name=data.name,source=data.source,source_type=data.source_type,confidence=data.confidence); db.add(camera); db.commit(); db.refresh(camera); return camera
@router.post("/cameras/{camera_id}/start")
def start_camera(camera_id:int,db:Session=Depends(get_db),user=Depends(current_user)):
    camera=db.query(Camera).filter(Camera.id==camera_id).first()
    if not camera: raise HTTPException(404,"Camera not found")
    zones=db.query(Zone).filter(Zone.camera_id==camera_id).all()
    camera_manager.start(camera.id,camera.source,camera.source_type,[{"id":z.id,"name":z.name,"coordinates":z.coordinates} for z in zones],camera.confidence)
    camera.status="online"; db.commit(); return {"started":True}
@router.post("/cameras/{camera_id}/stop")
def stop_camera(camera_id:int,db:Session=Depends(get_db),user=Depends(current_user)):
    camera_manager.stop(camera_id)
    camera=db.query(Camera).filter(Camera.id==camera_id).first()
    if camera: camera.status="offline"; db.commit()
    return {"started":False}
@router.get("/cameras/{camera_id}/stats")
def camera_stats(camera_id:int,user=Depends(current_user)): return camera_manager.get_stats(camera_id)
@router.get("/cameras/{camera_id}/frame")
def camera_frame(camera_id:int):
    jpg=camera_manager.get_frame(camera_id)
    if not jpg: raise HTTPException(503,"Live frame unavailable")
    import base64
    return StreamingResponse(iter([base64.b64decode(jpg)]),media_type="image/jpeg")
@router.post("/cameras/{camera_id}/upload")
async def upload_video(camera_id:int,file:UploadFile=File(...),db:Session=Depends(get_db),user=Depends(admin_required)):
    ext=os.path.splitext(file.filename or "")[1].lower()
    if ext not in {".mp4",".avi",".mov",".mkv"}: raise HTTPException(400,"Unsupported video format")
    os.makedirs("uploads",exist_ok=True); path=os.path.abspath(os.path.join("uploads",f"camera_{camera_id}_{file.filename}"))
    with open(path,"wb") as f: shutil.copyfileobj(file.file,f)
    camera=db.query(Camera).filter(Camera.id==camera_id).first();
    if not camera: raise HTTPException(404,"Camera not found")
    camera.source=path; camera.source_type="video"; db.commit(); return {"path":path}
@router.get("/zones")
def zones(camera_id:int|None=None,db:Session=Depends(get_db),user=Depends(current_user)):
    q=db.query(Zone); return q.filter(Zone.camera_id==camera_id).all() if camera_id else q.all()
@router.post("/zones")
def create_zone(data:ZoneCreate,db:Session=Depends(get_db),user=Depends(admin_required)):
    zone=Zone(camera_id=data.camera_id,name=data.name,coordinates=data.coordinates,threshold=data.threshold); db.add(zone); db.commit(); db.refresh(zone); return zone
@router.delete("/zones/{zone_id}")
def delete_zone(zone_id:int,db:Session=Depends(get_db),user=Depends(admin_required)):
    zone=db.query(Zone).filter(Zone.id==zone_id).first()
    if not zone: raise HTTPException(404,"Zone not found")
    db.delete(zone); db.commit(); return {"deleted":True}
@router.get("/alerts")
def alerts(db:Session=Depends(get_db),user=Depends(current_user)): return db.query(Alert).order_by(Alert.created_at.desc()).limit(100).all()
@router.get("/analytics")
def analytics(db:Session=Depends(get_db),user=Depends(current_user)):
    counts=db.query(CountingRecord).order_by(CountingRecord.timestamp.desc()).limit(24).all()
    return [{"timestamp":r.timestamp.isoformat(),"total":r.total_visible,"entries":r.entries,"exits":r.exits} for r in reversed(counts)]

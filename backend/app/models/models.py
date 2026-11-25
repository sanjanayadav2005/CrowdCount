from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey, Text, JSON, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from ..database.database import Base
class User(Base):
    __tablename__="users"
    id: Mapped[int]=mapped_column(primary_key=True); username: Mapped[str]=mapped_column(String(80),unique=True,index=True); password_hash: Mapped[str]=mapped_column(String(255)); role: Mapped[str]=mapped_column(String(20),default="user"); active: Mapped[bool]=mapped_column(Boolean,default=True); created_at: Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
class Camera(Base):
    __tablename__="cameras"
    id: Mapped[int]=mapped_column(primary_key=True); name: Mapped[str]=mapped_column(String(120)); source: Mapped[str]=mapped_column(String(500)); source_type: Mapped[str]=mapped_column(String(20),default="webcam"); active: Mapped[bool]=mapped_column(Boolean,default=True); status: Mapped[str]=mapped_column(String(30),default="offline"); confidence: Mapped[float]=mapped_column(Float,default=.45); created_at: Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
    zones: Mapped[list["Zone"]]=relationship(back_populates="camera")
class Zone(Base):
    __tablename__="zones"
    id: Mapped[int]=mapped_column(primary_key=True); camera_id: Mapped[int]=mapped_column(ForeignKey("cameras.id",ondelete="CASCADE"),index=True); name: Mapped[str]=mapped_column(String(120)); coordinates: Mapped[list]=mapped_column(JSON); threshold: Mapped[int]=mapped_column(Integer,default=10); camera: Mapped[Camera]=relationship(back_populates="zones")
class DetectionRecord(Base):
    __tablename__="detections"; id: Mapped[int]=mapped_column(primary_key=True); camera_id: Mapped[int]=mapped_column(ForeignKey("cameras.id"),index=True); count: Mapped[int]=mapped_column(Integer); timestamp: Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow,index=True)
class TrackingRecord(Base):
    __tablename__="tracking_records"; id: Mapped[int]=mapped_column(primary_key=True); camera_id: Mapped[int]=mapped_column(ForeignKey("cameras.id"),index=True); track_id: Mapped[int]=mapped_column(Integer,index=True); zone_id: Mapped[int|None]=mapped_column(ForeignKey("zones.id"),nullable=True); timestamp: Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow,index=True)
class CountingRecord(Base):
    __tablename__="counting_records"; id: Mapped[int]=mapped_column(primary_key=True); camera_id: Mapped[int]=mapped_column(ForeignKey("cameras.id"),index=True); entries: Mapped[int]=mapped_column(Integer,default=0); exits: Mapped[int]=mapped_column(Integer,default=0); total_visible: Mapped[int]=mapped_column(Integer,default=0); timestamp: Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow,index=True)
class Alert(Base):
    __tablename__="alerts"; id: Mapped[int]=mapped_column(primary_key=True); camera_id: Mapped[int]=mapped_column(ForeignKey("cameras.id"),index=True); zone_id: Mapped[int|None]=mapped_column(ForeignKey("zones.id"),nullable=True); severity: Mapped[str]=mapped_column(String(20),default="warning"); message: Mapped[str]=mapped_column(Text); resolved: Mapped[bool]=mapped_column(Boolean,default=False); created_at: Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow,index=True); resolved_at: Mapped[datetime|None]=mapped_column(DateTime,nullable=True)
class SystemLog(Base):
    __tablename__="system_logs"; id: Mapped[int]=mapped_column(primary_key=True); level: Mapped[str]=mapped_column(String(20)); message: Mapped[str]=mapped_column(Text); timestamp: Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow,index=True)

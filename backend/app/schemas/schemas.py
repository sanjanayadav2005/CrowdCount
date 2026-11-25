from pydantic import BaseModel
from typing import Optional, List

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class Login(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "user"

class CameraCreate(BaseModel):
    name: str
    source: str = "0"
    source_type: str = "webcam"
    confidence: float = .45

class CameraOut(BaseModel):
    id: int
    name: str
    source: str
    source_type: str
    active: bool
    status: str
    confidence: float
    model_config={"from_attributes":True}

class ZoneCreate(BaseModel):
    camera_id: int
    name: str
    coordinates: list[list[float]]
    threshold: int = 10

class ZoneOut(BaseModel):
    id: int
    camera_id: int
    name: str
    coordinates: list[list[float]]
    threshold: int
    model_config={"from_attributes":True}

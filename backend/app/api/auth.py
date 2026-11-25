from datetime import datetime,timedelta
from jose import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import os
from ..database.database import get_db
from ..models.models import User
pwd=CryptContext(schemes=["bcrypt"],deprecated="auto")
bearer=HTTPBearer()
SECRET=os.getenv("JWT_SECRET","change-this-in-production")
def hash_password(p): return pwd.hash(p)
def verify_password(p,h): return pwd.verify(p,h)
def create_token(subject:str,role:str):
    exp=datetime.utcnow()+timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES","1440")))
    return jwt.encode({"sub":subject,"role":role,"exp":exp},SECRET,algorithm=os.getenv("JWT_ALGORITHM","HS256"))
def current_user(creds:HTTPAuthorizationCredentials=Depends(bearer),db:Session=Depends(get_db)):
    try:
        data=jwt.decode(creds.credentials,SECRET,algorithms=[os.getenv("JWT_ALGORITHM","HS256")])
        user=db.query(User).filter(User.username==data["sub"],User.active==True).first()
        if not user: raise HTTPException(status_code=401,detail="Invalid user")
        return user
    except Exception: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid or expired token")
def admin_required(user:User=Depends(current_user)):
    if user.role != "admin": raise HTTPException(status_code=403,detail="Administrator access required")
    return user

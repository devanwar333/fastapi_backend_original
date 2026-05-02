from datetime import datetime, timedelta
import jwt
import os
SECRET = os.getenv("APP_SECRET_KEY", "secret")
ALGORITHM = os.getenv("APP_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))



def create_access_token(data: dict):

    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    return jwt.decode(token, SECRET, algorithms=[ALGORITHM])
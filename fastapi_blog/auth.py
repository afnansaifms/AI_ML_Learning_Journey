from jose import JWTError, jwt
from datetime import datetime,timedelta,timezone
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY="mysecret"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPRIE_MUNITES=30

oauth_schema=OAuth2PasswordBearer(tokenUrl="login")

def create_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPRIE_MUNITES)
    to_encode.update({"exp":expire})

    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

def verify_token(token: str=Depends(oauth_schema)):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        return payload
    except:
        raise HTTPException(status_code=401,detail="invalid token")


from fastapi import FastAPI,HTTPException,Depends,Header
from jose import jwt,JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext


app=FastAPI()

#jwt config
SECRET_KEY="mysecret"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_TIME=30

#password hashing

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

#oauthsetup
oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

#dummy user data
fake_user_db={
    'admin':{
        'username':"admin",
        'hashed_password':pwd_context.hash("1234")
    }
}

def hash_password(password:str):
    return pwd_context.hash(password)
#verify pass
def verify_password(plain_password,hased_password):
    return pwd_context.verify(plain_password,hased_password)

#creating token
def create_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+timedelta(minutes=30)
    to_encode.update({
        'exp':expire
    })
    token=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return token

#login api outh2form
@app.post('/login')
def login(from_data:OAuth2PasswordRequestForm=Depends()):
    user = fake_user_db.get(from_data.username)
    if not user or not verify_password(from_data.password,user['hashed_password']):
        raise HTTPException(
            status_code=400,
            detail="invalid username or password"
        )
    access_token = create_token({'sub':from_data.username})
    return{
        'access_token':access_token,
        'token_type':"bearer"
    } 
    
#verification

def verify_token(token:str = Depends(oauth2_schema)):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username: str =payload.get('sub')
        if username is None:
            raise HTTPException(
                status_code=401,
                detail="invalid token"
            )
        return username
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="invalid token"
        )
    

#protected route 
@app.get('/protected')
def protected_route(username: str=Depends(verify_token)):
    return {
        'message':"hello  you have acccess to this protected route",
        'user':username
    }
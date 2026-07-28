from fastapi import FastAPI, Depends, Header,HTTPException

app = FastAPI()

def verify_token(token:str=Header(None)):
    if token !="secret123":
        raise HTTPException(
            status_code=401,
            detail="unauthorised token"
        )
    return{
        'user':'Authorsied User'
    }
@app.get('/secure_data')
def secure_data(user=Depends(verify_token)):
    return user

# def common_logic():
#     return{
#         'message':'common logic executed'
#     }
# @app.get('/user')
# def home(data=Depends(common_logic)):
#     return data

# def get_current_user():
#     return{
#         'user':'afnan'
#     }

# @app.get('/profile')
# def profile(user=Depends(get_current_user)):
#     return user

# @app.get('/dashboard')
# def profile(user=Depends(get_current_user)):
#     return user
from fastapi import FastAPI,HTTPException,Request
from fastapi.responses import JSONResponse

app=FastAPI()

class UsernotFound(Exception):
    def __init__(self,name:str):
        self.name=name
@app.exception_handler(UsernotFound)
def user_not_found(request:Request,exception:UsernotFound):
    return JSONResponse(
        status_code=404,
        content={
            'status':'error',
            "message":f"user {exception.name} not found"
        }
    )
    
@app.get('/user/{name}')
def get_user(name:str):
    if name!="afnan":
        raise UsernotFound(name)
    return{
        "name":name,
        "status":"user found"
    }

# @app.get('/users/{user_id}')
# def get_user(user_id:int):
#     if user_id!=1:
#         raise HTTPException(
#             status_code=404,
#             detail="user not found"
#         )
#     return{
#         "id":1,
#         "name":'afnan'
#     }
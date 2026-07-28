from fastapi import FastAPI, status, HTTPException

app =FastAPI()

@app.post("/creat_user",status_code=status.HTTP_201_CREATED)
def create_user():
    return{
        'message':'user created'
    }
@app.get("/user")
def get_users():
    return{
        'status':"success",
        'message':'user feached',
        'data':{
            'name':'afnan',
            'age':21
        }
    }

@app.get('/user/{user_id}')
def get_user(user_id:int):
    if user_id!=1:
        raise HTTPException(
            status_code=404,
            detail='user not found'
        )
    return{
        'id':1,
        'name':'afnan'
    }
       
       

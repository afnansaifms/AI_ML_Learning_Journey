from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import sessionmaker,declarative_base,Session

from fastapi import FastAPI,Depends,HTTPException

app=FastAPI()

DATABASE_URL= "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread":False}
)

sessionlocal = sessionmaker(bind=engine)
base = declarative_base()

class Todo(base):
    __tablename__="todo"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    completed = Column(String)

base.metadata.create_all(bind=engine)

def get_db():
    db=sessionlocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/todos')
def create_todo(id:int ,title:str ,db:Session=Depends(get_db)):
    todo=Todo(title=title ,id=id ,completed='False')
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return{
        "messge":"todo created",
        "data":todo
    }

#all data
@app.get('/todos')
def create_todo(db:Session=Depends(get_db)):
    todos=db.query(Todo).all()
    
    return{
        "Total":len(todos),
        "data":todos
    }
#single data
@app.get("/todo/{todo_id}")
def get_data(todo_id=int,db:Session=Depends(get_db)):
    todo=db.query(Todo).filter(Todo.id==todo_id).first()

    if not todo:
        raise HTTPException(status_code=404,details="todo not found")
    return todo

#update

@app.put('/todo/{todo_id}')
def update_todo(todo_id:int, title:str, db:Session=Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, details="todo not found")

    todo.title=title
    db.commit()
    db.refresh(todo)
    return{
        "message":"updated",
        "data":todo
    }

#delete

@app.delete('/todos/{todo_id}')
def delete_todo(todo_id:int, db:Session=Depends(get_db)):
    todo=db.query(Todo).filter(Todo.id==todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, details="todo not found")
    db.delete(todo)
    db.commit()
    return{
        'message':"todo deleted"
    }

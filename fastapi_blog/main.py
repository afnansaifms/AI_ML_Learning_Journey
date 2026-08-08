from fastapi import FastAPI, Depends,HTTPException,Query
from sqlalchemy.orm import Session
from database import engine,SessionLocal
from database import Base
import models,schemas
from auth import create_token,verify_token


models.Base.metadata.create_all(bind=engine)
app=FastAPI()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

#login 
@app.post("/login")
def login():
    return{
        "access_token":create_token({"user":"admin"}),
        "token_type":"bearer"
    }

#home
@app.get('/')
def home():
    return{
        "message":"blog api start"
    }

@app.post('/blogs',response_model=schemas.BlogResponse)
def create_blog(blog:schemas.BlogCreate, db:Session=Depends(get_db), user=Depends(verify_token)):
    new_blog = models.Blog(
        id=blog.id,
        title=blog.title,
        content=blog.content
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blogs')
def get_all(page:int=1,
            limit:int=5,
            search:str=Query(default=""),
            db:Session=Depends(get_db)):
    query = db.query(models.Blog)
    if search:
        query=query.filter(models.Blog.title.ilike(f"%{search}%"))

    total = query.count()
    start=(page-1)*limit
    blogs=query.offset(start).limit(limit).all()
    return{
        "page":page,
        "limit":limit,
        "total":total,
        "data":blogs
    }


@app.get('/blogs/{id}',response_model=schemas.BlogResponse)
def get_by_id(id:int, db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="blog not found")
    return blog

@app.put("/blogs/{id}",response_model=schemas.BlogResponse)
def update_blog(id:int,blog:schemas.BlogCreate,db:Session=Depends(get_db), user=Depends(verify_token)):
    existing_blog=db.query(models.Blog).filter(models.Blog.id == id).first()
    if not existing_blog:
        raise HTTPException(status_code=404,detail="data not found")
    existing_blog.title=blog.title
    existing_blog.content=blog.content
    db.commit()
    return existing_blog

@app.delete("/blog/{id}")
def delete_blog(id:int,db:Session=Depends(get_db),user=Depends(verify_token)):
    blog  = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=404,detail="blog not found")
    blog.delete()
    db.commit()
    return {
        "message":"blog deleted successfully"
    }


from pydantic import BaseModel
class BlogCreate(BaseModel):
    id:int
    title:str
    content:str
class BlogResponse(BaseModel):
    id:int
    title:str
    content:str
    class Config:
        from_attribute=True
        
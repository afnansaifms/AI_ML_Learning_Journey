from fastapi import FastAPI
import requests

app =FastAPI()

@app.get('/posts')
def get_post(url:str):
    response=requests.get(url)
    return response.json()

@app.get('/posts/{post_id}')
def get_post(post_id:int):
    url=f"https://api.github.com/users/hadley/orgs/posts/{post_id}"
    response=requests.get(url)
    return response.json()
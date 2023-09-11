from fastapi import FastAPI
from route.general import user_post
from route.police_officer import police_post

app = FastAPI()

app.include_router(user_post.router)
app.include_router(police_post.router)



@app.get("/hello")
def show():
    return {"message" : "hello world"}



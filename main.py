from fastapi import FastAPI
from route.general import user_post
from route.police_officer import police_post,police_get

app = FastAPI()

app.include_router(user_post.router)
app.include_router(police_post.router)
app.include_router(police_get.router)



@app.get("/hello")
def show():
    return {"message" : "hello world"}



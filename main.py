from fastapi import FastAPI
from route.general import user_post
from route.police_officer import police_post,police_get
from route.it_officer import it_officer_post,it_officer_get
from route.criminal_reg_dept import criminal_reg_dept_get,criminal_reg_dept_post

app = FastAPI()

app.include_router(user_post.router)
app.include_router(police_post.router)
app.include_router(police_get.router)
app.include_router(it_officer_post.router)
app.include_router(criminal_reg_dept_get.router)
app.include_router(criminal_reg_dept_post.router)
app.include_router(it_officer_get.router)


@app.get("/hello")
def show():
    return {"message" : "hello world"}



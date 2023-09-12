from fastapi import FastAPI
from route.general import user_post
from route.police_officer import police_post,police_get
<<<<<<< HEAD
from route.it_officer import it_officer_post
=======
from route.criminal_reg_dept import criminal_reg_dept_get,criminal_reg_dept_post
>>>>>>> 7d14e1ec220c34ae4fdd903b9c3aab0bcd617f93

app = FastAPI()

app.include_router(user_post.router)
app.include_router(police_post.router)
app.include_router(police_get.router)
<<<<<<< HEAD
app.include_router(it_officer_post.router)
=======
app.include_router(criminal_reg_dept_get.router)
app.include_router(criminal_reg_dept_post.router)
>>>>>>> 7d14e1ec220c34ae4fdd903b9c3aab0bcd617f93


@app.get("/hello")
def show():
    return {"message" : "hello world"}



# fastapi imports
from fastapi import FastAPI

# CORS
from fastapi.middleware.cors import CORSMiddleware

# router imports
from .routers import post, user, auth, vote
from . import database, models

# intialize app
app = FastAPI()

# domains that can talk to our API *=all, best practice is just your web app domain deployment
origins = ["*"]

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# initialize db engine # NO LONGER NEED WITH ALEMBIC MANAGING TABLE CREATION
#models.Base.metadata.create_all(bind=database.engine)

### routes

# home
@app.get("/")
def root():
    return {"message": "welcome to my api!!! wooooop"}

# post
app.include_router(post.router)

# user
app.include_router(user.router)

# auth
app.include_router(auth.router)

# vote
app.include_router(vote.router)
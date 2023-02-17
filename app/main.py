from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api import api_router
from app.db.models import users
from app.cors.database import engine


users.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Instagram Influencer",
    description="API for creating and searching profiles",
    version="0.1.0",
    terms_of_service="http://github.com/nkasi-e/instagram-influencer",
    contact={
            "name": "Nkasi Emmanuel",
            "email": "emmanuelnkasi@gmail.com",
            "url": "http://github.com/nkasi-e/instagram-influencer"
    }
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router)


@app.get('/')
def root():
    return {"Message": "Welcome to Instagram Influencer"}

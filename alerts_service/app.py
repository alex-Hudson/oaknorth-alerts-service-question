from fastapi import FastAPI

from alerts_service import db, models, rest
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(on_startup=[lambda: models.Base.metadata.create_all(bind=db.engine)])
app.include_router(rest.router)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
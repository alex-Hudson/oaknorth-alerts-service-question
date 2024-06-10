from fastapi import FastAPI

from alerts_service import db, models, rest

app = FastAPI(on_startup=[lambda: models.Base.metadata.create_all(bind=db.engine)])
app.include_router(rest.router)

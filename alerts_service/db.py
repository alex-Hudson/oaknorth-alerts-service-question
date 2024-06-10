from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from alerts_service.settings import DB_URL

engine = create_engine(DB_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

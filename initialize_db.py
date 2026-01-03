import os
from models import Base
from sqlalchemy import create_engine

engine = create_engine(f'postgresql://postgres:{os.getenv("PG_PASSWORD")}@localhost:5432/gym', echo=True)
Base.metadata.create_all(engine)
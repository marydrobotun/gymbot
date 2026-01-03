import os
from sqlalchemy import create_engine, select, delete, insert, update
from sqlalchemy.orm import Session
from models import Base, Users, Trainings, Machines, Settings
engine = create_engine(f'postgresql://postgres:{os.getenv("PG_PASSWORD")}@localhost:5432/gym', echo=True)

def add_user(chat_id):
   with Session(engine) as session:
       inserting = insert(Users).values(chat_id=chat_id)
       session.execute(inserting)
       session.commit()

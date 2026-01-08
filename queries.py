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

def print_user_id(chat_id):
    selecting = select(Users.id).where(Users.chat_id == chat_id)
    with Session(engine) as session:
        result = session.execute(selecting).first()[0]
        print("\n\n\n\n\n", result, "\n\n\n\n\n")
        session.commit()

def add_training(title, chat_id):
    selecting = select(Users.id).where(Users.chat_id == chat_id)
    with Session(engine) as session:
        user_id = session.execute(selecting).first()[0]
        inserting = insert(Trainings).values(title=title, user_id=user_id)
        session.execute(inserting)
        session.commit()
def add_machine(title, training_id, weight):
    with Session(engine) as session:
        inserting = insert(Machines).values(title=title, training_id=training_id, weight=weight)
        session.execute(inserting)
        session.commit()
def add_setting(title, machine_id, value):
    with Session(engine) as session:
        inserting = insert(Settings).values(title=title, machine_id=machine_id, value=value)
        session.execute(inserting)
        session.commit()



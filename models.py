from typing import Optional

from sqlalchemy import ForeignKeyConstraint, Integer, PrimaryKeyConstraint, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='users_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)

    trainings: Mapped[list['Trainings']] = relationship('Trainings', back_populates='user')


class Trainings(Base):
    __tablename__ = 'trainings'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='trainings_user_id_fkey'),
        PrimaryKeyConstraint('id', name='trainings_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[Optional[int]] = mapped_column(Integer)

    user: Mapped[Optional['Users']] = relationship('Users', back_populates='trainings')
    machines: Mapped[list['Machines']] = relationship('Machines', back_populates='training')


class Machines(Base):
    __tablename__ = 'machines'
    __table_args__ = (
        ForeignKeyConstraint(['training_id'], ['trainings.id'], ondelete='CASCADE', name='machines_training_id_fkey'),
        PrimaryKeyConstraint('id', name='machines_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    weight: Mapped[int] = mapped_column(Integer, nullable=False)
    training_id: Mapped[Optional[int]] = mapped_column(Integer)

    training: Mapped[Optional['Trainings']] = relationship('Trainings', back_populates='machines')
    settings: Mapped[list['Settings']] = relationship('Settings', back_populates='machine')


class Settings(Base):
    __tablename__ = 'settings'
    __table_args__ = (
        ForeignKeyConstraint(['machine_id'], ['machines.id'], ondelete='CASCADE', name='settings_training_id_fkey'),
        PrimaryKeyConstraint('id', name='settings_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    value: Mapped[int] = mapped_column(Integer, nullable=False)
    machine_id: Mapped[Optional[int]] = mapped_column(Integer)

    machine: Mapped[Optional['Machines']] = relationship('Machines', back_populates='settings')

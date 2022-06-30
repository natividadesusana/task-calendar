"""
Os modelos do banco de dados utilizando a descrição do SQLAlchemy.
"""
from sqlalchemy import Column, String, Integer  # type: ignore

from .database import Base


class Task(Base):
    """
    Modelo de dados para persistir as informações das tarefas.
    """

    # nome da tabela
    __tablename__ = "tasks"

    # campos (tal qual definidos em "schemas.py")
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    schedule_datetime = Column(String)
    duration_time = Column(String)

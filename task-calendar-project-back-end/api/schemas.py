"""
Leiaute dos dados utilizados pelo pydantic para validação dos mesmos.
"""
from pydantic import BaseModel


class TaskBaseSchema(BaseModel):
    """
    Define a estrura de dados que armazena as informações das tarefas.
    """

    title: str
    description: str
    schedule_datetime: str
    duration_time: str


class CreateTaskSchema(TaskBaseSchema):
    """
    Esquema de dados para ser usado na criação de novas tarefas.
    """


class TaskSchema(TaskBaseSchema):
    """
    Esquema de dados para ser usado para visualização das tarefas.
    """

    id: int


class UpdateTaskSchema(TaskBaseSchema):
    """
    Esquema de dados para a atualização dos dados das tarefas.
    """

    title: str = ""
    description: str = ""
    schedule_datetime: str = ""
    duration_time: str = ""

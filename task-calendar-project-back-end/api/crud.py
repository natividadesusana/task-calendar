"""
Funções para o acesso ao banco de dados via SQLAlchemy via ORM ao
invés de consultas escritas diretamente em SQL.
"""
from typing import Generator
from asyncio import tasks

from sqlalchemy.orm import Session

from api.datatypes import UpdateTaskValuesType  # type: ignore

from .models import Task
from .schemas import TaskSchema, CreateTaskSchema

# from .datatypes import UpdateTaskValuesType

# modelo de dados das tarefas para SQL
tasks = Task


def create_task(db: Session, task: CreateTaskSchema):
    """
    Cria uma nova tarefa a partir dos dados enviados via API.
    """
    # cria um novo registro de tarefa e o insere no banco
    new_task = Task(**task.dict())
    db.add(new_task)
    db.commit()

    # recarrega os dados da tarefa antes de enviá-lo de volta
    db.refresh(new_task)

    return new_task


def retrieve_all_tasks(db: Session) -> Generator:
    """
    Retorna todos os registros das tarefas.
    """
    # pega tudo o que tem no banco de dados e envia...
    return db.query(tasks).all()


def retrieve_task(db: Session, task_id: int):
    """
    Retorna o registro de uma tarefa a partir do seu _id_.
    """
    # pega apenas uma tarefa com o id correto e o envia
    return db.query(tasks).filter(tasks.id == task_id).first()


def update_task(
    db: Session, task_id: int, values: UpdateTaskValuesType
):
    """
    Atualiza o registro de uma tarefa a partir do seu _id_ usando os
    novos valores em `values`.
    """
    # verifica se a tarefa existe...
    task = retrieve_task(db, task_id)

    if task:
        # altera os valores e submete as alterações
        db.query(tasks).filter(tasks.id == task_id).update(values)
        db.commit()

        # atualiza o conteúdo antes de enviá-lo de volta
        db.refresh(task)

        return task


def remove_task(db: Session, task_id: int) -> bool:
    """
    Remove o registro de uma tarefa a partir do seu _id_.
    """
    # verifica se a tarefa existe...
    task = retrieve_task(db, task_id)
        # daí o apaga do banco de dados

    if task:
        db.delete(task)
        db.commit()

        # retorna `True`, tarefa exisita e foi apagado
        return True

    # retorna `False`
    return False

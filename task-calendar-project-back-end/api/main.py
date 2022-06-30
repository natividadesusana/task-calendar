"""
Arquivo principal da API contendo os métodos HTTP implementados.
"""
from typing import Dict, Generator
from datetime import datetime

from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session  # type: ignore

from .crud import (
    create_task,
    remove_task,
    update_task,
    retrieve_task,
    retrieve_all_tasks
)
from .schemas import CreateTaskSchema, UpdateTaskSchema
from .database import Base, SessionLocal, engine
from .datatypes import TaskType

# instancia o FastAPI
app = FastAPI()

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

Base.metadata.create_all(bind=engine)


def get_db() -> Generator:
    """
    Retorna a sessão de conexão do banco de dados.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/tasks/", status_code=status.HTTP_200_OK)
def get_all_tasks(db: Session = Depends(get_db)) -> Generator:
    """
    Retorna todas as tarefas armazenadas.
    """

    result = retrieve_all_tasks(db)

    if result:
        return result

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Não existem tarefas cadastradas.",
    )


@app.get("/tasks/{task_id}/", status_code=status.HTTP_200_OK,)
def get_task(task_id: int, db: Session = Depends(get_db)) -> TaskType:
    """
    Retorna os dados da tarefa, recebe o _id_ da tarefa em `task_id`
    e retorna as informações armazenadas ou gera uma exceção caso não seja
    encontrado.
    """
    result = retrieve_task(db, task_id)
    
    if result:
        return result

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Tarefa de 'id={task_id}' não encontrada.",
    )


@app.delete("/tasks/{task_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)) -> None:
    """
    Remove uma tarefa do banco de dados, recebe o _id_ da tarefa em
    `task_id` e retorna uma mensagem de sucesso, caso contrário gera uma
    exceção de não encontrada.
    """
    if not remove_task(db, task_id):

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task de 'id={task_id}' não encontrado.",
        )


@app.post("/tasks/", status_code=status.HTTP_201_CREATED,)
def post_task(task: CreateTaskSchema, db: Session = Depends(get_db)) -> TaskType:
    """
    Insere uma nova tarefa no banco de dados, recebe todos os campos
    necessários, valida e insere no banco de dados. Retorna o registro
    inserido acrescido do seu `id`.
    """
    result = create_task(db, task)

    if result:
        return result

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST
    )


@app.put("/tasks/{task_id}/", status_code=status.HTTP_201_CREATED)
def put_task(task_id: int, task: UpdateTaskSchema, db: Session = Depends(get_db)) -> TaskType:
    """
    Atualiza os dados de uma tarefa, recebe o _id_  em `task_id` e a
    lista de campos a modificar dentro do JSON (campos com valor `None`
    serão ignorados).
    """
    result = update_task(
        db, task_id, {key: value for key, value in task if value}
    )
        
    if result:
        return result

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Tarefa de 'id={task_id}' não encontrada.",
    )

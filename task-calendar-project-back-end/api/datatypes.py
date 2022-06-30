"""
Tipos de dados customizados usados na aplicação.
"""
from typing import Dict, List, Union

TaskType = Dict[str, Union[float, int, str]]
TaskListType = List[TaskType]

UpdateTaskValuesType = Dict[str, Union[int, str]]

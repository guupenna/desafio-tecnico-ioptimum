from dataclasses import dataclass
from typing import Optional

@dataclass
class Tarefa:
    nome: str
    habilidade: str
    duracao: int
    qtd: int
    horas: int  # adiciona atributo de total de horas da habilidade na tarefa

@dataclass
class OS:
    id: str
    tarefas: list[Tarefa]
    condicao: str
    prioridade: str
    pred: Optional[str]     # pode ter valores nulos
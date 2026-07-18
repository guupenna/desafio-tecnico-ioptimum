from dataclasses import dataclass
from typing import Optional

@dataclass
class Tarefa:
    nome: str
    habilidade: str
    duracao: int
    qtd: int

    # calcula atributo de total de horas da habilidade na tarefa
    @property
    def horas(self) -> int:
        return self.duracao * self.qtd


@dataclass
class OS:
    id: str
    tarefas: list[Tarefa]
    condicao: str
    prioridade: str
    pred: Optional[str]     # pode ter valores nulos

    # calcula atributo de total de horas de habilidade de todas tarefas da OS
    @property
    def horas_total(self) -> int:
        return sum(t.horas for t in self.tarefas)
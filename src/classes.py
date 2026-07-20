"""
Classes para guardar os dados de OS e das tarefas que fazem parte delas
"""

from dataclasses import dataclass

@dataclass
class Tarefa:
    """
    Uma tarefa de uma OS com a habilidade que ela usa e quantas horas dela usa
    """

    nome: str
    habilidade: str
    duracao: int
    qtd: int

    @property
    def horas(self) -> int:
        """
        Horas de habilidade consumidas pela tarefa (duração x quantidade)
        """
        return self.duracao * self.qtd


@dataclass
class OS:
    """
    Uma OS com suas tarefas, prioridade e restrições de condição (parada ou operando) e predecessora
    """

    id: str
    tarefas: list[Tarefa]
    condicao: str
    prioridade: str
    pred: str | None    # pode ter valores nulos

    @property
    def horas_total(self) -> int:
        """
        Total de horas de habilidade de todas tarefas da OS
        """
        return sum(t.horas for t in self.tarefas)
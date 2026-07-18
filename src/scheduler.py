from classes import OS


"""
    Constroi layout de uma OS

    Recebe OS e dia de inicio e monta um layout, que é basicamente a disposição das tarefas da OS nos dias a partir do dia de inicio

    Parameters:
    os (OS): objeto contendo os dados de uma OS
    dia_inicio (int): dia de inicio da OS passada como parametro

    Returns:
    dict[tuple[int, str], int]: horas consumidas de cada habilidade da OS em cada dia
"""
def layout_os(os: OS, dia_inicio: int) -> dict[tuple[int, str], int]:
    consumo_dia = {}
    livre = 8
    dia = dia_inicio

    for tarefa in os.tarefas:
        restante = tarefa.horas

        while restante > 0:
            if dia > 5:
                return None
            
            horas_gastas = min(restante, livre)
            
            consumo_dia[(dia, tarefa.habilidade)] = consumo_dia.get((dia, tarefa.habilidade), 0) + horas_gastas

            restante -= horas_gastas
            livre -= horas_gastas

            if livre == 0:
                dia += 1
                livre = 8

    return consumo_dia
            

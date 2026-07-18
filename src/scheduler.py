from classes import OS


def layout_os(
        os: OS,
        dia_inicio: int
) -> dict[tuple[int, str], int] | None:
    """
    Constroi layout de uma OS

    Recebe OS e dia de inicio e monta um layout, que é basicamente a disposição das tarefas da OS nos dias a partir do dia de inicio

    Parameters:
    os (OS): objeto contendo os dados de uma OS
    dia_inicio (int): dia de inicio da OS passada como parametro

    Returns:
    dict[tuple[int, str], int] | None: horas consumidas de cada habilidade da OS em cada dia
    """
    consumo_os = {}
    livre = 8
    dia = dia_inicio

    for tarefa in os.tarefas:
        restante = tarefa.horas

        while restante > 0:
            if dia > 5:
                return None
            
            horas_usadas = min(restante, livre)
            
            consumo_os[(dia, tarefa.habilidade)] = consumo_os.get((dia, tarefa.habilidade), 0) + horas_usadas

            restante -= horas_usadas
            livre -= horas_usadas

            if livre == 0:
                dia += 1
                livre = 8

    return consumo_os
   


def verifica_consumo(
        consumo_os: dict[tuple[int, str], int], horas_disponiveis: dict[int, dict[str, int]]
) -> bool:
    """
    Verifica se horas usadas pelas tarefas da OS cabem nas horas disponíveis 
    """
    for (dia, habilidade), horas_usadas in consumo_os.items():
        if horas_usadas > horas_disponiveis[dia][habilidade]:
            return False
        
    return True


def verifica_parada(
        os: OS,
        consumo_os: dict[tuple[int, str], int],
        paradas: set{int}
) -> bool:
    """
    Verifica se os dias ocupados por uma OS de parada são apenas os dias de parada
    """
    if os.condicao != 'Parada':
        return True
    
    dias_ocupados = {dia for (dia, _) in consumo_os}

    return dias_ocupados.issubset(paradas)



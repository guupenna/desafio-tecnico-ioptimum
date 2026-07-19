from classes import OS
from copy import deepcopy

PRIORIDADE_RANKING = {'Z': 0, 'A': 1, 'B': 2, 'C': 3}

def layout_os(
        os: OS,
        dia_inicio: int
) -> dict[tuple[int, str], int] | None:
    """
    Constroi layout de uma OS

    Recebe OS e dia de inicio e monta um layout, que é basicamente a disposição das tarefas da OS nos dias a partir do dia de inicio

    Args:
    os (OS): dados de uma OS
    dia_inicio (int): dia de inicio da OS passada como parametro

    Return:
    dict[tuple[int, str], int] | None: horas consumidas de cada habilidade da OS em cada dia a partir do dia de inicio
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
        paradas: set[int]
) -> bool:
    """
    Verifica se os dias ocupados por uma OS de parada são apenas os dias de parada.
    """
    if os.condicao != 'Parada':
        return True
    
    dias_ocupados = {dia for (dia, _) in consumo_os}

    return dias_ocupados.issubset(paradas)



def build_schedule(
        os_list: list[OS],
        recursos_dict: dict[int, dict[str, int]], paradas_set: set[int]
) -> tuple[dict[str, int], dict[str, int], dict[int, dict[str, int]]]:
    """
    Obtem solução inicial de disposição de dias de início para cada OS

    Args:
    os_list (list[OS]): dados de todas as OS
    recursos_dict (dict[int, dict[str, int]]): horas disponiveis de cada habilidade em cada dia
    paradas_set (set[int]): dias de parada

    Returns:
    tuple[dict[str, int], dict[str, int], dict[int, dict[str, int]]]: dias de início para cada OS, dia de fim para cada OS e capacidade restante de cada hora de habilidade dada a alocação de dias
    """

    # copia dicionario de recursos usando deepcopy para garantir que o dicionario interno tambem seja copiado
    capacidade = deepcopy(recursos_dict)

    # cria lista de OS ordenada pelos critérios de, respectivamente, prioridade e horas totais, os dois em ordem crescente
    os_ordenada = sorted(os_list, key=lambda os: (PRIORIDADE_RANKING[os.prioridade], os.horas_total))

    solucao = {}

    # define dicionario usado para lidar com a restrição de predecessora, verificando onde a predecessora acabou por meio deste
    dia_fim = {}

    # define flag usada para marcar se houve alocação de OS na iteração
    # é feito isso para tratar casos que é alocada uma OS que tem predecessora, mas a predecessora está mais à frente na lista ordenada 
    houve_progresso = True

    while houve_progresso:
        houve_progresso = False

        for os in os_ordenada:
            if os.id in solucao:
                continue

            if os.pred is None:
                dia_min = 1
            else:
                if os.pred not in solucao:
                    continue

                # define o dia minimo de inicio da OS como o dia seguinte ao fim da predecessora
                dia_min = dia_fim[os.pred] + 1

            # itera por cada dia possível (dia mínimo de início até o último dia da semana, dia 5)
            for dia_inicio in range(dia_min, 6):
                consumo_os = layout_os(os, dia_inicio)

                # verifica se o consumo da OS não cabe começando do dia de início
                if consumo_os is None:
                    continue

                if not verifica_parada(os, consumo_os, paradas_set):
                    continue

                if not verifica_consumo(consumo_os, capacidade):
                    continue

                # subtrai a as horas usadas por cada dia e cada habilidade da OS pela da capacidade atual
                for (d, habilidade), horas in consumo_os.items():
                    capacidade[d][habilidade] -= horas

                # atribui dia de fim como o maior valor de dia para os dias de execução de tarefas da OS
                dia_fim[os.id] = max(d for d,_ in consumo_os)

                solucao[os.id] = dia_inicio

                houve_progresso = True

                break

    return solucao, dia_fim, capacidade
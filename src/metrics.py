"""
Cálculo da métricas de resultado exigidas na especificação do desafio
"""

from classes import OS

def calculate_metrics(
        solucao: dict[str, int],
        os_dict: dict[str, OS],
        recursos_dict: dict[int, dict[str, int]],
        capacidade_restante: dict[int, dict[str, int]]
) -> dict:
    """
    Calcula métricas de resultado da programação

    Args:
    solucao: OS programads e seu dia de início
    os_dict: dicionário de OS com o id da OS como chave
    recursos_dict: horas disponíveis de cada habilidade em cada dia
    capacidade_restante: o que sobrou das horas depois da programação das OS

    Returns:
    O dicionário metrics da saída pedida na especificação, com número total de OS programadas, número de OS programadas para cada prioridade e percentual de utilização de cada habilidade (e todos os valores como string)
    """

    n_os = len(solucao)

    # inicializa as quatro chaves para que uma prioridade sem nenhuma OS programada seja 0 em vez de não aparecer
    cont = {'Z': 0, 'A': 0, 'B': 0, 'C': 0}

    for os_id in solucao.keys():
        prioridade_os = os_dict[os_id].prioridade
        cont[prioridade_os] += 1

    # soma as horas disponíveis de cada habilidade por todos os dias da semana
    total = {}

    for dia in recursos_dict:
        for habilidade in recursos_dict[dia]:
            total[habilidade] = total.get(habilidade, 0) + recursos_dict[dia][habilidade]

    # tambem a mesma soma, mas agora com o que sobrou
    restante = {}

    for dia in capacidade_restante:
        for habilidade in capacidade_restante[dia]:
            restante[habilidade] = restante.get(habilidade, 0) + capacidade_restante[dia][habilidade]

    # o que foi usado é total - restante
    utilizacao = {}

    for habilidade in total:
        if total[habilidade] == 0:
            porcentagem = 0
        else:
            porcentagem = 100 * (total[habilidade] - restante[habilidade]) / total[habilidade]
        
        utilizacao[habilidade] = f'{porcentagem:.0f}%'

    metrics = {
        'n_os': str(n_os),
        'n_Z': str(cont['Z']),
        'n_A': str(cont['A']),
        'n_B': str(cont['B']),
        'n_C': str(cont['C']),
        'utilization': utilizacao
    }

    return metrics
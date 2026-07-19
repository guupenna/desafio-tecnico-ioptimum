from classes import OS


def calculate_metrics(
        solucao: dict[str, int],
        os_dict: dict[str, OS],
        recursos_dict: dict[int, dict[str, int]],
        capacidade_restante: dict[int, dict[str, int]]
) -> dict:
    """
    Calcula metricas e preenche dicionario com os valores (n_os, n_Z, n_A, n_B, n_C e utilization)
    """

    metrics = {}

    n_os = len(solucao)

    cont = {'Z': 0, 'A': 0, 'B': 0, 'C': 0}

    for os_id in solucao.keys():
        prioridade_os = os_dict[os_id].prioridade
        cont[prioridade_os] += 1

    # registra no dicionario a soma de horas de cada habilidade, salvas em recursos
    total = {}

    for dia in recursos_dict:
        for habilidade in recursos_dict[dia]:
            total[habilidade] = total.get(habilidade, 0) + recursos_dict[dia][habilidade]

    # registra no dicionario a soma de horas restante de cada habilidade, salvas em capacidade_restante
    restante = {}

    for dia in capacidade_restante:
        for habilidade in capacidade_restante[dia]:
            restante[habilidade] = restante.get(habilidade, 0) + capacidade_restante[dia][habilidade]

    # cria e preenche dicionario utilizacao com a porcentagem calculada
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
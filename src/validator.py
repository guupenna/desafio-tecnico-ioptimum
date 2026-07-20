"""
Validação independente da solução gerada pelo scheduler

O validador não usa as funções de scheduler.py pois um erro dentro delas passaria despercebido no validador, por isso a ocupação de cada OS é calculada novamente mas de outro jeito. Nesse caso, em vez do loop que vai preenchendo 8h por dia, as tarefas viram uma lista em que cada item representa a execução em 1 hora e o dia é extraído dividindo o índice da tarefa por 8 (8h em um dia).
"""

from classes import OS

def _ocupacao_os(
        os: OS,
        dia_inicio: int
) -> dict[tuple[int, str], int]:
    """
    Calcula novamente quantas horas de cada habilidade a OS usa em um dia, mas de outra forma
    """
    
    ocupacao_os = {}

    # inicializa lista de ocupação de habilidades, dispostas como uma inserçao do nome da habilidade para cada hora, em ordem.
    # ex: para OS com T1 com 2h de mecânica e T2 com 1h de elétrica, list = ['Mecânico', 'Mecânico', 'Elétrico']
    ocupacao_habilidades = []

    for tarefa in os.tarefas:
        lista_tarefa = [tarefa.habilidade] * tarefa.horas

        ocupacao_habilidades.extend(lista_tarefa)

    # itera por enumerate(list) para usar indice de cada inserção da lista como hora
    for hora, habilidade in enumerate(ocupacao_habilidades):
        # soma 1 hora ao dia extraido a partir do dia de inicio e hora atual
        dia_da_hora = dia_inicio + hora // 8
        ocupacao_os[(dia_da_hora, habilidade)] = ocupacao_os.get((dia_da_hora, habilidade), 0) + 1

    return ocupacao_os
            

def validate_solution(
        solucao: dict[str, int],
        os_dict: dict[str, OS],
        recursos_dict: dict[int, dict[str, int]],
        paradas_set: set[int]
) -> list[str]:
    """
    Verifica se uma solução respeita todas as restrições do problema

    Args:
    solucao: OS programads e seu dia de início
    os_dict: dicionário de OS com o id da OS como chave
    recursos_dict: horas disponíveis de cada habilidade em cada dia
    paradas_set: dias de parada

    Returns:
    Uma descrição por erro encontrado (não cumprimento da restrição), em que a lista vazia significa solução válida
    """    

    erros = []

    # cria dicionario para acumular uso de horas de habilidade por dia para todas as OS
    uso_total = {}

    for os_id, dia_inicio in solucao.items():
        if os_id not in os_dict:
            erros.append(f"{os_id} não existente")
            continue

        if dia_inicio not in range(1, 6):
            erros.append(f"Dia {dia_inicio} na OS {os_id} não permitido")
            continue

        os = os_dict.get(os_id)

        ocupacao_os = _ocupacao_os(os, dia_inicio)
        
        dias = {d for d,_ in ocupacao_os}

        if max(dias) > 5:
            erros.append(f"{os_id} termina no dia {max(dias)}, acima do limite de dias")

        if os.condicao == 'Parada':
            fora = dias - paradas_set
            if fora:
                erros.append(f"{os_id} de parada ocupa os dias {sorted(fora)} que não são de parada")

        if os.pred is not None:
            if os.pred not in solucao:
                erros.append(f"predecessora de {os_id} não está programada")
            else:
                ocupacao_os_pred = _ocupacao_os(os_dict[os.pred], solucao[os.pred])

                dia_fim_pred = max(d for d,_ in ocupacao_os_pred)

                if dia_fim_pred >= dia_inicio:
                    erros.append(f"predecessora de {os_id} não finalizada")

        # soma as horas usadas por aquela OS no dicionario uso_total, para a respectiva chave (dia, habilidade)
        for (dia, habilidade), horas_usadas in ocupacao_os.items():
            uso_total[(dia, habilidade)] = uso_total.get((dia, habilidade), 0) + horas_usadas

    # itera pelo dicionario uso_total para verificar se não viola a restrição de capacidade de horas para cada habilidade em cada dia da semana
    for (dia, habilidade), horas_usadas in uso_total.items():
        if dia not in recursos_dict:
            continue

        horas_disponiveis = recursos_dict[dia][habilidade]

        if horas_usadas > horas_disponiveis:
            erros.append(f"dia {dia}, habilidade {habilidade}: {horas_usadas}h usadas excedem as {horas_disponiveis}h disponíveis")

    return erros


from classes import OS

def _ocupacao_os(
        os: OS,
        dia_inicio: int
) -> dict[tuple[int, str], int]:
    """
    Funçao helper usado para construir abordagem diferente para verificar disposição de tarefas de uma OS
    """
    
    # inicializa dicionario que acumula as horas consumidas em cada dia para cada habilidade da OS
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
    Verifica se uma solução cumpre as restrições do problema utilizando uma modelagem diferente da construção da solução Retorna uma lista com os problemas encontrados (lista vazia = soluçao valida)
    """    

    erros = []

    # cria dicionario para acumular uso de horas de habilidade por dia para todas as OS
    uso_total = {}

    for os_id, dia_inicio in solucao.items():
        if os_id not in os_dict:
            erros.append(f"{os_id} não existente")
            continue

        if dia_inicio not in range(1, 6):
            erros.append(f"Dia {dia_inicio} não permitido")
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
                erros.append(f"predecessora de {os_id} não está alocada")
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


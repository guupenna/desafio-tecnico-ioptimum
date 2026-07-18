from classes import OS

def _ocupacao_os(os: OS, dia_inicio: int) -> dict[tuple[int, str], int]:
    """
    Abordagem diferente para verificar disposição de tarefas de uma OS
    """
    
    # inicializa dicionario de tarefas da OS que será retornado identico ao feito no scheduler caso nao haja divergencias
    ocupacao_os = {}

    # inicaliza lista de ocupação de habilidades, dispostas como uma inserçao do nome da habilidade para cada hora, em ordem.
    # ex: para OS com T1 com 2h de mecânica e T2 com 1h de elétrica, list = ['Mecânica', 'Mecânica', 'Elétrica']
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
            


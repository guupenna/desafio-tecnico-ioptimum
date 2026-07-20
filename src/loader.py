"""
Leitura do Excel do desafio e montagem das classes do projeto
"""

import pandas as pd
from pathlib import Path
from classes import Tarefa, OS

def load_data(excel_path: str) -> tuple[
    list[OS],
    dict[str, OS],
    dict[int, dict[str, int]],
    set[int]
]:
    """
    Lê o Excel do desafio e monta as classes usadas pelo restante do projeto

    Args:
    excel_path: caminho do .xlsx com as abas OS, Tarefas, Recursos e Paradas

    Returns:
    Lista de OS, dicionário de OS com o id da OS como chave, horas disponíveis de cada habilidade em cada dia, e os dias de parada 
    """

    # lê cada aba do arquivo excel como um dataframe
    os_df = pd.read_excel(excel_path, sheet_name='OS')
    tarefas_df = pd.read_excel(excel_path, sheet_name='Tarefas')
    recursos_df = pd.read_excel(excel_path, sheet_name='Recursos')
    paradas_df = pd.read_excel(excel_path, sheet_name='Paradas')

    # agrupa as tarefas por OS de uma vez só, evitando varrer o dataframe uma vez por OS
    tarefas_os_dict = {}

    for os_id, grupo in tarefas_df.groupby('OS'):
        lista_tarefas = [
            Tarefa(
                nome=tarefa['Tarefa'],
                habilidade=tarefa['Habilidade'],
                duracao=tarefa['Duração'],
                qtd=tarefa['Quantidade']
            )

            for _, tarefa in grupo.iterrows()
        ]

        tarefas_os_dict[os_id] = lista_tarefas

    # cria uma lista de objetos OS com o atributo 'tarefas' sendo as tarefas daquela OS estruturadas em lista
    os_list = []

    for _, linha in os_df.iterrows():
        os_obj = OS(
            id=linha['OS'],
            tarefas=tarefas_os_dict.get(linha['OS'], []),
            condicao=linha['Condição'],
            prioridade=linha['Prioridade'],
            pred=None if pd.isna(linha['Predecessora']) else linha['Predecessora']    # trata valores nulos na coluna 'Predecessora' no momento da criação do objeto 
        )

        os_list.append(os_obj)

    
    # cria dicionário de OS para facilitar acesso indexado O(1)
    os_dict = {os.id: os for os in os_list}

    # organiza recursos (horas de habilidade por dia da semana) em um dicionário de dicionários
    # com a chave sendo o dia da semana, para facilitar acesso de horas de uma habilidade em um dia 
    recursos_dict = {}

    for _, linha in recursos_df.iterrows():
        dia_num = int(linha['Dia'].split('_')[1])

        habilidade = linha['Habilidade']
        horas = linha['HH_Disponivel']

        if dia_num not in recursos_dict:
            recursos_dict[dia_num] = {}

        recursos_dict[dia_num][habilidade] = horas

    # usa set para organizar paradas por questão de simplicidade de uso
    paradas_set = set(paradas_df['Dia'])

    return os_list, os_dict, recursos_dict, paradas_set
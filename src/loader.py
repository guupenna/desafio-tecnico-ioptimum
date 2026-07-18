import pandas as pd
from classes import Tarefa, OS

def load_data(excel_path):
    # Lê cada aba do arquivo Excel como um dataframe
    os_df = pd.read_excel(excel_path, sheet_name='OS')
    tarefas_df = pd.read_excel(excel_path, sheet_name='Tarefas')
    recursos_df = pd.read_excel(excel_path, sheet_name='Recursos')
    paradas_df = pd.read_excel(excel_path, sheet_name='Paradas')

    # Dicionário de tarefas criado para otimizar a busca de tarefas pertencentes à OS específica ao preencher o atributo 'tarefas' da classe OS
    tarefas_os_dict = {}

    for os_id, grupo in tarefas_df.groupby('OS'):
        lista_tarefas = [
            Tarefa(
                nome=tarefa['Tarefa'],
                habilidade=tarefa['Habilidade'],
                duracao=tarefa['Duração'],
                qtd=tarefa['Quantidade'],
                horas=tarefa['Duração']*tarefa['Quantidade']
            )

            for _, tarefa in grupo.iterrows()
        ]

        tarefas_os_dict[os_id] = lista_tarefas

    # Cria uma lista de objetos OS com o atributo 'tarefas' sendo as tarefas daquela OS estruturadas em lista
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

    
    # Cria dicionário de OS para facilitar acesso indexado O(1)
    os_dict = {os.id: os for os in os_list}

    # Organiza recursos (horas de habilidade por dia da semana) em um dicionário de dicionários
    # com a chave sendo o dia da semana, para facilitar acesso de horas da habilidade no dia 
    recursos_dict = {}

    for _, linha in recursos_df.iterrows():
        dia_num = int(linha['Dia'].split('_')[1])

        habilidade = linha['Habilidade']
        horas = linha['HH_Disponivel']

        if dia_num not in recursos_dict:
            recursos_dict[dia_num] = {}

        recursos_dict[dia_num][habilidade] = horas

    # Usa set para organizar paradas por questão de simplicidade de uso
    paradas_set = set(paradas_df['Dia'])

    return os_list, os_dict, recursos_dict, paradas_set
import pandas as pd
from collections import defaultdict

# Lê cada aba do arquivo Excel como um dataframe
def load_data(excel_path):
    os_df = pd.read_excel(excel_path, sheet_name='OS')
    tarefas_df = pd.read_excel(excel_path, sheet_name='Tarefas')
    recursos_df = pd.read_excel(excel_path, sheet_name='Recursos')
    paradas_df = pd.read_excel(excel_path, sheet_name='Paradas')

    return os_df, tarefas_df, recursos_df, paradas_df

os_df, tarefas_df, recursos_df, paradas_df = load_data('../data/backlog_desafio_500.xlsx')

# print(df_os, df_tarefas, recursos_df, paradas_df)

# Dicionario de OS
os = {
    'os1': {
        'prioridade': 'Z',
        'tarefas' : [ {
            'nome': 't1',
            'habilidade': 'mecanica',
            'duracao': 15,
            'quantidade': 2,
            'horas': 1
            }
        ],
        'parada': True, 
        'predecessora': 'OS2'
    }
}

# Cria dicionário para tarefas, onde a chave é o id da OS
tarefas_por_os = {}

for os_id, grupo in tarefas_df.groupby('OS'):
    tarefas_por_os[os_id] = [
        {
            'nome': tarefa['Tarefa'],
            "habilidade": tarefa['Habilidade'],
            'duracao': tarefa['Duração'],
            'qtd': tarefa['Quantidade'],
            'horas': tarefa['Duração'] * tarefa['Quantidade'] # item que representa as horas totais da habilidade na tarefa
        }
        for _, tarefa in grupo.iterrows()
    ]

# Cria dicionário para OS, onde o valor da chave tarefas é uma lista
#  de dicionários de tarefa
os_dict = {}

for _, linha in os_df.iterrows():
    os_dict[linha['OS']] = {
        'tarefas': tarefas_por_os[linha['OS']],
        'condicao': linha['Condição'],
        'prioridade': linha['Prioridade'],
        'pred': linha['Predecessora']
    }
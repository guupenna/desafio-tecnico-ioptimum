from pathlib import Path
from loader import load_data

def create_solution(excel_path):
    pass

if __name__ == '__main__':
    diretorio_atual = Path(__file__).resolve().parent.parent
    excel_path = diretorio_atual / 'data' / 'backlog_desafio_500.xlsx'
    os_list, recursos_dict, paradas_set = load_data(excel_path)
    print(os_list[1])
    print(recursos_dict[1])
    print(paradas_set)
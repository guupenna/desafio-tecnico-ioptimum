from pathlib import Path
from loader import load_data
from scheduler import build_schedule
from metrics import calculate_metrics
from validator import validate_solution
import json


def create_solution(excel_path):
    os_list, os_dict, recursos_dict, paradas_set = load_data(excel_path)

    solucao, dia_fim, capacidade = build_schedule(os_list, recursos_dict, paradas_set)

    metrics = calculate_metrics(solucao, os_dict, recursos_dict, capacidade)

    erros = validate_solution(solucao, os_dict, recursos_dict, paradas_set)

    output_solution = {
        'solution': {os_id: str(dia) for os_id, dia in solucao.items()},
        'metrics': metrics,
        'extras': {
            'observations': '',
            'plots': '',
            'any_additional_information': ''
        }
    }

    return output_solution


if __name__ == '__main__':
    diretorio_atual = Path(__file__).resolve().parent.parent
    excel_path = diretorio_atual / 'data' / 'backlog_desafio_500.xlsx'
    output_solution = create_solution(excel_path)

    print(json.dumps(output_solution, indent=4, ensure_ascii=False))
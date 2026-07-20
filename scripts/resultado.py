"""
Roda a heurística nos três backlogs e imprime a tabela de resultados

Serve como fonte única dos números citados no README e no relatório para que documento e código não sejam diferentes
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))

from loader import load_data
from scheduler import build_schedule
from metrics import calculate_metrics
from validator import validate_solution

BACKLOGS = ('500', '1000', '2000')


def _roda(nome: str) -> dict:
    """
    Executa o pipeline num backlog e pega os números para preencher o relatório
    """
    os_list, os_dict, recursos_dict, paradas_set = load_data(
        Path(__file__).resolve().parent.parent / 'data' / f'backlog_desafio_{nome}.xlsx'
    )

    solucao, _, capacidade = build_schedule(os_list, recursos_dict, paradas_set)

    metrics = calculate_metrics(solucao, os_dict, recursos_dict, capacidade)

    erros = validate_solution(solucao, os_dict, recursos_dict, paradas_set)

    # separa as não programadas pelo motivo de terem ficado de fora
    teto = len(recursos_dict) * 8
    fora = [o for o in os_list if o.id not in solucao]
    excede_teto = [o for o in fora if o.horas_total > teto]
    pred_fora = [o for o in fora if o.horas_total <= teto and o.pred and o.pred not in solucao]

    return {
        'total': len(os_list),
        'metrics': metrics,
        'erros': len(erros),
        'fora': len(fora),
        'excede_teto': len(excede_teto),
        'pred_fora': len(pred_fora),
        'sem_espaco': len(fora) - len(excede_teto) - len(pred_fora),
    }


if __name__ == '__main__':
    resultados = {nome: _roda(nome) for nome in BACKLOGS}

    print('PROGRAMAÇÃO')
    print('backlog   programadas     Z     A     B     C   violações')
    for nome, r in resultados.items():
        m = r['metrics']

        print(f'{nome:>7}   {m["n_os"]:>4} / {r["total"]:<5}   '
              f'{m["n_Z"]:>3}   {m["n_A"]:>3}   {m["n_B"]:>3}   {m["n_C"]:>3}   '
              f'{r["erros"]:>9}')

    print('\nUTILIZAÇÃO POR HABILIDADE')
    print('backlog   Mecânico   Elétrico   Lubrificador   Soldador')
    for nome, r in resultados.items():
        u = r['metrics']['utilization']

        print(f'{nome:>7}   {u["Mecânico"]:>8}   {u["Elétrico"]:>8}   '
              f'{u["Lubrificador"]:>12}   {u["Soldador"]:>8}')

    print('\nPOR QUE AS OS FICARAM DE FORA')
    print('backlog     fora   usada > disponivel   pred. fora   sem espaço')
    for nome, r in resultados.items():
        fora = r['fora']

        teto_txt = f'{r["excede_teto"]} ({100 * r["excede_teto"] / fora:.0f}%)'
        pred_txt = f'{r["pred_fora"]} ({100 * r["pred_fora"] / fora:.0f}%)'
        espaco_txt = f'{r["sem_espaco"]} ({100 * r["sem_espaco"] / fora:.0f}%)'

        print(f'{nome:>7}   {fora:>6}   {teto_txt:>18}   {pred_txt:>10}   {espaco_txt:>10}')

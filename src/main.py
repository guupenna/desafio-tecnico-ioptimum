"""
Monta a programação semanal de manutenção e devolve resultado no formato pedido de output_solution
"""

import json
from pathlib import Path

from loader import load_data
from scheduler import build_schedule
from metrics import calculate_metrics
from validator import validate_solution
from plots import gera_plots


def create_solution(excel_path: str) -> dict:
    """
    Gera a programação semanal de OS a partir do Excel

    Executa as 4 etapas do projeto em sequência: carrega dados, constrói solução pela heurística gulosa, calcula métricas e valida resultado

    Args:
    excel_path: caminho do .xlsx com a entrada (backlog)

    Returns:
    Dicionário output_solution no formato da especificação do desafio, com as chaves solution (valor: OS e seu dia de início), metrics (contagens e porcentagem de utilização) e extras (observações, plots e informações adicionais)
    """

    os_list, os_dict, recursos_dict, paradas_set = load_data(excel_path)

    solucao, dia_fim, capacidade = build_schedule(os_list, recursos_dict, paradas_set)

    metrics = calculate_metrics(solucao, os_dict, recursos_dict, capacidade)

    erros = validate_solution(solucao, os_dict, recursos_dict, paradas_set)

    plots = gera_plots(solucao, os_dict, recursos_dict, capacidade)

    # calculados na hora porque variam de acordo com o backlog escolhido como entrada
    teto_semana = len(recursos_dict) * 8
    demanda_total = sum(o.horas_total for o in os_list)
    capacidade_total = sum(h for dia in recursos_dict.values() for h in dia.values())
    nao_programadas = [o for o in os_list if o.id not in solucao]
    excedem_teto = [o for o in nao_programadas if o.horas_total > teto_semana]


    output_solution = {
        'solution': {os_id: str(dia) for os_id, dia in solucao.items()},
        'metrics': metrics,
        'extras': {
            'observations': (
                f'A demanda supera muito a capacidade, pois são {demanda_total}h de trabalho no '
                f'backlog para {capacidade_total}h disponíveis na semana, ou seja, dá para '
                f'atender só {100 * capacidade_total / demanda_total:.1f}% do que existe. Por '
                f'isso o problema é escolher bem quais OS entram na solução, não encaixar todas, portanto deixar '
                f'a maioria de fora é o resultado esperado. '
                f'O que mais limita não é a quantidade de horas de habilidade disponíveis, e sim o teto de 8h por dia de cada OS: '
                f'{len(excedem_teto)} das {len(nao_programadas)} OS que ficaram de fora '
                f'({100 * len(excedem_teto) / len(nao_programadas):.0f}%) precisam de mais de '
                f'{teto_semana}h, então não caberiam na semana nem se houvesse mais horas de habilidade '
                f'disponível, tanto que sobra hora em todas as habilidades depois da programação de OS.'
            ),
            'plots': plots,
            'any_additional_information': {
                'metodo': (
                    'Heurística gulosa que monta a programação uma OS por vez. A ordem segue a prioridade (Z > A > B > C) e quando há '
                    'empate a OS que usa menos horas entra primeiro. Assim, o processo repete até não '
                    'conseguir encaixar mais nada, o que resolve a questão das predecessoras.'
                ),
                'premissas': [
                    'Uma tarefa gasta duração x quantidade em horas e esse número conta duas '
                    'vezes, uma no tempo que a OS leva e outra no que ela consome da habilidade. Além disso, não '
                    'foi considerado paralelismo.',

                    'Cada OS entra na programação uma vez só em um único dia de início e se passar '
                    'de 8h de trabalho ela continua nos dias seguintes.',

                    'OS de parada ficam restritas aos dias de parada e as de operando podem cair '
                    'em qualquer dia.',

                    'Uma OS sucessora só começa depois que a sua predecessora acaba, do dia seguinte em '
                    'diante. Além disso, se a predecessora não entrou, a sucessora fica de fora junto.',
                ],
                'validacao': (
                    f'Quantidade de erros: {len(erros)}. A verificação é feita por um validador independente '
                    f'que refaz as contas em vez de reutilizar o código que gerou '
                    f'a solução. Esse validador checa se cada OS aparece uma vez só, se as de parada estão em '
                    f'dias de parada, se as horas cabem na capacidade de cada dia, se as '
                    f'predecessoras terminam antes e se nenhuma OS passa do quinto dia.'
                ),
            },
        }
    }

    return output_solution


if __name__ == '__main__':
    diretorio_atual = Path(__file__).resolve().parent.parent
    excel_path = diretorio_atual / 'data' / 'backlog_desafio_500.xlsx'
    output_solution = create_solution(excel_path)

    print(json.dumps(output_solution, indent=4, ensure_ascii=False))
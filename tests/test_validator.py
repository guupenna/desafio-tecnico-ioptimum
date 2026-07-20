"""
Testes do validador, executados a partir de uma solução modificada

Para provar que o validador realmente funciona, cada teste parte da solução válida gerada pelo scheduler, modifica para quebrar uma restrição de propósito e afirma que a violação correspondente apareceu
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))

from loader import load_data
from scheduler import build_schedule
from validator import validate_solution


def _cenario_valido():
    """
    Carrega os dados e gera solução base para todos os testes
    """

    diretorio_atual = Path(__file__).resolve().parent.parent
    excel_path = diretorio_atual / 'data' / 'backlog_desafio_500.xlsx'

    os_list, os_dict, recursos_dict, paradas_set = load_data(excel_path)

    solucao, _, _ = build_schedule(os_list, recursos_dict, paradas_set)

    return solucao, os_dict, recursos_dict, paradas_set


def test_solucao_valida_sem_erros():
    """
    Solução válida não deve gerar erros
    """

    solucao, os_dict, recursos_dict, paradas_set = _cenario_valido()

    erros = validate_solution(solucao, os_dict, recursos_dict, paradas_set)

    assert erros == [], f'solução válida acusou os erros {erros}'
    

def test_os_de_parada_em_dia_invalido():
    """
    Deve acusar OS de parada em dia que não é de parada
    """

    solucao, os_dict, recursos_dict, paradas_set = _cenario_valido()

    # copia a solução para não interferir nos proximos testes
    solucao_modificada = dict(solucao)

    # seleciona a primeira OS com condição de parada da solução
    os_id_modificada = next(os_id for os_id in solucao_modificada if os_dict[os_id].condicao == 'Parada')

    # modifica o dia de início da OS para o primeiro dia que não é de parada
    solucao_modificada[os_id_modificada] = next(d for d in range(1, 6) if d not in paradas_set)

    erros = validate_solution(solucao_modificada, os_dict, recursos_dict, paradas_set)

    assert any(os_id_modificada in e and 'parada' in e for e in erros), f'não acusou OS {os_id_modificada} com erro na condição de parada: {erros}'


def test_excede_capacidade():
    """
    Deve acusar capacidade de horas de habilidade excedidas
    """

    solucao, os_dict, recursos_dict, paradas_set = _cenario_valido()
    
    # cria dicionário com dia de início 1 em todas as OS
    solucao_modificada = {os_id: 1 for os_id in solucao}

    erros = validate_solution(solucao_modificada, os_dict, recursos_dict, paradas_set)

    assert any('dia 1' in e and 'excedem' in e for e in erros), f'não acusou que as OS excedem a capacidade no dia 1: {erros}'


def test_sucessora_antes_da_predecessora():
    """
    Deve acusar OS sucessora programada antes da finalização da predecessora
    """

    solucao, os_dict, recursos_dict, paradas_set = _cenario_valido()

    solucao_modificada = dict(solucao)

    os_id_modificada = next(i for i in solucao if os_dict[i].pred and os_dict[i].pred in solucao)

    # altera dia de iníco da OS para o dia de início de sua predecessora
    solucao_modificada[os_id_modificada] = solucao[os_dict[os_id_modificada].pred]

    erros = validate_solution(solucao_modificada, os_dict, recursos_dict, paradas_set)

    assert any(os_id_modificada in e and 'não finalizada' in e for e in erros), f'não acusou que OS sucessora {os_id_modificada} começa no mesmo dia que predecessora: {erros}'


def test_predecessora_nao_programada():
    """
    Deve acusar OS sucessora programada sem que a predecessora esteja programada
    """

    solucao, os_dict, recursos_dict, paradas_set = _cenario_valido()

    solucao_modificada = dict(solucao)

    os_id_modificada = next(i for i in solucao if os_dict[i].pred and os_dict[i].pred in solucao)

    # modifica o dicionário removendo a OS predecessora selecionada
    del solucao_modificada[os_dict[os_id_modificada].pred]

    erros = validate_solution(solucao_modificada, os_dict, recursos_dict, paradas_set)

    assert any(os_id_modificada in e and 'não está programada' in e for e in erros), f'não acusou que OS {os_id_modificada} tem OS predecessora que não está programada: {erros}'


def test_validade_id_e_dia():
    """
    Deve acusar nome não existente e OS com dia não permitido
    """

    solucao, os_dict, recursos_dict, paradas_set = _cenario_valido()
    
    solucao_modificada = dict(solucao)

    # adiciona OS não existente
    solucao_modificada['OS_teste'] = 1
    
    # seleciona uma os para modificar seu dia de início para dia inválido
    os_id_modificada = next(iter(solucao))
    solucao_modificada[os_id_modificada] = 6

    erros = validate_solution(solucao_modificada, os_dict, recursos_dict, paradas_set)
    
    assert any('não existente' in e for e in erros), f'não acusou OS com nome não existente: {erros}'

    assert any(os_id_modificada in e and 'não permitido' in e for e in erros), f'não acusou OS {os_id_modificada} com dia não permitido: {erros}'


def test_os_passa_limite_da_semana():
    """
    Deve acusar OS ultrapassando limite de dias da semana
    """
    solucao, os_dict, recursos_dict, paradas_set = _cenario_valido()

    solucao_modificada = dict(solucao)

    # seleciona os que tem mais de 8 horas, ou seja, usa mais de 1 dia
    os_id_modificada = next(i for i in solucao if os_dict[i].horas_total > 8)

    # modifica dia de início para o último dia da semana para testar a situação de passar do limite de dias
    solucao_modificada[os_id_modificada] = 5

    erros = validate_solution(solucao_modificada, os_dict, recursos_dict, paradas_set)

    assert any(os_id_modificada in e and 'limite de dias' in e for e in erros), f'não acusou OS {os_id_modificada} que passa do limite de dias da semana: {erros}'


if __name__ == '__main__':
    # varre todo o módulo procurando as funções test_* e executa cada uma
    for nome, f in list(globals().items()):
        if nome.startswith('test_'):
            f()
            print(f'passou {nome}')
    print('todos os testes passaram')
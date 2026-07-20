import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path


CORES = {
    'Mecânico': "#a55a0e",
    'Elétrico': "#c9a20b",
    'Lubrificador': "#1988d3",
    'Soldador': "#d81c1c",
}
GRADE = '#e5e5e5'
CONTEXTO = '#c8c8c8'
REF = '#6b6b6b'
DESTACAR = '#37474f'


def _horas_usadas(recursos_dict, capacidade_restante):
    """
    Função helper para facilitar acesso a horas usadas para cada habilidade em cada dia
    """

    horas_usadas = {}

    for dia in recursos_dict:
        for habilidade in recursos_dict[dia]:
            horas_usadas[(dia, habilidade)] = recursos_dict[dia][habilidade] - capacidade_restante[dia][habilidade]

    return horas_usadas


def gera_plots(solucao, os_dict, recursos_dict, capacidade_restante, caminho='outputs/figs') -> list[str]:
    """
    Gera e salva todos plots necessários, retornando os caminhos
    """
    Path(caminho).mkdir(parents=True, exist_ok=True)
    usado = _horas_usadas(recursos_dict, capacidade_restante)

    destino_fig_1 = _plot_utilizacao(usado, recursos_dict, caminho)
    destino_fig_2 = _plot_prioridades(solucao, os_dict, caminho)
    destino_fig_3 = _plot_ocupacao(usado, recursos_dict, caminho)

    return [destino_fig_1, destino_fig_2, destino_fig_3]


def _plot_utilizacao(usado, recursos_dict, caminho) -> str:
    """
    Plot de porcentagem de utilização por habilidade
    """
    usado_por_habilidade = {}

    for (dia, habilidade), horas in usado.items():
        usado_por_habilidade[habilidade] = usado_por_habilidade.get(habilidade, 0) + horas

    total_por_habilidade = {}

    for dia in recursos_dict:
        for habilidade in recursos_dict[dia]:
            total_por_habilidade[habilidade] = total_por_habilidade.get(habilidade, 0) + recursos_dict[dia][habilidade]

    habilidades = list(CORES)

    percentuais = []

    cores = []

    for h in habilidades:
        percentuais.append(100 * usado_por_habilidade[h] / total_por_habilidade[h])
        cores.append(CORES[h])

    fig, ax = plt.subplots(figsize=(8, 4))
    barras = ax.barh(
        habilidades,
        percentuais,
        color=cores,
        height=0.6
    )
    ax.bar_label(
        barras,
        fmt='%.0f%%',
        padding=3
    )
    ax.axvline(100, color=REF, linestyle='--')
    ax.set_xlim(0, 115)
    ax.grid(axis='x', color=GRADE, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.invert_yaxis()
    ax.set_title('Utilização por habilidade')
    ax.set_xlabel('Utilização (%)')

    destino = Path(caminho) / 'utilizacao_habilidades.png'
    fig.savefig(destino, dpi=150, bbox_inches='tight')
    plt.close(fig)

    return str(destino)


def _plot_prioridades(solucao, os_dict, caminho) -> str:
    """
    Plot de OS programadas por prioridade sobre total
    """
    programadas = {'Z': 0, 'A': 0, 'B': 0, 'C': 0}

    for os_id in solucao.keys():
        prioridade_os = os_dict[os_id].prioridade
        programadas[prioridade_os] += 1

    total_os_prioridade = {'Z': 0, 'A': 0, 'B': 0, 'C': 0}

    for os in os_dict.values():
        total_os_prioridade[os.prioridade] += 1

    prioridades = ['Z', 'A', 'B', 'C']

    valores_totais = [total_os_prioridade[p] for p in prioridades]

    valores_programados = [programadas[p] for p in prioridades]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(
        prioridades,
        valores_totais,
        color=CONTEXTO,
        height=0.6,
        label='Total'
    )
    barras = ax.barh(
        prioridades,
        valores_programados,
        color=DESTACAR,
        height=0.6,
        label='Programadas'
    )
    ax.bar_label(barras, fmt='%d', padding=3)
    ax.legend(frameon=False, loc='upper left')
    ax.grid(axis='x', color=GRADE, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.invert_yaxis()
    ax.set_title('OS programadas por prioridade')
    ax.set_xlabel('Quantidade de OS')

    destino = Path(caminho) / 'os_por_prioridade.png'
    fig.savefig(destino, dpi=150, bbox_inches='tight')
    plt.close(fig)

    return str(destino)


def _plot_ocupacao(usado, recursos_dict, caminho) -> str:
    """
    Plot de horas ocupadas na semana por habilidade em cada dia
    """
    dias = sorted(recursos_dict)

    fig, ax = plt.subplots(figsize=(8, 4))

    acumulado = [0] * len(dias)

    for habilidade in CORES:
        alturas = [usado[(d, habilidade)] for d in dias]

        ax.bar(
            dias,
            alturas,
            bottom=acumulado,
            color=CORES[habilidade],
            label=habilidade,
            edgecolor='white',
            linewidth=2
        )

        acumulado = [a + h for a, h in zip(acumulado, alturas)]

    capacidades = [sum(recursos_dict[d].values()) for d in dias]

    ax.hlines(
        capacidades,
        [d - 0.4 for d in dias],
        [d + 0.4 for d in dias],
        color=REF,
        linewidth=2
    )
    ax.legend(frameon=False)
    ax.set_ylim(0, 160)
    ax.grid(axis='y', color=GRADE, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.set_xticks(dias)
    ax.set_title('Horas alocadas por dia')
    ax.set_xlabel('Dia da semana')
    ax.set_ylabel('Horas')

    destino = Path(caminho) / 'ocupacao_semana.png'
    fig.savefig(destino, dpi=150, bbox_inches='tight')
    plt.close(fig)

    return str(destino)
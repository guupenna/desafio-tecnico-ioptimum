# Desafio Técnico — Programação de Manutenção (iOptimum)

Desafio técnico para a vaga de estágio no iOptimum, da IndustriALL.

## Objetivo 
Montar uma programação semanal de manutenção: escolher quais ordens de
serviço executar em cada um dos cinco dias da semana, respeitando as horas disponíveis
de cada habilidade, os dias de parada de planta e a ordem entre OS que dependem umas
das outras. Como o backlog tem muito mais horas de trabalho do que cabe na semana, é necessário escolher bem quais OS serão programadas, pois o objetivo é executar o máximo de OS possíveis, dando preferência para as mais críticas.

A solução encontrada foi uma heurística gulosa, onde as OS são ordenadas por prioridade e cada uma é
programada no primeiro dia em que for possível. Depois, um validador independente
confere se o resultado respeita todas as restrições.

## Como executar

```bash
pip install -r requirements.txt
python src/main.py
```

Isso processa o backlog de 500 OS, imprime o dicionário de saída e gera os gráficos em
`outputs/figs/`.

Para comparar os três backlogs:

```bash
python scripts/resultado.py
```

Para rodar os testes:

```bash
python tests/test_validator.py
```

## Estrutura do projeto

```
desafio-tecnico-ioptimum/
├── data/
│   ├── backlog_desafio_500.xlsx
│   ├── backlog_desafio_1000.xlsx
│   └── backlog_desafio_2000.xlsx
├── src/
│   ├── classes.py
│   ├── loader.py
│   ├── scheduler.py
│   ├── validator.py
│   ├── metrics.py
│   ├── plots.py
│   └── main.py
├── tests/
│   └── test_validator.py
├── scripts/
│   └── resultado.py
├── outputs/
│   └── figs/
│       ├── utilizacao_habilidades.png
│       ├── os_por_prioridade.png
│       └── ocupacao_semana.png
├── docs/
│   ├── RELATORIO.md
│   └── RELATORIO.pdf
├── .gitignore
├── LICENSE
├── requirements.txt
└── README.md
```

O `main.py` roda o backlog de 500, que é o usado nos gráficos e nas tabelas abaixo e `scripts/resultado.py` compara os três.

O `validator.py` não reutiliza nada do `scheduler.py`, já que ele recalcula a ocupação de cada OS por um caminho diferente justamente para que um erro na heurística não passe despercebido nos dois lados. Os testes conferem isso modificando a solução de propósito e verificando se o validador acusa esse erro causado pela modificação.


## Resultados

| Backlog | Programadas | Z | A | B | C | Violações |
|--------:|------------:|--:|--:|--:|--:|----------:|
| 500 | 38 de 500 | 11 | 11 | 8 | 8 | 0 |
| 1000 | 54 de 1000 | 17 | 17 | 10 | 10 | 0 |
| 2000 | 61 de 2000 | 23 | 22 | 13 | 3 | 0 |

Utilização das horas disponíveis:

| Backlog | Mecânico | Elétrico | Lubrificador | Soldador |
|--------:|---------:|---------:|-------------:|---------:|
| 500 | 57% | 58% | 74% | 72% |
| 1000 | 97% | 91% | 93% | 95% |
| 2000 | 98% | 93% | 98% | 96% |

No backlog de 500 por exemplo, são 25.751
horas de trabalho para 512 horas disponíveis na semana. Das 462 OS que ficaram de fora,
298 precisam de mais de 40 horas cada uma, e como cada OS avança no máximo 8 horas por
dia e a semana tem 5 dias, elas não caberiam na semana nessa configuração.
Portanto, programar poucas OS é um resultado esperado.


Mais informações sobre as decisões para a solução do desafio em [docs/RELATORIO.md](docs/RELATORIO.md), tambem disponível em [PDF](docs/RELATORIO.pdf).

# Planejador Autônomo Acadêmico

Projeto em Python para a disciplina de Lógica Aplicada. O sistema simula um planejador autônomo simples: o usuário informa uma tarefa complexa e o programa divide essa tarefa em subtarefas menores, calcula urgência, calcula uma pontuação lógica e recomenda uma ordem de execução.

O projeto não usa API externa de IA, banco de dados online ou bibliotecas complexas. A versão de terminal funciona apenas com Python. A interface visual usa Streamlit.

## Objetivo

Demonstrar, de forma didática, a ideia de delegar uma tarefa complexa para um algoritmo que aplica regras lógicas e organiza uma sequência de ações.

Exemplos de tarefas:

- fazer trabalho acadêmico;
- estudar para prova;
- preparar apresentação;
- desenvolver projeto de programação;
- organizar rotina de estudos;
- tarefa personalizada.

## Estrutura

```text
planejador_autonomo/
|-- main.py
|-- app.py
|-- models.py
|-- planner.py
|-- storage.py
|-- validators.py
|-- sample_data.json
|-- requirements.txt
|-- README.md
`-- tests/
    `-- test_planner.py
```

## Como executar no terminal

Entre na pasta do projeto:

```bash
cd planejador_autonomo
```

Execute:

```bash
python main.py
```

No menu, você pode:

- cadastrar tarefa;
- listar tarefas carregadas;
- gerar plano;
- salvar tarefas em JSON;
- carregar tarefas salvas;
- carregar exemplos do arquivo `sample_data.json`;
- excluir tarefas com confirmação.

## Como executar com Streamlit

Instale a dependência:

```bash
pip install -r requirements.txt
```

Execute:

```bash
streamlit run app.py
```

A página permite preencher tarefa, prazo, prioridade e duração estimada. Depois mostra urgência, pontuação, justificativa e subtarefas ordenadas.

## Como rodar os testes

Dentro da pasta `planejador_autonomo`, execute:

```bash
python -m unittest discover -s tests
```

Os testes verificam cálculo de urgência, pontuação, geração de subtarefas, ordenação, geração de plano completo e exclusão de tarefas.

## Regras lógicas usadas

O sistema usa regras condicionais simples:

- se o prazo já passou, a tarefa recebe urgência `prazo vencido`;
- se faltam poucos dias e a prioridade é alta, a tarefa fica `muito urgente`;
- quanto menor o prazo, maior a pontuação;
- quanto maior a prioridade, maior a pontuação;
- se a tarefa for longa, o sistema sugere dividir a execução em blocos menores;
- se o tipo da tarefa for conhecido, o sistema usa subtarefas predefinidas;
- se o tipo for personalizado, o sistema usa uma sequência genérica de análise, divisão, ordenação, execução e revisão.

## Como o algoritmo funciona

O fluxo principal está em `planner.py`:

1. `calcular_dias_restantes` compara o prazo com a data atual.
2. `classificar_urgencia` transforma prazo e prioridade em uma categoria de urgência.
3. `calcular_pontuacao` soma pesos de prioridade, prazo e duração.
4. `identificar_tipo` reconhece o tipo informado ou procura palavras-chave.
5. `gerar_subtarefas` transforma a tarefa principal em etapas menores.
6. `ordenar_subtarefas` organiza as etapas em planejamento, pesquisa, execução e revisão.
7. `gerar_justificativa` explica por que o plano foi escolhido.

Esse fluxo mostra decomposição do problema em sub-rotinas menores, cada uma com uma responsabilidade clara.

## Exemplo de entrada

```text
Título: Fazer trabalho acadêmico de Lógica Aplicada
Tipo: trabalho academico
Prazo: 15/06/2026
Prioridade: alta
Duração estimada: 8 horas
```

## Exemplo de saída

```text
Tipo identificado: trabalho academico
Urgência: moderada
Pontuação: 50

Ordem recomendada:
1. Dividir a tarefa em blocos menores de tempo.
2. Entender o tema proposto.
3. Definir problema de pesquisa.
4. Organizar estrutura do trabalho.
5. Buscar referências bibliográficas.
...
```

## Relação com Lógica Aplicada

### Introdução

O projeto representa um planejador autônomo simples, inspirado na ideia de que um agente pode receber um objetivo geral e transformá-lo em uma sequência de ações menores.

### Metodologia

A metodologia do programa é baseada em decomposição funcional. Cada arquivo possui uma responsabilidade: modelos de dados, validação, regras de planejamento, armazenamento e interface. Em `planner.py`, cada função representa uma etapa do raciocínio.

### Fundamentação Teórica

O sistema usa proposições condicionais do tipo `se... então...`. Exemplos:

- se a prioridade é alta, então a pontuação aumenta;
- se o prazo está próximo, então a urgência aumenta;
- se a duração estimada é alta, então o sistema recomenda dividir a tarefa em blocos menores;
- se o tipo é conhecido, então subtarefas específicas são usadas.

Essas regras são simples, mas demonstram inferência lógica, tomada de decisão e organização sequencial.

### Resultados e Discussão

O resultado é um plano com subtarefas ordenadas e justificadas. A discussão pode avaliar se as regras foram suficientes, se a ordem gerada faz sentido e quais melhorias futuras poderiam ser feitas, como pesos configuráveis, calendário real ou uma interface mais avançada.

## Partes boas para explicar na apresentação

- `Tarefa`, `Subtarefa` e `Plano` em `models.py`, pois mostram como os dados foram organizados.
- `classificar_urgencia` em `planner.py`, pois demonstra regras condicionais.
- `calcular_pontuacao` em `planner.py`, pois mostra uso de pesos lógicos.
- `gerar_subtarefas` em `planner.py`, pois demonstra decomposição da tarefa complexa.
- `ordenar_subtarefas` em `planner.py`, pois mostra a sequência lógica de execução.
- `storage.py`, pois mostra persistência simples em JSON sem banco de dados.

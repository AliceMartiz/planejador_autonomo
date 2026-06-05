# Planejador Autônomo Acadêmico

Protótipo desenvolvido em Python para a disciplina de **Lógica Aplicada**, com o objetivo de simular um **agente planejador baseado em regras lógicas**.

O sistema recebe uma tarefa complexa, identifica seu tipo, calcula urgência e pontuação, divide a tarefa em subtarefas menores e apresenta uma sequência lógica de execução.

> Este projeto não utiliza IA generativa, API externa, machine learning ou rede neural. A proposta é representar uma abordagem clássica de **IA simbólica**, baseada em regras condicionais, decomposição de problemas e execução sequencial.

---

## Demonstração

Aplicação publicada no Streamlit:

```text
https://planejadorautonomoacademico-logicaaplicada.streamlit.app/
```

Repositório no GitHub:

```text
https://github.com/AliceMartiz/planejador_autonomo
```

---

## Sumário

- [Sobre o projeto](#sobre-o-projeto)
- [Objetivo](#objetivo)
- [Relação com Lógica Aplicada e IA](#relação-com-lógica-aplicada-e-ia)
- [Funcionalidades](#funcionalidades)
- [Interface para apresentação acadêmica](#interface-para-apresentação-acadêmica)
- [Tecnologias utilizadas](#tecnologias-utilizadas)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Como executar](#como-executar)
- [Como usar o sistema](#como-usar-o-sistema)
- [Como o algoritmo funciona](#como-o-algoritmo-funciona)
- [Regras lógicas implementadas](#regras-lógicas-implementadas)
- [Exemplo de entrada e saída](#exemplo-de-entrada-e-saída)
- [Testes](#testes)
- [Relação com o paper](#relação-com-o-paper)
- [Limitações](#limitações)
- [Melhorias futuras](#melhorias-futuras)
- [Considerações éticas](#considerações-éticas)
- [Autores](#autores)

---

## Sobre o projeto

O **Planejador Autônomo Acadêmico** foi criado para demonstrar como um sistema computacional pode receber uma tarefa ampla e transformá-la em um plano de ação organizado.

A ideia central é semelhante a um agente planejador: o usuário informa um objetivo, e o sistema aplica regras para decidir quais etapas devem ser executadas primeiro.

Exemplos de tarefas aceitas:

- fazer trabalho acadêmico;
- estudar para prova;
- preparar apresentação;
- desenvolver projeto de programação;
- organizar rotina de estudos;
- criar uma tarefa personalizada.

O projeto foi pensado para ser simples, didático e adequado ao primeiro semestre de Ciência da Computação.

---

## Objetivo

Desenvolver um protótipo funcional capaz de:

1. receber uma tarefa complexa informada pelo usuário;
2. identificar ou classificar o tipo da tarefa;
3. decompor a tarefa em subtarefas menores;
4. calcular a urgência com base no prazo;
5. calcular uma pontuação lógica com base em prioridade, prazo e duração;
6. organizar as subtarefas em ordem recomendada;
7. justificar a decisão tomada pelo sistema;
8. salvar as tarefas em um arquivo JSON;
9. permitir interação por terminal e por interface visual em Streamlit.

---

## Relação com Lógica Aplicada e IA

O projeto se relaciona com **Lógica Aplicada** porque utiliza estruturas fundamentais de raciocínio computacional, como:

- estruturas condicionais `if`, `elif` e `else`;
- operadores de comparação;
- funções com responsabilidades específicas;
- listas e dicionários;
- ordenação por critérios lógicos;
- validação de entradas;
- decomposição de problemas;
- execução sequencial de sub-rotinas.

O projeto se relaciona com **Inteligência Artificial** por simular um **agente planejador baseado em regras**. Ele recebe dados do ambiente, interpreta a tarefa, aplica regras de decisão e retorna um plano de ação.

Fluxo conceitual do agente:

```text
Entrada do usuário
        ↓
Validação dos dados
        ↓
Identificação do tipo de tarefa
        ↓
Cálculo de prazo, urgência e pontuação
        ↓
Decomposição em subtarefas
        ↓
Ordenação lógica das etapas
        ↓
Exibição do plano e da justificativa
```

---

## Funcionalidades

A aplicação possui as seguintes funcionalidades:

- cadastro de tarefas;
- seleção do tipo da tarefa;
- definição de prazo;
- definição de prioridade;
- definição de duração estimada;
- geração automática de subtarefas;
- cálculo de urgência;
- cálculo de pontuação lógica;
- justificativa da decisão do planejador;
- listagem de tarefas cadastradas;
- ordenação das tarefas por prazo, pontuação, prioridade ou duração;
- exclusão de tarefas;
- marcação de subtarefas como concluídas;
- marcação de tarefa como concluída quando todas as subtarefas forem finalizadas;
- armazenamento local em JSON;
- interface de terminal;
- interface visual com Streamlit;
- testes automatizados com `unittest`.

---

## Interface para apresentação acadêmica

A interface Streamlit foi organizada para uso em apresentações acadêmicas,
com cabeçalho explicativo, barra lateral, formulário compacto, abas para
separar os fluxos e componentes responsivos para telas de notebook e celular.

O tema visual fica em `.streamlit/config.toml` e utiliza cores discretas,
contraste adequado e uma identidade coerente com o contexto acadêmico.

---

## Tecnologias utilizadas

- **Python 3**: linguagem principal do projeto;
- **Streamlit**: criação da interface visual;
- **JSON**: armazenamento local das tarefas;
- **unittest**: testes automatizados;
- **Git e GitHub**: versionamento do código;
- **Streamlit Community Cloud**: publicação da aplicação online.

---

## Estrutura do projeto

```text
planejador_autonomo/
│
├── .streamlit/
│   └── config.toml          # Tema visual usado pelo Streamlit
├── app.py                  # Interface visual com Streamlit
├── main.py                 # Interface de terminal
├── models.py               # Modelos de dados do sistema
├── planner.py              # Regras lógicas e geração do plano
├── storage.py              # Salvamento e carregamento em JSON
├── validators.py           # Validação e normalização de dados
├── sample_data.json        # Exemplos de tarefas
├── tarefas.json            # Tarefas salvas pelo usuário
├── requirements.txt        # Dependências do projeto
├── README.md               # Documentação do projeto
└── tests/
    ├── test_interfaces.py  # Testes das interfaces e interações
    ├── test_planner.py     # Testes da lógica de planejamento
    └── test_storage.py     # Testes do armazenamento em JSON
```

---

## Como executar

### 1. Clonar o repositório

```bash
git clone https://github.com/AliceMartiz/planejador_autonomo.git
cd planejador_autonomo
```

### 2. Criar ambiente virtual

No Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Caso o PowerShell bloqueie a ativação do ambiente virtual, use:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

No Linux ou macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Executar a interface visual

```bash
python -m streamlit run app.py
```

Alternativa no Windows:

```powershell
py -m streamlit run app.py
```

### 5. Executar a versão de terminal

```bash
python main.py
```

No Windows, também é possível usar:

```powershell
py main.py
```

---

## Como usar o sistema

Na interface visual, o usuário deve preencher:

1. **Tarefa principal**: nome geral da tarefa;
2. **Descrição**: explicação curta sobre o que precisa ser feito;
3. **Tipo da tarefa**: categoria escolhida pelo usuário;
4. **Prazo**: data limite para realização;
5. **Prioridade**: baixa, média ou alta;
6. **Duração estimada**: quantidade aproximada de horas necessárias.

Após o preenchimento, o sistema gera um plano contendo:

- tipo identificado;
- urgência;
- pontuação;
- dias restantes;
- justificativa;
- lista de subtarefas em ordem recomendada.

---

## Como o algoritmo funciona

A lógica principal está no arquivo `planner.py`.

O processo é dividido em pequenas funções, cada uma com uma responsabilidade específica:

1. `calcular_dias_restantes`  
   Compara a data atual com o prazo informado pelo usuário.

2. `classificar_urgencia`  
   Usa o prazo e a prioridade para classificar a tarefa como baixa, moderada, urgente, muito urgente ou vencida.

3. `calcular_pontuacao`  
   Soma pesos lógicos de prioridade, prazo e duração estimada.

4. `identificar_tipo`  
   Verifica o tipo informado e também procura palavras-chave no título e na descrição.

5. `gerar_subtarefas`  
   Divide a tarefa principal em subtarefas menores, de acordo com o tipo identificado.

6. `ordenar_subtarefas`  
   Organiza as subtarefas em uma sequência lógica: planejamento, pesquisa, execução e revisão.

7. `gerar_justificativa`  
   Explica por que o sistema gerou aquele plano.

8. `gerar_plano`  
   Reúne todas as etapas anteriores e retorna o plano completo.

Essa separação mostra a ideia de **decomposição de problemas em funções menores**, que é um dos pontos centrais do projeto.

---

## Regras lógicas implementadas

O planejador utiliza regras simples para simular tomada de decisão.

### Regra de urgência

```text
Se o prazo já passou, então a tarefa é classificada como "prazo vencido".
Se faltam 0 ou 1 dia e a prioridade é alta, então a tarefa é "muito urgente".
Se faltam até 2 dias, então a tarefa é "muito urgente".
Se faltam até 5 dias, então a tarefa é "urgente".
Se faltam até 10 dias, então a tarefa é "moderada".
Caso contrário, a urgência é "baixa".
```

### Regra de pontuação

A pontuação é usada para indicar o nível de atenção que a tarefa exige.

| Critério | Condição | Pontos |
|---|---|---:|
| Prioridade | baixa | 10 |
| Prioridade | média | 20 |
| Prioridade | alta | 30 |
| Prazo | vencido | +50 |
| Prazo | 0 ou 1 dia | +40 |
| Prazo | 2 ou 3 dias | +30 |
| Prazo | 4 a 7 dias | +20 |
| Prazo | 8 a 14 dias | +10 |
| Prazo | mais de 14 dias | +5 |
| Duração | 6 horas ou mais | +10 |

Exemplo:

```text
Tarefa de prioridade alta, faltando 2 dias e com duração de 8 horas:
30 pontos da prioridade + 30 pontos do prazo + 10 pontos da duração = 70 pontos
```

### Regra de decomposição

```text
Se o tipo da tarefa for conhecido, então o sistema usa subtarefas específicas.
Se o tipo da tarefa não for reconhecido, então o sistema usa um plano genérico.
```

### Regra para tarefas longas

```text
Se a duração estimada for igual ou maior que 6 horas,
então o sistema adiciona uma subtarefa inicial sugerindo dividir a tarefa em blocos menores.
```

---

## Exemplo de entrada e saída

### Entrada

```text
Tarefa principal: Fazer trabalho acadêmico de Lógica Aplicada
Descrição: Criar paper e protótipo sobre planejador autônomo em IA.
Tipo: trabalho academico
Prazo: 15/06/2026
Prioridade: alta
Duração estimada: 8 horas
```

### Saída esperada

```text
Tipo identificado: trabalho academico
Urgência: moderada
Pontuação: 50
Dias restantes: depende da data atual

Ordem recomendada:
1. Dividir a tarefa em blocos menores de tempo.
2. Entender o tema proposto.
3. Definir problema de pesquisa.
4. Organizar estrutura do trabalho.
5. Buscar referências bibliográficas.
6. Escrever introdução.
7. Escrever fundamentação teórica.
8. Descrever metodologia.
9. Desenvolver ou explicar protótipo.
10. Analisar resultados.
11. Revisar e entregar.
```

### Justificativa gerada

```text
O sistema identificou a tarefa como 'trabalho academico'.
A prioridade e o prazo geraram uma pontuação lógica.
As subtarefas foram ordenadas começando por planejamento,
seguindo para execução e terminando em revisão.
```

---

## Testes

O projeto possui testes automatizados para verificar partes importantes do sistema.

Para executar:

```bash
python -m unittest discover -s tests
```

Os testes cobrem:

- cálculo de dias restantes;
- classificação de urgência;
- cálculo de pontuação;
- geração de subtarefas;
- ordenação lógica das subtarefas;
- geração de plano completo;
- exclusão de tarefas;
- salvamento e carregamento em JSON;
- ordenação de tarefas na interface visual;
- reconhecimento de conclusão de subtarefas.

---

## Relação com o paper

Este projeto pode ser explicado no paper como um **relato de experiência técnica** sobre a construção de um agente planejador simples.

### Introdução

O problema abordado é a dificuldade de transformar tarefas amplas em etapas menores e organizadas. O sistema propõe uma solução automatizada baseada em lógica, capaz de receber uma tarefa complexa e gerar um plano de execução.

### Fundamentação Teórica

O protótipo se apoia em conceitos como:

- agentes inteligentes;
- IA simbólica;
- sistemas baseados em regras;
- decomposição de problemas;
- estruturas condicionais;
- tomada de decisão;
- heurísticas simples;
- execução sequencial.

### Metodologia

A metodologia consistiu no desenvolvimento de um protótipo em Python. O sistema foi dividido em módulos: modelos, validações, regras de planejamento, armazenamento e interfaces. A lógica principal foi implementada em funções menores, permitindo organizar o problema em etapas independentes.

### Resultados e Discussão

O resultado obtido foi um sistema funcional que gera planos de ação automatizados. A avaliação pode ser feita por meio de cenários de teste, observando se o sistema classifica corretamente a urgência, gera subtarefas coerentes e organiza a sequência de execução.

Exemplos de cenários:

| Cenário | Entrada | Resultado esperado |
|---|---|---|
| Tarefa urgente | Prioridade alta e prazo próximo | Classificação como urgente ou muito urgente |
| Tarefa longa | Duração de 6 horas ou mais | Sugestão de dividir em blocos menores |
| Trabalho acadêmico | Tipo "trabalho academico" | Subtarefas de pesquisa, escrita, metodologia e revisão |
| Tarefa personalizada | Tipo "personalizada" | Plano genérico com análise, divisão, execução e revisão |

---

## Fluxograma

O fluxograma será incluído posteriormente.

Sugestão de fluxo para representar:

```text
Início
  ↓
Usuário informa tarefa
  ↓
Sistema valida os dados
  ↓
Sistema identifica o tipo da tarefa
  ↓
Sistema calcula dias restantes
  ↓
Sistema classifica urgência
  ↓
Sistema calcula pontuação
  ↓
Sistema gera subtarefas
  ↓
Sistema ordena subtarefas
  ↓
Sistema exibe plano e justificativa
  ↓
Fim
```

---

## Limitações

O projeto possui algumas limitações importantes:

- não utiliza modelo generativo de linguagem;
- não aprende automaticamente com dados anteriores;
- não possui banco de dados online;
- não integra calendário real;
- não considera disponibilidade diária detalhada do usuário;
- usa regras fixas definidas previamente;
- depende da qualidade das informações inseridas pelo usuário.

Essas limitações não invalidam a proposta, pois o objetivo principal é demonstrar lógica aplicada e planejamento baseado em regras.

---

## Melhorias futuras

Possíveis melhorias para versões futuras:

- adicionar campo de tempo disponível por dia;
- detectar conflitos entre duração estimada e tempo disponível;
- permitir edição de tarefas já cadastradas;
- permitir criação manual de subtarefas personalizadas;
- gerar gráficos de progresso;
- integrar com calendário;
- usar SQLite ou outro banco de dados local;
- permitir múltiplos usuários;
- adicionar uma camada de IA generativa apenas para sugerir subtarefas com linguagem natural;
- exportar o plano em PDF;
- melhorar o design visual da aplicação.

---

## Considerações éticas

O sistema não toma decisões definitivas pelo usuário. Ele apenas sugere uma sequência de execução baseada em regras lógicas simples.

Além disso:

- os dados ficam armazenados localmente no arquivo JSON do projeto;
- nenhuma informação é enviada para APIs externas de IA;
- o usuário continua responsável por avaliar se o plano gerado faz sentido;
- o sistema deve ser visto como apoio à organização, não como substituto do julgamento humano.

---

## Autores

Projeto desenvolvido para a disciplina de **Lógica Aplicada**.

Integrantes:

- Alice Martinez
- Ana Claara Peres
- Caetano
- Guilherme Ojeda
- Renzo

Professor:

- Renato Gil Arruda Vieira

Instituição:

- Universidade Católica Dom Bosco (UCDB)

---

## Status do projeto

Protótipo funcional desenvolvido para fins acadêmicos.

Atualmente, o sistema possui:

- interface visual publicada;
- versão de terminal;
- regras lógicas implementadas;
- armazenamento em JSON;
- testes automatizados;
- documentação inicial.

---

## Licença

Este projeto foi desenvolvido para fins acadêmicos. Caso seja reutilizado, recomenda-se citar o repositório original e os autores do trabalho.

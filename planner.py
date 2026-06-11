"""Lógica principal do Planejador Autônomo Acadêmico.

Este módulo concentra as regras de decisão do projeto. A ideia é mostrar,
de forma didática, como uma tarefa complexa pode ser decomposta em etapas
menores e organizada por uma sequência lógica.
"""

from datetime import date

from models import Plano, Subtarefa, Tarefa
from validators import (
    converter_data,
    formatar_prioridade,
    formatar_tipo_tarefa,
    normalizar_prioridade,
    normalizar_texto,
)


SubtarefaModelo = tuple[str, str, str]


SUBTAREFAS_PRE_DEFINIDAS: dict[str, list[SubtarefaModelo]] = {
    "trabalho academico": [
        (
            "Entender o tema proposto.",
            "planejamento",
            "Antes de pesquisar, é preciso compreender o que foi pedido.",
        ),
        (
            "Definir problema de pesquisa.",
            "planejamento",
            "O problema orienta o restante do trabalho.",
        ),
        (
            "Buscar referências bibliográficas.",
            "pesquisa",
            "As referências sustentam a fundamentação teórica.",
        ),
        (
            "Organizar estrutura do trabalho.",
            "planejamento",
            "Uma estrutura evita escrita desordenada.",
        ),
        (
            "Escrever introdução.",
            "execução",
            "A introdução apresenta tema, objetivo e contexto.",
        ),
        (
            "Escrever fundamentação teórica.",
            "execução",
            "A teoria explica os conceitos usados no trabalho.",
        ),
        (
            "Descrever metodologia.",
            "execução",
            "A metodologia mostra como o trabalho foi desenvolvido.",
        ),
        (
            "Desenvolver ou explicar protótipo.",
            "execução",
            "O protótipo demonstra a aplicação prática da ideia.",
        ),
        (
            "Analisar resultados.",
            "revisão",
            "A análise interpreta o que foi produzido.",
        ),
        (
            "Revisar e entregar.",
            "revisão",
            "A revisão reduz erros antes da entrega final.",
        ),
    ],
    "estudar para prova": [
        (
            "Listar conteúdos cobrados.",
            "planejamento",
            "Primeiro é preciso saber o que será estudado.",
        ),
        (
            "Separar materiais.",
            "planejamento",
            "Materiais organizados reduzem perda de tempo.",
        ),
        ("Ler teoria principal.", "execução", "A teoria cria a base de compreensão."),
        ("Fazer resumo.", "execução", "O resumo ajuda a fixar os pontos essenciais."),
        ("Resolver exercícios.", "execução", "Exercícios testam a aplicação do conteúdo."),
        ("Revisar erros.", "revisão", "Corrigir erros evita repeti-los na prova."),
        (
            "Fazer revisão final.",
            "revisão",
            "A revisão final consolida o estudo antes do prazo.",
        ),
    ],
    "apresentacao": [
        (
            "Definir objetivo da apresentação.",
            "planejamento",
            "O objetivo define o foco da fala.",
        ),
        ("Organizar tópicos principais.", "planejamento", "Os tópicos criam uma ordem clara."),
        ("Criar slides.", "execução", "Os slides dão apoio visual à apresentação."),
        (
            "Preparar roteiro de fala.",
            "execução",
            "O roteiro ajuda a explicar sem improviso excessivo.",
        ),
        ("Ensaiar apresentação.", "revisão", "O ensaio revela problemas de tempo e clareza."),
        ("Revisar tempo e clareza.", "revisão", "A última revisão melhora a comunicação final."),
    ],
    "projeto de programacao": [
        (
            "Entender o problema.",
            "planejamento",
            "Nenhum código deve começar antes de entender o problema.",
        ),
        (
            "Definir funcionalidades.",
            "planejamento",
            "As funcionalidades delimitam o que será implementado.",
        ),
        (
            "Planejar estrutura do projeto.",
            "planejamento",
            "A estrutura separa responsabilidades em arquivos e funções.",
        ),
        (
            "Implementar lógica principal.",
            "execução",
            "A lógica principal resolve o núcleo do problema.",
        ),
        (
            "Testar código.",
            "revisão",
            "Testes verificam se o programa se comporta como esperado.",
        ),
        ("Corrigir erros.", "revisão", "Correções melhoram a qualidade do resultado."),
        (
            "Documentar funcionamento.",
            "revisão",
            "A documentação facilita apresentação e manutenção.",
        ),
    ],
    "rotina de estudos": [
        (
            "Listar disciplinas e compromissos.",
            "planejamento",
            "A rotina precisa começar com uma visão geral das demandas.",
        ),
        (
            "Definir horários disponíveis.",
            "planejamento",
            "O tempo disponível limita o plano possível.",
        ),
        ("Separar blocos de estudo.", "planejamento", "Blocos menores tornam a rotina executável."),
        (
            "Priorizar conteúdos mais urgentes.",
            "execução",
            "Urgência e prioridade indicam o que vem antes.",
        ),
        ("Executar sessões de estudo.", "execução", "A execução transforma o plano em ação."),
        ("Revisar rotina semanal.", "revisão", "A revisão mostra se o planejamento foi realista."),
    ],
    "personalizada": [
        ("Analisar a tarefa.", "planejamento", "Primeiro é necessário entender o objetivo geral."),
        (
            "Dividir em partes menores.",
            "planejamento",
            "A decomposição transforma algo complexo em etapas simples.",
        ),
        (
            "Definir ordem de execução.",
            "planejamento",
            "A ordem reduz dependências e evita retrabalho.",
        ),
        ("Executar etapas principais.", "execução", "A execução realiza o núcleo da tarefa."),
        ("Revisar resultado final.", "revisão", "A revisão verifica se o objetivo foi cumprido."),
    ],
}

# As duas interfaces usam esta mesma lista para evitar opções divergentes.
TIPOS_DISPONIVEIS = tuple(SUBTAREFAS_PRE_DEFINIDAS)


PALAVRAS_CHAVE_TIPO = {
    "trabalho academico": ["trabalho", "paper", "artigo", "pesquisa", "relatorio"],
    "estudar para prova": ["prova", "exame", "avaliacao", "estudar"],
    "apresentacao": ["apresentacao", "seminario", "slides"],
    "projeto de programacao": ["programacao", "programar", "codigo", "software", "projeto"],
    "rotina de estudos": ["rotina", "cronograma", "agenda", "estudos"],
}


PESO_CATEGORIA = {
    "planejamento": 1,
    "pesquisa": 2,
    "execução": 3,
    "revisão": 4,
}


def calcular_dias_restantes(prazo: str, hoje: date | None = None) -> int:
    """Calcula quantos dias faltam até o prazo informado."""

    data_prazo = converter_data(prazo)
    data_atual = hoje or date.today()
    return (data_prazo - data_atual).days


def classificar_urgencia(dias_restantes: int, prioridade: str = "media") -> str:
    """Classifica a urgência com base no prazo e na prioridade."""

    prioridade_normalizada = normalizar_prioridade(prioridade)

    if dias_restantes < 0:
        return "prazo vencido"
    if dias_restantes <= 1 and prioridade_normalizada == "alta":
        return "muito urgente"
    if dias_restantes <= 2:
        return "muito urgente"
    if dias_restantes <= 5:
        return "urgente"
    if dias_restantes <= 10:
        return "moderada"
    return "baixa"


def calcular_pontuacao(
    prioridade: str,
    dias_restantes: int,
    duracao_estimada: float,
) -> int:
    """Calcula uma pontuação lógica para ordenar e explicar a tarefa."""

    prioridade_normalizada = normalizar_prioridade(prioridade)
    pesos_prioridade = {"baixa": 10, "media": 20, "alta": 30}
    pontuacao = pesos_prioridade[prioridade_normalizada]

    # Quanto menor o prazo, maior o peso de urgência.
    if dias_restantes < 0:
        pontuacao += 50
    elif dias_restantes <= 1:
        pontuacao += 40
    elif dias_restantes <= 3:
        pontuacao += 30
    elif dias_restantes <= 7:
        pontuacao += 20
    elif dias_restantes <= 14:
        pontuacao += 10
    else:
        pontuacao += 5

    if duracao_estimada >= 6:
        pontuacao += 10

    return pontuacao


def identificar_tipo(tarefa: Tarefa) -> str:
    """Identifica o tipo da tarefa usando o tipo informado e palavras-chave."""

    tipo_informado = normalizar_texto(tarefa.tipo)
    texto_busca = normalizar_texto(f"{tarefa.titulo} {tarefa.descricao} {tarefa.tipo}")

    # Um tipo específico escolhido pelo usuário tem prioridade. "Personalizada"
    # funciona como fallback e ainda permite a classificação por palavras-chave.
    if (
        tipo_informado in SUBTAREFAS_PRE_DEFINIDAS
        and tipo_informado != "personalizada"
    ):
        return tipo_informado

    for tipo, palavras in PALAVRAS_CHAVE_TIPO.items():
        if any(palavra in texto_busca for palavra in palavras):
            return tipo

    return "personalizada"


def gerar_subtarefas(tarefa: Tarefa) -> list[Subtarefa]:
    """Gera subtarefas menores a partir do tipo identificado."""

    tipo_identificado = identificar_tipo(tarefa)
    modelos = SUBTAREFAS_PRE_DEFINIDAS[tipo_identificado]
    subtarefas = []

    for indice, (nome, categoria, motivo) in enumerate(modelos, start=1):
        subtarefas.append(
            Subtarefa(
                nome=nome,
                categoria=categoria,
                ordem_logica=indice,
                motivo=motivo,
            )
        )

    if tarefa.duracao_estimada >= 6:
        subtarefas.insert(
            0,
            Subtarefa(
                nome="Dividir a tarefa em blocos menores de tempo.",
                categoria="planejamento",
                ordem_logica=0,
                motivo=(
                    "Como a duração estimada é alta, blocos menores "
                    "tornam a execução mais controlável."
                ),
            ),
        )

    return subtarefas


def ordenar_subtarefas(subtarefas: list[Subtarefa]) -> list[Subtarefa]:
    """Ordena por planejamento, pesquisa, execução e revisão."""

    subtarefas_ordenadas = sorted(
        subtarefas,
        key=lambda subtarefa: (
            PESO_CATEGORIA.get(subtarefa.categoria, 99),
            subtarefa.ordem_logica,
        ),
    )

    for nova_ordem, subtarefa in enumerate(subtarefas_ordenadas, start=1):
        subtarefa.ordem_logica = nova_ordem

    return subtarefas_ordenadas


def gerar_justificativa(
    tarefa: Tarefa,
    tipo_identificado: str,
    dias_restantes: int,
    urgencia: str,
    pontuacao: int,
) -> str:
    """Gera uma explicação simples para a decisão do planejador."""

    partes = [
        (
            "O sistema identificou a tarefa como "
            f"'{formatar_tipo_tarefa(tipo_identificado)}'."
        ),
        (
            f"Faltam {dias_restantes} dia(s) para o prazo, por isso a "
            f"urgência foi classificada como '{urgencia.capitalize()}'."
        ),
        (
            f"A prioridade '{formatar_prioridade(tarefa.prioridade)}' "
            f"e o prazo geraram pontuação {pontuacao}."
        ),
        (
            "As subtarefas foram ordenadas começando por planejamento, "
            "seguindo para execução e terminando em revisão."
        ),
    ]

    return " ".join(partes)


def gerar_plano(tarefa: Tarefa, hoje: date | None = None) -> Plano:
    """Gera um plano completo para a tarefa informada."""

    dias_restantes = calcular_dias_restantes(tarefa.prazo, hoje)
    urgencia = classificar_urgencia(dias_restantes, tarefa.prioridade)
    pontuacao = calcular_pontuacao(
        tarefa.prioridade,
        dias_restantes,
        tarefa.duracao_estimada,
    )
    tipo_identificado = identificar_tipo(tarefa)
    subtarefas = ordenar_subtarefas(gerar_subtarefas(tarefa))
    justificativa = gerar_justificativa(
        tarefa,
        tipo_identificado,
        dias_restantes,
        urgencia,
        pontuacao,
    )

    return Plano(
        tarefa=tarefa,
        tipo_identificado=tipo_identificado,
        dias_restantes=dias_restantes,
        urgencia=urgencia,
        pontuacao=pontuacao,
        subtarefas=subtarefas,
        justificativa=justificativa,
    )

"""Regras puras usadas pela listagem de tarefas da interface."""

from datetime import date

from models import Tarefa
from planner import gerar_plano
from validators import converter_data


def ordenar_tarefas(
    tarefas: list[Tarefa],
    criterio: str,
) -> list[tuple[int, Tarefa]]:
    """Ordena tarefas sem perder os índices da lista original."""

    tarefas_com_indice = list(enumerate(tarefas))

    if criterio == "Prazo mais próximo":
        return sorted(
            tarefas_com_indice,
            key=lambda item: converter_data(item[1].prazo),
        )

    if criterio == "Maior pontuação":
        return sorted(
            tarefas_com_indice,
            key=lambda item: (
                -gerar_plano(item[1]).pontuacao,
                converter_data(item[1].prazo),
            ),
        )

    if criterio == "Prioridade mais alta":
        pesos = {"baixa": 1, "media": 2, "alta": 3}
        return sorted(
            tarefas_com_indice,
            key=lambda item: (
                -pesos[item[1].prioridade],
                converter_data(item[1].prazo),
            ),
        )

    if criterio == "Maior duração":
        return sorted(
            tarefas_com_indice,
            key=lambda item: (
                -item[1].duracao_estimada,
                converter_data(item[1].prazo),
            ),
        )

    return tarefas_com_indice


def filtrar_tarefas(
    tarefas_com_indice: list[tuple[int, Tarefa]],
    criterio_filtro: str,
    hoje: date | None = None,
) -> list[tuple[int, Tarefa]]:
    """Filtra tarefas sem perder os índices usados pela interface."""

    if criterio_filtro == "Tarefas terminadas":
        return [
            (indice, tarefa)
            for indice, tarefa in tarefas_com_indice
            if tarefa.concluida
        ]

    if criterio_filtro == "Tarefas atrasadas":
        data_atual = hoje or date.today()
        return [
            (indice, tarefa)
            for indice, tarefa in tarefas_com_indice
            if (
                not tarefa.concluida
                and converter_data(tarefa.prazo) < data_atual
            )
        ]

    return list(tarefas_com_indice)


def remover_tarefas_terminadas(
    tarefas: list[Tarefa],
) -> list[Tarefa]:
    """Retorna uma nova lista contendo apenas tarefas em andamento."""

    return [
        tarefa
        for tarefa in tarefas
        if not tarefa.concluida
    ]


def todas_subtarefas_concluidas(tarefa: Tarefa) -> bool:
    """Verifica a conclusão usando as subtarefas atuais da tarefa."""

    if tarefa.subtarefas_personalizadas is None:
        nomes_subtarefas = {
            subtarefa.nome
            for subtarefa in gerar_plano(tarefa).subtarefas
        }
    else:
        nomes_subtarefas = {
            str(subtarefa.get("nome", "")).strip()
            for subtarefa in tarefa.subtarefas_personalizadas
            if isinstance(subtarefa, dict)
            and str(subtarefa.get("nome", "")).strip()
        }

    return bool(nomes_subtarefas) and nomes_subtarefas.issubset(
        set(tarefa.subtarefas_concluidas)
    )

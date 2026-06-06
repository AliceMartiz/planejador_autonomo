"""Operações puras usadas na edição manual das subtarefas."""

from copy import deepcopy
from uuid import uuid4

from models import Subtarefa


SubtarefaEditavel = dict[str, object]


def criar_subtarefa_editavel(
    nome: str,
    categoria: str,
    motivo: str,
    ordem: int = 1,
    identificador: str | None = None,
) -> SubtarefaEditavel:
    """Cria uma subtarefa editável com identificador estável."""

    return {
        "id": identificador or uuid4().hex,
        "nome": nome.strip(),
        "categoria": categoria.strip(),
        "motivo": motivo.strip(),
        "ordem_logica": ordem,
    }


def converter_subtarefas(
    subtarefas: list[Subtarefa],
) -> list[SubtarefaEditavel]:
    """Converte as subtarefas do planejador para o formato editável."""

    convertidas = [
        criar_subtarefa_editavel(
            nome=subtarefa.nome,
            categoria=subtarefa.categoria,
            motivo=subtarefa.motivo,
            ordem=subtarefa.ordem_logica,
        )
        for subtarefa in subtarefas
    ]
    return renumerar_subtarefas(convertidas)


def normalizar_subtarefas(
    subtarefas: list[SubtarefaEditavel],
) -> list[SubtarefaEditavel]:
    """Completa campos ausentes de listas salvas em JSON."""

    normalizadas = []
    identificadores_usados = set()

    for indice, subtarefa in enumerate(subtarefas, start=1):
        if not isinstance(subtarefa, dict):
            continue

        nome = str(subtarefa.get("nome", "")).strip()
        if not nome:
            continue

        identificador = str(subtarefa.get("id") or uuid4().hex)
        if identificador in identificadores_usados:
            identificador = uuid4().hex
        identificadores_usados.add(identificador)

        normalizadas.append(
            criar_subtarefa_editavel(
                nome=nome,
                categoria=str(
                    subtarefa.get("categoria") or "personalizada"
                ),
                motivo=str(subtarefa.get("motivo") or ""),
                ordem=indice,
                identificador=identificador,
            )
        )

    return renumerar_subtarefas(normalizadas)


def renumerar_subtarefas(
    subtarefas: list[SubtarefaEditavel],
) -> list[SubtarefaEditavel]:
    """Retorna uma cópia da lista com a ordem sequencial atualizada."""

    renumeradas = deepcopy(subtarefas)

    for indice, subtarefa in enumerate(renumeradas, start=1):
        subtarefa["ordem_logica"] = indice

    return renumeradas


def inserir_subtarefa_abaixo(
    subtarefas: list[SubtarefaEditavel],
    identificador_referencia: str,
    nova_subtarefa: SubtarefaEditavel,
) -> list[SubtarefaEditavel]:
    """Insere uma subtarefa logo após a subtarefa de referência."""

    atualizadas = deepcopy(subtarefas)
    indice_referencia = next(
        (
            indice
            for indice, subtarefa in enumerate(atualizadas)
            if subtarefa["id"] == identificador_referencia
        ),
        len(atualizadas) - 1,
    )
    atualizadas.insert(indice_referencia + 1, deepcopy(nova_subtarefa))
    return renumerar_subtarefas(atualizadas)


def editar_subtarefa(
    subtarefas: list[SubtarefaEditavel],
    identificador: str,
    nome: str,
    categoria: str,
    motivo: str,
) -> list[SubtarefaEditavel]:
    """Edita os campos de uma subtarefa sem alterar sua posição."""

    atualizadas = deepcopy(subtarefas)
    indice_atual = next(
        (
            indice
            for indice, subtarefa in enumerate(atualizadas)
            if subtarefa["id"] == identificador
        ),
        None,
    )

    if indice_atual is None:
        return renumerar_subtarefas(atualizadas)

    atualizadas[indice_atual].update(
        {
            "nome": nome.strip(),
            "categoria": categoria.strip(),
            "motivo": motivo.strip(),
        }
    )

    return renumerar_subtarefas(atualizadas)


def reordenar_subtarefas(
    subtarefas: list[SubtarefaEditavel],
    identificadores: list[str],
) -> list[SubtarefaEditavel]:
    """Reordena pelos identificadores e atualiza os índices sequenciais."""

    por_identificador = {
        str(subtarefa["id"]): deepcopy(subtarefa)
        for subtarefa in subtarefas
    }
    ordem_solicitada = [
        str(identificador)
        for identificador in identificadores
    ]
    ordem_valida = (
        len(ordem_solicitada) == len(por_identificador)
        and len(set(ordem_solicitada)) == len(ordem_solicitada)
        and set(ordem_solicitada) == set(por_identificador)
    )
    if not ordem_valida:
        return renumerar_subtarefas(subtarefas)

    reordenadas = [
        por_identificador[identificador]
        for identificador in ordem_solicitada
    ]
    return renumerar_subtarefas(reordenadas)


def remover_subtarefa(
    subtarefas: list[SubtarefaEditavel],
    identificador: str,
) -> list[SubtarefaEditavel]:
    """Remove uma subtarefa pelo identificador e renumera a lista."""

    restantes = [
        deepcopy(subtarefa)
        for subtarefa in subtarefas
        if subtarefa["id"] != identificador
    ]
    return renumerar_subtarefas(restantes)

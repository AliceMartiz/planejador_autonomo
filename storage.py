"""Funções para salvar e carregar tarefas em arquivos JSON."""

import json
from dataclasses import asdict, fields
from pathlib import Path
from tempfile import NamedTemporaryFile

from models import Tarefa
from validators import (
    normalizar_prioridade,
    validar_data,
    validar_numero_positivo,
    validar_prioridade,
)


ARQUIVO_PADRAO = Path(__file__).with_name("tarefas.json")


def _campos_tarefa():
    """Retorna os nomes dos campos aceitos pela dataclass Tarefa."""

    return {campo.name for campo in fields(Tarefa)}


def _normalizar_tarefa_carregada(tarefa: Tarefa) -> Tarefa | None:
    """Valida dados externos antes que eles cheguem às interfaces."""

    if (
        not isinstance(tarefa.titulo, str)
        or not tarefa.titulo.strip()
        or not isinstance(tarefa.tipo, str)
        or not isinstance(tarefa.prazo, str)
        or not isinstance(tarefa.prioridade, str)
        or not validar_data(tarefa.prazo)
        or not validar_prioridade(tarefa.prioridade)
        or not validar_numero_positivo(tarefa.duracao_estimada)
    ):
        return None

    tarefa.titulo = tarefa.titulo.strip()
    tarefa.tipo = tarefa.tipo.strip()
    tarefa.descricao = str(tarefa.descricao or "").strip()
    tarefa.prioridade = normalizar_prioridade(tarefa.prioridade)
    tarefa.duracao_estimada = float(tarefa.duracao_estimada)

    if not isinstance(tarefa.subtarefas_concluidas, list):
        tarefa.subtarefas_concluidas = []
    else:
        tarefa.subtarefas_concluidas = [
            nome.strip()
            for item in tarefa.subtarefas_concluidas
            if (nome := str(item).strip())
        ]
    if not isinstance(tarefa.concluida, bool):
        tarefa.concluida = False
    if (
        tarefa.subtarefas_personalizadas is not None
        and not isinstance(tarefa.subtarefas_personalizadas, list)
    ):
        tarefa.subtarefas_personalizadas = None

    return tarefa


def salvar_tarefas(tarefas: list[Tarefa], caminho=ARQUIVO_PADRAO) -> None:
    """Salva as tarefas sem deixar um JSON parcial em caso de falha."""

    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)

    campos_validos = _campos_tarefa()
    dados = [
        {
            campo: valor
            for campo, valor in asdict(tarefa).items()
            if campo in campos_validos
        }
        for tarefa in tarefas
    ]

    caminho_temporario = None
    try:
        # O arquivo definitivo só é trocado após a gravação ser concluída.
        with NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=caminho.parent,
            prefix=f".{caminho.name}.",
            suffix=".tmp",
            delete=False,
        ) as arquivo:
            caminho_temporario = Path(arquivo.name)
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)

        caminho_temporario.replace(caminho)
    finally:
        if caminho_temporario and caminho_temporario.exists():
            caminho_temporario.unlink()


def carregar_tarefas(caminho=ARQUIVO_PADRAO) -> list[Tarefa]:
    """Carrega tarefas de um arquivo JSON, retornando lista vazia se ele não existir."""

    caminho = Path(caminho)

    if not caminho.exists():
        return []

    try:
        with caminho.open("r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except (json.JSONDecodeError, OSError, UnicodeDecodeError):
        return []

    if isinstance(dados, dict):
        dados = dados.get("tarefas", [])

    if not isinstance(dados, list):
        return []

    tarefas = []
    campos_validos = _campos_tarefa()

    for item in dados:
        if not isinstance(item, dict):
            continue

        dados_tarefa = {
            campo: item[campo]
            for campo in campos_validos
            if campo in item
        }

        try:
            tarefa = _normalizar_tarefa_carregada(Tarefa(**dados_tarefa))
        except (TypeError, ValueError):
            continue
        if tarefa is not None:
            tarefas.append(tarefa)

    return tarefas

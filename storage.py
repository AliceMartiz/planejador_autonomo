"""Funções para salvar e carregar tarefas em arquivos JSON."""

import json
from dataclasses import asdict, fields
from pathlib import Path
from typing import List

from models import Tarefa


ARQUIVO_PADRAO = Path(__file__).with_name("tarefas.json")


def _campos_tarefa():
    """Retorna os nomes dos campos aceitos pela dataclass Tarefa."""

    return {campo.name for campo in fields(Tarefa)}


def salvar_tarefas(tarefas: List[Tarefa], caminho=ARQUIVO_PADRAO) -> None:
    """Salva uma lista de tarefas em arquivo JSON."""

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

    with caminho.open("w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)


def carregar_tarefas(caminho=ARQUIVO_PADRAO) -> List[Tarefa]:
    """Carrega tarefas de um arquivo JSON, retornando lista vazia se ele não existir."""

    caminho = Path(caminho)

    if not caminho.exists():
        return []

    try:
        with caminho.open("r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except (json.JSONDecodeError, OSError):
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
            tarefas.append(Tarefa(**dados_tarefa))
        except TypeError:
            continue

    return tarefas

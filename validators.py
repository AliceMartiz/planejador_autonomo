"""Funções de validação para entradas do usuário."""

from datetime import date, datetime
import unicodedata


PRIORIDADES_VALIDAS = {"baixa", "media", "alta"}


def remover_acentos(texto: str) -> str:
    """Remove acentos para facilitar comparações de texto."""

    texto_normalizado = unicodedata.normalize("NFD", texto)
    return "".join(
        caractere
        for caractere in texto_normalizado
        if unicodedata.category(caractere) != "Mn"
    )


def normalizar_texto(texto: str) -> str:
    """Padroniza texto para comparações simples."""

    return remover_acentos(texto.strip().lower())


def converter_data(data_texto: str) -> date:
    """Converte uma data no formato dd/mm/aaaa para um objeto date."""

    return datetime.strptime(data_texto, "%d/%m/%Y").date()


def validar_data(data_texto: str) -> bool:
    """Verifica se a data está no formato dd/mm/aaaa."""

    try:
        converter_data(data_texto)
        return True
    except (TypeError, ValueError):
        return False


def validar_prioridade(prioridade: str) -> bool:
    """Verifica se a prioridade é baixa, media ou alta."""

    return normalizar_texto(prioridade) in PRIORIDADES_VALIDAS


def normalizar_prioridade(prioridade: str) -> str:
    """Retorna a prioridade em um formato usado pelas regras lógicas."""

    prioridade_normalizada = normalizar_texto(prioridade)
    if prioridade_normalizada not in PRIORIDADES_VALIDAS:
        raise ValueError("Prioridade inválida. Use baixa, media ou alta.")
    return prioridade_normalizada


def validar_numero_positivo(valor) -> bool:
    """Verifica se o valor informado pode ser convertido para número positivo."""

    try:
        return float(valor) > 0
    except (TypeError, ValueError):
        return False


def converter_numero_positivo(valor, nome_campo: str) -> float:
    """Converte um valor para número positivo ou gera uma mensagem amigável."""

    try:
        numero = float(valor)
    except (TypeError, ValueError) as erro:
        raise ValueError(f"{nome_campo} deve ser um número.") from erro

    if numero <= 0:
        raise ValueError(f"{nome_campo} deve ser maior que zero.")

    return numero

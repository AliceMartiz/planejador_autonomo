"""Modelos de dados usados pelo Planejador Autônomo Acadêmico."""

from dataclasses import dataclass, field


@dataclass
class Tarefa:
    """Representa a tarefa principal informada pelo usuário."""

    titulo: str
    tipo: str
    prazo: str
    prioridade: str
    duracao_estimada: float
    descricao: str = ""
    subtarefas_concluidas: list[str] = field(default_factory=list)
    concluida: bool = False
    subtarefas_personalizadas: list[dict[str, object]] | None = None


@dataclass
class Subtarefa:
    """Representa uma etapa menor gerada a partir da tarefa principal."""

    nome: str
    categoria: str
    ordem_logica: int
    motivo: str


@dataclass
class Plano:
    """Guarda o resultado completo do planejamento."""

    tarefa: Tarefa
    tipo_identificado: str
    dias_restantes: int
    urgencia: str
    pontuacao: int
    subtarefas: list[Subtarefa] = field(default_factory=list)
    justificativa: str = ""

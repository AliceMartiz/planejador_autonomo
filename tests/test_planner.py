"""Testes simples para a lógica do planejador."""

from datetime import date
from pathlib import Path
import sys
import unittest


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from models import Subtarefa, Tarefa
from planner import (
    calcular_dias_restantes,
    calcular_pontuacao,
    classificar_urgencia,
    gerar_plano,
    gerar_subtarefas,
    ordenar_subtarefas,
)


class TestPlanner(unittest.TestCase):
    """Testa as principais regras lógicas do planejador."""

    def test_calculo_de_urgencia(self):
        urgencia = classificar_urgencia(dias_restantes=1, prioridade="alta")
        self.assertEqual(urgencia, "muito urgente")

    def test_calculo_de_dias_restantes(self):
        dias = calcular_dias_restantes("10/06/2026", hoje=date(2026, 6, 3))
        self.assertEqual(dias, 7)

    def test_calculo_de_pontuacao(self):
        pontuacao_alta = calcular_pontuacao("alta", dias_restantes=1, duracao_estimada=8)
        pontuacao_baixa = calcular_pontuacao("baixa", dias_restantes=20, duracao_estimada=2)
        self.assertGreater(pontuacao_alta, pontuacao_baixa)

    def test_geracao_de_subtarefas(self):
        tarefa = Tarefa(
            titulo="Fazer trabalho acadêmico",
            tipo="trabalho academico",
            prazo="15/06/2026",
            prioridade="alta",
            duracao_estimada=5,
        )

        subtarefas = gerar_subtarefas(tarefa)

        self.assertGreater(len(subtarefas), 0)
        self.assertEqual(subtarefas[0].nome, "Entender o tema proposto.")

    def test_ordenacao_das_subtarefas(self):
        subtarefas = [
            Subtarefa("Revisar resultado.", "revisão", 1, "Revisão vem depois."),
            Subtarefa("Planejar execução.", "planejamento", 2, "Planejamento vem antes."),
            Subtarefa("Executar tarefa.", "execução", 3, "Execução vem no meio."),
        ]

        ordenadas = ordenar_subtarefas(subtarefas)

        self.assertEqual(ordenadas[0].categoria, "planejamento")
        self.assertEqual(ordenadas[-1].categoria, "revisão")

    def test_geracao_de_plano_completo(self):
        tarefa = Tarefa(
            titulo="Preparar apresentação",
            tipo="apresentacao",
            prazo="05/06/2026",
            prioridade="alta",
            duracao_estimada=4,
        )

        plano = gerar_plano(tarefa, hoje=date(2026, 6, 3))

        self.assertEqual(plano.urgencia, "muito urgente")
        self.assertGreater(len(plano.subtarefas), 0)


if __name__ == "__main__":
    unittest.main()

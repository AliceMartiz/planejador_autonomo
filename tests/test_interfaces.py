"""Testes das interações compartilhadas pelas interfaces."""

from pathlib import Path
from unittest.mock import patch
import sys
import unittest


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import ordenar_tarefas, todas_subtarefas_concluidas
from main import excluir_tarefa
from models import Tarefa
from planner import gerar_plano


def criar_tarefa() -> Tarefa:
    """Cria uma tarefa simples para os testes de exclusão."""

    return Tarefa(
        titulo="Trabalho de teste",
        tipo="trabalho academico",
        prazo="22/07/2026",
        prioridade="alta",
        duracao_estimada=5,
    )


class TestExclusaoTerminal(unittest.TestCase):
    """Testa a confirmação de exclusão na interface de terminal."""

    @patch("main.salvar_tarefas")
    @patch("builtins.input", side_effect=["1", "n"])
    def test_cancelar_exclusao_mantem_tarefa(self, _, salvar_mock):
        tarefas = [criar_tarefa()]

        resultado = excluir_tarefa(tarefas)

        self.assertFalse(resultado)
        self.assertEqual(len(tarefas), 1)
        salvar_mock.assert_not_called()

    @patch("main.salvar_tarefas")
    @patch("builtins.input", side_effect=["1", "s"])
    def test_confirmar_exclusao_remove_e_salva(self, _, salvar_mock):
        tarefas = [criar_tarefa()]

        resultado = excluir_tarefa(tarefas)

        self.assertTrue(resultado)
        self.assertEqual(tarefas, [])
        salvar_mock.assert_called_once_with([])


class TestOrdenacaoTarefas(unittest.TestCase):
    """Testa as opções do filtro da interface visual."""

    def setUp(self):
        self.tarefas = [
            Tarefa(
                titulo="Longa",
                tipo="personalizada",
                prazo="20/06/2026",
                prioridade="baixa",
                duracao_estimada=8,
            ),
            Tarefa(
                titulo="Urgente",
                tipo="personalizada",
                prazo="06/06/2026",
                prioridade="alta",
                duracao_estimada=2,
            ),
        ]

    def test_ordena_por_prazo(self):
        ordenadas = ordenar_tarefas(self.tarefas, "Prazo mais próximo")

        self.assertEqual(ordenadas[0][1].titulo, "Urgente")

    def test_ordena_por_prioridade(self):
        ordenadas = ordenar_tarefas(self.tarefas, "Prioridade mais alta")

        self.assertEqual(ordenadas[0][1].titulo, "Urgente")

    def test_ordena_por_duracao(self):
        ordenadas = ordenar_tarefas(self.tarefas, "Maior duração")

        self.assertEqual(ordenadas[0][1].titulo, "Longa")


class TestConclusaoTarefa(unittest.TestCase):
    """Testa a conclusão baseada em todas as subtarefas."""

    def test_reconhece_todas_as_subtarefas_concluidas(self):
        tarefa = criar_tarefa()
        tarefa.subtarefas_concluidas = [
            subtarefa.nome
            for subtarefa in gerar_plano(tarefa).subtarefas
        ]

        self.assertTrue(todas_subtarefas_concluidas(tarefa))

    def test_nao_conclui_com_subtarefa_pendente(self):
        tarefa = criar_tarefa()

        self.assertFalse(todas_subtarefas_concluidas(tarefa))


if __name__ == "__main__":
    unittest.main()

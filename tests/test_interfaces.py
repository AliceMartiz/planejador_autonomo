"""Testes das interações compartilhadas pelas interfaces."""

from datetime import date
from pathlib import Path
from unittest.mock import patch
import sys
import unittest


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ui_tarefas import (
    atualizar_dados_planejamento,
    filtrar_tarefas,
    ordenar_tarefas,
    remover_tarefas_terminadas,
    todas_subtarefas_concluidas,
)
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


class TestFiltroTarefas(unittest.TestCase):
    """Testa os filtros por conclusão e atraso."""

    def setUp(self):
        self.tarefas = [
            Tarefa(
                titulo="Terminada",
                tipo="personalizada",
                prazo="01/06/2026",
                prioridade="media",
                duracao_estimada=2,
                concluida=True,
            ),
            Tarefa(
                titulo="Atrasada",
                tipo="personalizada",
                prazo="05/06/2026",
                prioridade="alta",
                duracao_estimada=3,
            ),
            Tarefa(
                titulo="No prazo",
                tipo="personalizada",
                prazo="20/06/2026",
                prioridade="baixa",
                duracao_estimada=1,
            ),
        ]
        self.tarefas_com_indice = ordenar_tarefas(
            self.tarefas,
            "Padrão",
        )

    def test_filtra_tarefas_terminadas(self):
        resultado = filtrar_tarefas(
            self.tarefas_com_indice,
            "Tarefas terminadas",
            hoje=date(2026, 6, 10),
        )

        self.assertEqual(
            [(indice, tarefa.titulo) for indice, tarefa in resultado],
            [(0, "Terminada")],
        )

    def test_filtra_tarefas_atrasadas_nao_concluidas(self):
        resultado = filtrar_tarefas(
            self.tarefas_com_indice,
            "Tarefas atrasadas",
            hoje=date(2026, 6, 10),
        )

        self.assertEqual(
            [(indice, tarefa.titulo) for indice, tarefa in resultado],
            [(1, "Atrasada")],
        )

    def test_remove_somente_tarefas_terminadas(self):
        resultado = remover_tarefas_terminadas(self.tarefas)

        self.assertEqual(
            [tarefa.titulo for tarefa in resultado],
            ["Atrasada", "No prazo"],
        )
        self.assertEqual(len(self.tarefas), 3)


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


class TestEdicaoTarefa(unittest.TestCase):
    """Testa a atualização dos critérios usados pelo planejamento."""

    def test_atualiza_prioridade_prazo_e_duracao(self):
        tarefa = criar_tarefa()

        atualizar_dados_planejamento(
            tarefa,
            "media",
            "30/07/2026",
            7.5,
        )

        self.assertEqual(tarefa.prioridade, "media")
        self.assertEqual(tarefa.prazo, "30/07/2026")
        self.assertEqual(tarefa.duracao_estimada, 7.5)

    def test_nova_etapa_automatica_reabre_tarefa_concluida(self):
        tarefa = criar_tarefa()
        tarefa.subtarefas_concluidas = [
            subtarefa.nome
            for subtarefa in gerar_plano(tarefa).subtarefas
        ]
        tarefa.concluida = True

        atualizar_dados_planejamento(
            tarefa,
            tarefa.prioridade,
            tarefa.prazo,
            7,
        )

        self.assertFalse(tarefa.concluida)
        self.assertNotIn(
            "Dividir a tarefa em blocos menores de tempo.",
            tarefa.subtarefas_concluidas,
        )


if __name__ == "__main__":
    unittest.main()

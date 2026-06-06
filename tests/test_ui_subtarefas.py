"""Testes das operações puras de edição das subtarefas."""

import unittest

from ui_subtarefas import (
    criar_subtarefa_editavel,
    editar_subtarefa,
    inserir_subtarefa_abaixo,
    reordenar_subtarefas,
    remover_subtarefa,
)


def criar_lista():
    """Cria uma lista curta e previsível para os testes."""

    return [
        criar_subtarefa_editavel("A", "planejamento", "Motivo A", 1, "a"),
        criar_subtarefa_editavel("B", "execução", "Motivo B", 2, "b"),
        criar_subtarefa_editavel("C", "revisão", "Motivo C", 3, "c"),
    ]


class TestEdicaoSubtarefas(unittest.TestCase):
    """Testa inserção, edição, remoção e renumeração."""

    def test_insere_subtarefa_abaixo_da_posicao_escolhida(self):
        nova = criar_subtarefa_editavel(
            "Nova",
            "pesquisa",
            "Motivo novo",
            identificador="nova",
        )

        resultado = inserir_subtarefa_abaixo(criar_lista(), "a", nova)

        self.assertEqual(
            [subtarefa["nome"] for subtarefa in resultado],
            ["A", "Nova", "B", "C"],
        )
        self.assertEqual(
            [subtarefa["ordem_logica"] for subtarefa in resultado],
            [1, 2, 3, 4],
        )

    def test_edita_sem_mudar_a_posicao(self):
        resultado = editar_subtarefa(
            criar_lista(),
            "b",
            "B editada",
            "pesquisa",
            "Novo motivo",
        )

        self.assertEqual(
            [subtarefa["id"] for subtarefa in resultado],
            ["a", "b", "c"],
        )
        self.assertEqual(resultado[1]["nome"], "B editada")
        self.assertEqual(resultado[1]["categoria"], "pesquisa")
        self.assertEqual(resultado[1]["motivo"], "Novo motivo")

    def test_reordena_e_atualiza_os_indices(self):
        resultado = reordenar_subtarefas(
            criar_lista(),
            ["c", "a", "b"],
        )

        self.assertEqual(
            [subtarefa["id"] for subtarefa in resultado],
            ["c", "a", "b"],
        )
        self.assertEqual(
            [subtarefa["ordem_logica"] for subtarefa in resultado],
            [1, 2, 3],
        )

    def test_reordena_a_mesma_subtarefa_varias_vezes(self):
        primeira_ordem = reordenar_subtarefas(
            criar_lista(),
            ["b", "c", "a"],
        )
        segunda_ordem = reordenar_subtarefas(
            primeira_ordem,
            ["a", "b", "c"],
        )
        terceira_ordem = reordenar_subtarefas(
            segunda_ordem,
            ["b", "a", "c"],
        )

        self.assertEqual(
            [subtarefa["id"] for subtarefa in terceira_ordem],
            ["b", "a", "c"],
        )
        self.assertEqual(
            [subtarefa["ordem_logica"] for subtarefa in terceira_ordem],
            [1, 2, 3],
        )

    def test_ignora_ordem_antiga_depois_de_excluir_subtarefa(self):
        restantes = remover_subtarefa(criar_lista(), "b")

        resultado = reordenar_subtarefas(
            restantes,
            ["c", "a", "b"],
        )

        self.assertEqual(
            [subtarefa["id"] for subtarefa in resultado],
            ["a", "c"],
        )
        self.assertEqual(
            [subtarefa["ordem_logica"] for subtarefa in resultado],
            [1, 2],
        )

    def test_ignora_ordem_com_identificador_duplicado(self):
        resultado = reordenar_subtarefas(
            criar_lista(),
            ["a", "a", "c"],
        )

        self.assertEqual(
            [subtarefa["id"] for subtarefa in resultado],
            ["a", "b", "c"],
        )

    def test_remove_e_renumera_subtarefa(self):
        resultado = remover_subtarefa(criar_lista(), "b")

        self.assertEqual(
            [subtarefa["nome"] for subtarefa in resultado],
            ["A", "C"],
        )
        self.assertEqual(
            [subtarefa["ordem_logica"] for subtarefa in resultado],
            [1, 2],
        )


if __name__ == "__main__":
    unittest.main()

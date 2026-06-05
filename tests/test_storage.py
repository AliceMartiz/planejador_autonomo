"""Testes de compatibilidade do armazenamento em JSON."""

import json
from pathlib import Path
import sys
import tempfile
import unittest


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from models import Tarefa
from storage import carregar_tarefas, salvar_tarefas


class TestStorage(unittest.TestCase):
    """Testa o carregamento de arquivos criados por versões anteriores."""

    def test_ignora_tempo_disponivel_de_json_antigo(self):
        dados = [
            {
                "titulo": "Tarefa antiga",
                "tipo": "personalizada",
                "prazo": "20/06/2026",
                "prioridade": "media",
                "duracao_estimada": 2,
                "tempo_disponivel": 1,
                "descricao": "",
            }
        ]

        with tempfile.TemporaryDirectory() as diretorio:
            caminho = Path(diretorio) / "tarefas.json"
            caminho.write_text(json.dumps(dados), encoding="utf-8")

            tarefas = carregar_tarefas(caminho)

        self.assertEqual(len(tarefas), 1)
        self.assertEqual(tarefas[0].titulo, "Tarefa antiga")
        self.assertFalse(hasattr(tarefas[0], "tempo_disponivel"))
        self.assertEqual(tarefas[0].subtarefas_concluidas, [])
        self.assertFalse(tarefas[0].concluida)

    def test_salva_progresso_das_subtarefas(self):
        tarefa = Tarefa(
            titulo="Tarefa com progresso",
            tipo="personalizada",
            prazo="20/06/2026",
            prioridade="media",
            duracao_estimada=2,
            subtarefas_concluidas=["Analisar a tarefa."],
            concluida=True,
        )

        with tempfile.TemporaryDirectory() as diretorio:
            caminho = Path(diretorio) / "tarefas.json"
            salvar_tarefas([tarefa], caminho)
            tarefas = carregar_tarefas(caminho)

        self.assertEqual(
            tarefas[0].subtarefas_concluidas,
            ["Analisar a tarefa."],
        )
        self.assertTrue(tarefas[0].concluida)


if __name__ == "__main__":
    unittest.main()

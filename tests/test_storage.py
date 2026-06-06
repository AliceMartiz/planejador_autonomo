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

    def test_json_corrompido_retorna_lista_vazia(self):
        with tempfile.TemporaryDirectory() as diretorio:
            caminho = Path(diretorio) / "tarefas.json"
            caminho.write_bytes(b"\xff\xfeJSON invalido")

            tarefas = carregar_tarefas(caminho)

        self.assertEqual(tarefas, [])

    def test_ignora_tarefa_com_campos_invalidos(self):
        dados = [
            {
                "titulo": "Tarefa inválida",
                "tipo": "personalizada",
                "prazo": "data incorreta",
                "prioridade": "urgente",
                "duracao_estimada": -2,
            }
        ]

        with tempfile.TemporaryDirectory() as diretorio:
            caminho = Path(diretorio) / "tarefas.json"
            caminho.write_text(
                json.dumps(dados, ensure_ascii=False),
                encoding="utf-8",
            )

            tarefas = carregar_tarefas(caminho)

        self.assertEqual(tarefas, [])

    def test_normaliza_progresso_invalido(self):
        dados = [
            {
                "titulo": "Tarefa válida",
                "tipo": "trabalho academico",
                "prazo": "22/07/2026",
                "prioridade": "alta",
                "duracao_estimada": 2,
                "subtarefas_concluidas": [
                    "  Revisar texto  ",
                    123,
                    "",
                ],
            }
        ]

        with tempfile.TemporaryDirectory() as diretorio:
            caminho = Path(diretorio) / "tarefas.json"
            caminho.write_text(
                json.dumps(dados, ensure_ascii=False),
                encoding="utf-8",
            )

            tarefas = carregar_tarefas(caminho)

        self.assertEqual(
            tarefas[0].subtarefas_concluidas,
            ["Revisar texto", "123"],
        )

    def test_remove_temporario_quando_salvamento_falha(self):
        tarefa = Tarefa(
            titulo="Tarefa não serializável",
            tipo="personalizada",
            prazo="20/06/2026",
            prioridade="media",
            duracao_estimada=2,
            subtarefas_personalizadas=[{"valor": object()}],
        )

        with tempfile.TemporaryDirectory() as diretorio:
            caminho = Path(diretorio) / "tarefas.json"

            with self.assertRaises(TypeError):
                salvar_tarefas([tarefa], caminho)

            temporarios = list(Path(diretorio).glob("*.tmp"))

        self.assertEqual(temporarios, [])

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
        self.assertIsNone(tarefas[0].subtarefas_personalizadas)

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

    def test_salva_subtarefas_personalizadas(self):
        tarefa = Tarefa(
            titulo="Tarefa personalizada",
            tipo="personalizada",
            prazo="20/06/2026",
            prioridade="media",
            duracao_estimada=2,
            subtarefas_personalizadas=[
                {
                    "id": "etapa-1",
                    "nome": "Etapa personalizada",
                    "categoria": "pesquisa",
                    "motivo": "Ajuste feito pelo usuário.",
                    "ordem_logica": 1,
                }
            ],
        )

        with tempfile.TemporaryDirectory() as diretorio:
            caminho = Path(diretorio) / "tarefas.json"
            salvar_tarefas([tarefa], caminho)
            tarefas = carregar_tarefas(caminho)

        self.assertEqual(
            tarefas[0].subtarefas_personalizadas,
            tarefa.subtarefas_personalizadas,
        )


if __name__ == "__main__":
    unittest.main()

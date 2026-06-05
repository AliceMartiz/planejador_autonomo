"""Interface de terminal do Planejador Autônomo Acadêmico."""

from pathlib import Path

from models import Tarefa
from planner import gerar_plano
from storage import ARQUIVO_PADRAO, carregar_tarefas, salvar_tarefas
from validators import (
    converter_numero_positivo,
    normalizar_prioridade,
    validar_data,
    validar_numero_positivo,
    validar_prioridade,
)


TIPOS_DISPONIVEIS = [
    "trabalho academico",
    "estudar para prova",
    "apresentacao",
    "projeto de programacao",
    "rotina de estudos",
    "personalizada",
]


def mostrar_menu() -> None:
    """Mostra o menu principal."""

    print("\n=== Planejador Autônomo Acadêmico ===")
    print("1. Cadastrar nova tarefa")
    print("2. Listar tarefas carregadas")
    print("3. Gerar plano de uma tarefa")
    print("4. Salvar tarefas em JSON")
    print("5. Carregar tarefas salvas")
    print("6. Carregar exemplos do sample_data.json")
    print("7. Excluir uma tarefa")
    print("0. Sair")


def ler_texto_obrigatorio(mensagem: str) -> str:
    """Lê um texto que não pode ficar vazio."""

    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("Entrada obrigatória. Tente novamente.")


def ler_data_valida() -> str:
    """Lê uma data no formato dd/mm/aaaa."""

    while True:
        prazo = input("Prazo (dd/mm/aaaa): ").strip()
        if validar_data(prazo):
            return prazo
        print("Data inválida. Use o formato dd/mm/aaaa.")


def ler_prioridade_valida() -> str:
    """Lê uma prioridade válida."""

    while True:
        prioridade = input("Prioridade (baixa, media ou alta): ").strip()
        if validar_prioridade(prioridade):
            return normalizar_prioridade(prioridade)
        print("Prioridade inválida. Digite baixa, media ou alta.")


def ler_numero_valido(mensagem: str) -> float:
    """Lê um número positivo."""

    while True:
        valor = input(mensagem).strip().replace(",", ".")
        if validar_numero_positivo(valor):
            return converter_numero_positivo(valor, mensagem.replace(": ", ""))
        print("Valor inválido. Digite um número maior que zero.")


def escolher_tipo() -> str:
    """Permite escolher o tipo de tarefa por número."""

    print("\nTipos disponíveis:")
    for indice, tipo in enumerate(TIPOS_DISPONIVEIS, start=1):
        print(f"{indice}. {tipo}")

    while True:
        escolha = input("Escolha o tipo pelo número: ").strip()
        if escolha.isdigit():
            indice = int(escolha)
            if 1 <= indice <= len(TIPOS_DISPONIVEIS):
                return TIPOS_DISPONIVEIS[indice - 1]
        print("Opção inválida. Tente novamente.")


def cadastrar_tarefa() -> Tarefa:
    """Coleta dados do usuário e cria uma nova tarefa."""

    print("\nCadastro de tarefa")
    titulo = ler_texto_obrigatorio("Título da tarefa: ")
    descricao = input("Descrição curta (opcional): ").strip()
    tipo = escolher_tipo()
    prazo = ler_data_valida()
    prioridade = ler_prioridade_valida()
    duracao_estimada = ler_numero_valido("Duração estimada em horas: ")

    return Tarefa(
        titulo=titulo,
        descricao=descricao,
        tipo=tipo,
        prazo=prazo,
        prioridade=prioridade,
        duracao_estimada=duracao_estimada,
    )


def listar_tarefas(tarefas) -> None:
    """Mostra as tarefas carregadas na memória."""

    if not tarefas:
        print("\nNenhuma tarefa cadastrada.")
        return

    print("\nTarefas:")
    for indice, tarefa in enumerate(tarefas, start=1):
        print(
            f"{indice}. {tarefa.titulo} | tipo: {tarefa.tipo} | prazo: {tarefa.prazo} | "
            f"prioridade: {tarefa.prioridade}"
        )


def escolher_tarefa(tarefas):
    """Escolhe uma tarefa da lista pelo índice."""

    if not tarefas:
        print("\nNão há tarefas cadastradas.")
        return None

    listar_tarefas(tarefas)

    while True:
        escolha = input("Escolha o número da tarefa: ").strip()
        if escolha.isdigit():
            indice = int(escolha)
            if 1 <= indice <= len(tarefas):
                return tarefas[indice - 1]
        print("Opção inválida. Tente novamente.")


def excluir_tarefa(tarefas) -> bool:
    """Exclui uma tarefa após confirmação do usuário."""

    tarefa = escolher_tarefa(tarefas)
    if tarefa is None:
        return False

    while True:
        resposta = input(
            f'Deseja continuar e excluir a tarefa "{tarefa.titulo}"? (s/n): '
        ).strip().lower()

        if resposta in {"s", "sim"}:
            tarefas.remove(tarefa)
            salvar_tarefas(tarefas)
            print("Tarefa excluída com sucesso.")
            return True
        if resposta in {"n", "nao", "não"}:
            print("Exclusão cancelada.")
            return False

        print("Resposta inválida. Digite s para sim ou n para não.")


def mostrar_plano(tarefa: Tarefa) -> None:
    """Gera e mostra o plano no terminal."""

    plano = gerar_plano(tarefa)

    print("\n=== Plano gerado ===")
    print(f"Tarefa: {plano.tarefa.titulo}")
    print(f"Tipo identificado: {plano.tipo_identificado}")
    print(f"Dias restantes: {plano.dias_restantes}")
    print(f"Urgência: {plano.urgencia}")
    print(f"Pontuação: {plano.pontuacao}")

    print("\nOrdem recomendada:")
    for subtarefa in plano.subtarefas:
        print(f"{subtarefa.ordem_logica}. {subtarefa.nome} ({subtarefa.categoria})")
        print(f"   Motivo: {subtarefa.motivo}")

    print("\nJustificativa:")
    print(plano.justificativa)


def carregar_exemplos():
    """Carrega tarefas de exemplo do arquivo sample_data.json."""

    caminho_exemplos = Path(__file__).with_name("sample_data.json")
    return carregar_tarefas(caminho_exemplos)


def executar_menu() -> None:
    """Controla o laço principal da interface de terminal."""

    tarefas = carregar_tarefas()

    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            tarefas.append(cadastrar_tarefa())
            print("Tarefa cadastrada com sucesso.")
        elif opcao == "2":
            listar_tarefas(tarefas)
        elif opcao == "3":
            tarefa = escolher_tarefa(tarefas)
            if tarefa:
                mostrar_plano(tarefa)
        elif opcao == "4":
            salvar_tarefas(tarefas)
            print(f"Tarefas salvas em {ARQUIVO_PADRAO}.")
        elif opcao == "5":
            tarefas = carregar_tarefas()
            print(f"{len(tarefas)} tarefa(s) carregada(s).")
        elif opcao == "6":
            exemplos = carregar_exemplos()
            tarefas.extend(exemplos)
            print(f"{len(exemplos)} exemplo(s) carregado(s).")
        elif opcao == "7":
            excluir_tarefa(tarefas)
        elif opcao == "0":
            print("Encerrando o planejador.")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    executar_menu()

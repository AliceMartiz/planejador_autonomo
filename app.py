"""Interface visual do Planejador Autônomo Acadêmico."""

import streamlit as st

from componentes_subtarefas import capturar_nova_ordem
from models import Tarefa
from planner import TIPOS_DISPONIVEIS, gerar_plano
from storage import carregar_tarefas, salvar_tarefas
from ui_tarefas import (
    atualizar_dados_planejamento,
    filtrar_tarefas,
    ordenar_tarefas,
    remover_tarefas_terminadas,
    todas_subtarefas_concluidas,
)
from ui_subtarefas import (
    criar_subtarefa_editavel,
    converter_subtarefas,
    editar_subtarefa,
    inserir_subtarefa_abaixo,
    normalizar_subtarefas,
    reordenar_subtarefas,
    remover_subtarefa,
)
from validators import (
    converter_data,
    converter_numero_positivo,
    normalizar_prioridade,
    validar_data,
    validar_numero_positivo,
    validar_prioridade,
)

OPCOES_ORDENACAO = [
    "Padrão",
    "Prazo mais próximo",
    "Maior pontuação",
    "Prioridade mais alta",
    "Maior duração",
]

OPCOES_FILTRO_TAREFAS = [
    "Todas as tarefas",
    "Tarefas terminadas",
    "Tarefas atrasadas",
]

ABAS_PRINCIPAIS = [
    "Gerar plano",
    "Tarefas salvas",
    "Sobre o projeto",
]


def aplicar_estilos() -> None:
    """Aplica os estilos visuais da interface."""

    st.markdown(
        """
        <style>
        :root {
            --academico-verde: #2f6b5f;
            --academico-verde-claro: rgba(47, 107, 95, 0.10);
            --academico-borda: rgba(89, 103, 116, 0.22);
            --academico-texto-suave: #64717d;
        }

        html, body, [class*="css"] {
            letter-spacing: 0;
        }

        .block-container {
            max-width: 1180px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        .app-header {
            padding: 0.4rem 0 1.5rem;
            margin-bottom: 1rem;
            border-bottom: 1px solid var(--academico-borda);
        }

        .app-header h1 {
            margin: 0.2rem 0 0.5rem;
            font-size: clamp(2rem, 4vw, 3rem);
            line-height: 1.08;
            letter-spacing: 0;
        }

        .app-header .app-kicker {
            margin: 0;
            color: var(--academico-verde);
            font-size: 0.86rem;
            font-weight: 650;
        }

        .app-header .app-subtitle {
            max-width: 760px;
            margin: 0;
            color: var(--academico-texto-suave);
            font-size: 1.02rem;
            line-height: 1.6;
        }

        [data-testid="stSidebar"] {
            border-right: 1px solid var(--academico-borda);
        }

        [data-testid="stSidebar"] .block-container {
            padding-top: 1.7rem;
        }

        [data-testid="stForm"] {
            padding: 1.25rem;
            border: 1px solid var(--academico-borda);
            border-radius: 8px;
            box-shadow: 0 8px 24px rgba(30, 47, 61, 0.045);
        }

        div[data-testid="stMetric"] {
            min-height: 102px;
            padding: 0.85rem 1rem;
            border: 1px solid var(--academico-borda);
            border-radius: 8px;
            background-color: rgba(255, 255, 255, 0.42);
        }

        .st-key-resumo_plano_recente {
            padding: 1.1rem;
            border: 1px solid var(--academico-borda);
            border-radius: 8px;
            background-color: rgba(47, 107, 95, 0.045);
        }

        .st-key-botao_ajuda_pontuacao {
            position: fixed;
            left: 1rem;
            bottom: 1rem;
            z-index: 999;
            width: 3rem;
        }

        .st-key-botao_ajuda_pontuacao button {
            width: 3rem;
            height: 3rem;
            min-height: 3rem;
            padding: 0;
            border-radius: 50%;
            box-shadow: 0 5px 16px rgba(28, 43, 54, 0.18);
        }

        .st-key-lista_tarefas {
            padding-bottom: 0.35rem;
            overflow: hidden;
            border: 1px solid var(--academico-borda);
            border-radius: 8px;
        }

        .st-key-cabecalho_tarefas {
            padding: 0.7rem 0.8rem 0.35rem;
            background-color: rgba(47, 107, 95, 0.06);
        }

        .st-key-cabecalho_subtarefas {
            padding: 0.65rem 0.65rem 0.35rem;
            margin-bottom: 0.25rem;
            border-radius: 7px;
            background-color: rgba(47, 107, 95, 0.08);
        }

        [class*="st-key-bloco_subtarefa_"] {
            position: relative;
            gap: 0;
            margin-bottom: -0.45rem;
        }

        .st-key-cabecalho_secao_tarefas {
            position: relative;
            padding-right: 9rem;
        }

        .st-key-controles_tarefas {
            position: absolute;
            top: 0.15rem;
            right: 0;
            z-index: 4;
            width: 8.75rem;
        }

        .st-key-controles_tarefas
        [data-testid="stHorizontalBlock"] {
            gap: 0.25rem;
        }

        .st-key-controles_tarefas
        [data-testid="stColumn"] {
            width: 2.75rem !important;
            min-width: 2.75rem !important;
        }

        .st-key-controles_tarefas button {
            width: 2.75rem;
            height: 2.75rem;
            padding: 0;
        }

        .st-key-limpar_tarefas_terminadas button:hover:not(:disabled) {
            border-color: rgba(185, 28, 28, 0.38);
            background-color: rgba(185, 28, 28, 0.06);
            color: #b91c1c;
        }

        [class*="st-key-linha_tarefa_"],
        [class*="st-key-linha_subtarefa_"] {
            position: relative;
            cursor: pointer;
        }

        [class*="st-key-linha_tarefa_"] {
            padding: 0.45rem 0.8rem 0.7rem;
            transition: background-color 160ms ease;
        }

        [class*="st-key-linha_tarefa_"]:hover {
            background-color: rgba(47, 107, 95, 0.075);
        }

        [class*="st-key-linha_tarefa_concluida_"] {
            background-color: rgba(34, 197, 94, 0.13);
        }

        [class*="st-key-linha_tarefa_concluida_"]:hover {
            background-color: rgba(34, 197, 94, 0.19);
        }

        [class*="st-key-abrir_linha_tarefa_"] {
            position: absolute;
            inset: 0 3.5rem 0 0;
            width: calc(100% - 3.5rem) !important;
            max-width: none !important;
            z-index: 2;
        }

        [class*="st-key-alternar_subtarefa_"] {
            position: absolute;
            inset: 0;
            width: 100% !important;
            max-width: none !important;
            z-index: 2;
        }

        [class*="st-key-abrir_linha_tarefa_"] button,
        [class*="st-key-alternar_subtarefa_"] button {
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100% !important;
            min-height: 100%;
            padding: 0;
            border: 0;
            opacity: 0;
            cursor: pointer;
        }

        [class*="st-key-excluir_tarefa_"] {
            position: absolute;
            top: 50%;
            right: 0.75rem;
            z-index: 3;
            transform: translateY(-50%);
        }

        [class*="st-key-linha_subtarefa_"] {
            padding: 0.48rem 0.65rem;
            margin: 0;
            border-radius: 7px;
            transition: background-color 160ms ease, opacity 160ms ease;
        }

        [class*="st-key-linha_subtarefa_"]:hover {
            background-color: rgba(47, 107, 95, 0.075);
        }

        [class*="st-key-linha_subtarefa_concluida_"] {
            background-color: rgba(100, 116, 139, 0.07);
        }

        [class*="st-key-linha_subtarefa_concluida_"]
        [data-testid="stColumn"]:not(:nth-child(5)) p,
        [class*="st-key-linha_subtarefa_concluida_"]
        [data-testid="stColumn"]:not(:nth-child(5)) code,
        [class*="st-key-linha_subtarefa_concluida_"]
        [data-testid="stColumn"]:not(:nth-child(5)) span {
            text-decoration: line-through;
            text-decoration-thickness: 1px;
            opacity: 0.52;
        }

        [class*="st-key-area_inserir_subtarefa_"] button,
        [class*="st-key-acao_editar_subtarefa_"] button,
        [class*="st-key-acao_excluir_subtarefa_"] button {
            width: 1.8rem;
            height: 1.55rem;
            min-height: 1.55rem;
            padding: 0;
            border: 1px solid var(--academico-borda);
            border-radius: 999px;
            background-color: #f7f9fa;
            color: var(--academico-verde);
            box-shadow: 0 1px 5px rgba(30, 47, 61, 0.08);
        }

        [class*="st-key-area_inserir_subtarefa_"] {
            position: relative;
            z-index: 5;
            height: 0.8rem;
            min-height: 0.8rem;
            margin: -0.08rem 0 -0.18rem;
            opacity: 0;
            transition: opacity 180ms ease;
        }

        [class*="st-key-bloco_subtarefa_"]:hover
        [class*="st-key-area_inserir_subtarefa_"],
        [class*="st-key-area_inserir_subtarefa_"]:hover,
        [class*="st-key-area_inserir_subtarefa_"]:focus-within {
            opacity: 1;
        }

        [class*="st-key-area_inserir_subtarefa_"]
        [data-testid="stHorizontalBlock"] {
            display: grid;
            position: absolute;
            top: 0;
            right: 0;
            left: 0;
            transform: translateY(-42%);
            grid-template-columns:
                minmax(0, 1fr)
                1.8rem
                1.8rem
                1.8rem
                minmax(0, 1fr);
            gap: 0.22rem;
            min-height: 1.55rem;
            align-items: center;
        }

        [class*="st-key-area_inserir_subtarefa_"]
        [data-testid="stColumn"] {
            width: auto !important;
            min-width: 0 !important;
        }

        [class*="st-key-editor_subtarefa_"],
        [class*="st-key-confirmacao_subtarefa_"] {
            padding: 0.8rem 0.9rem 0.9rem;
            margin: 0.3rem 0 0.55rem;
            border: 1px solid var(--academico-borda);
            border-radius: 7px;
            background-color: rgba(47, 107, 95, 0.035);
        }

        [class*="st-key-editor_subtarefa_"] [data-testid="stForm"] {
            padding: 0;
            border: 0;
            background: transparent;
        }

        [class*="st-key-editor_subtarefa_"] h5 {
            margin-bottom: 0.15rem;
            font-size: 0.98rem;
        }

        .st-key-detalhes_planejamento {
            position: relative;
            margin: 0.15rem 0 0.65rem;
            padding-top: 0.15rem;
        }

        .st-key-detalhes_planejamento > div:first-child p {
            color: var(--academico-texto-suave);
            font-size: 0.86rem;
            font-weight: 650;
        }

        [class*="st-key-editar_dados_tarefa_"] {
            position: absolute;
            top: -0.2rem;
            right: 0;
            z-index: 3;
        }

        [class*="st-key-editar_dados_tarefa_"] button {
            width: 2.35rem;
            height: 2.35rem;
            min-height: 2.35rem;
            padding: 0;
        }

        .st-key-editor_dados_planejamento {
            padding: 0.8rem 0.9rem 0.9rem;
            margin: 0.2rem 0 0.7rem;
            border: 1px solid var(--academico-borda);
            border-radius: 7px;
            background-color: rgba(47, 107, 95, 0.035);
        }

        .st-key-editor_dados_planejamento [data-testid="stForm"] {
            padding: 0;
            border: 0;
            background: transparent;
            box-shadow: none;
        }

        [class*="st-key-editor_subtarefa_"] textarea {
            min-height: 5.5rem;
        }

        @media (hover: none) {
            [class*="st-key-area_inserir_subtarefa_"] {
                opacity: 0.55;
            }
        }

        .app-footer {
            padding-top: 1.4rem;
            margin-top: 2rem;
            border-top: 1px solid var(--academico-borda);
            color: var(--academico-texto-suave);
            font-size: 0.82rem;
            text-align: center;
        }

        @media (max-width: 640px) {
            .block-container {
                padding: 1.1rem 1rem 2.5rem;
            }

            .app-header {
                padding-bottom: 1.15rem;
            }

            .app-header h1 {
                font-size: 2rem;
            }

            .st-key-botao_ajuda_pontuacao {
                left: 0.75rem;
                bottom: 0.75rem;
            }

            .st-key-cabecalho_tarefas,
            .st-key-cabecalho_subtarefas {
                display: none;
            }

            .st-key-lista_tarefas {
                padding: 0.35rem;
            }

            [class*="st-key-linha_tarefa_"] {
                padding: 0.85rem 0.8rem;
                border-radius: 7px;
            }

            [class*="st-key-linha_tarefa_"] [data-testid="stHorizontalBlock"] {
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: 0.75rem 1rem;
                width: 100%;
            }

            [class*="st-key-linha_tarefa_"] [data-testid="stColumn"],
            [class*="st-key-linha_subtarefa_"] [data-testid="stColumn"] {
                width: auto !important;
                min-width: 0 !important;
            }

            [class*="st-key-linha_tarefa_"] [data-testid="stColumn"]::before {
                display: block;
                margin-bottom: 0.18rem;
                color: var(--academico-texto-suave);
                font-size: 0.75rem;
                line-height: 1.2;
            }

            [class*="st-key-linha_tarefa_"] [data-testid="stColumn"]:nth-child(1),
            [class*="st-key-linha_tarefa_"] [data-testid="stColumn"]:nth-child(2) {
                grid-column: 1 / -1;
            }

            [class*="st-key-linha_tarefa_"] [data-testid="stColumn"]:nth-child(1)::before {
                content: "Tarefa";
            }

            [class*="st-key-linha_tarefa_"] [data-testid="stColumn"]:nth-child(2)::before {
                content: "Tipo";
            }

            [class*="st-key-linha_tarefa_"] [data-testid="stColumn"]:nth-child(3)::before {
                content: "Prazo";
            }

            [class*="st-key-linha_tarefa_"] [data-testid="stColumn"]:nth-child(4)::before {
                content: "Prioridade";
            }

            [class*="st-key-linha_tarefa_"] [data-testid="stColumn"]:nth-child(5)::before {
                content: "Duração";
            }

            [class*="st-key-linha_tarefa_"] [data-testid="stColumn"]:nth-child(1) p {
                font-weight: 650;
            }

            [class*="st-key-linha_subtarefa_"] {
                padding: 0.75rem;
                margin: 0.3rem 0;
                background-color: rgba(47, 107, 95, 0.045);
            }

            [class*="st-key-linha_subtarefa_"] [data-testid="stHorizontalBlock"] {
                display: grid;
                grid-template-columns: 2rem minmax(0, 1fr);
                gap: 0.25rem 0.65rem;
                width: 100%;
            }

            [class*="st-key-linha_subtarefa_"] [data-testid="stColumn"]:nth-child(1) {
                grid-column: 1;
                grid-row: 1 / span 2;
                align-self: start;
            }

            [class*="st-key-linha_subtarefa_"] [data-testid="stColumn"]:nth-child(2) {
                grid-column: 2;
                grid-row: 1;
            }

            [class*="st-key-linha_subtarefa_"] [data-testid="stColumn"]:nth-child(2) p {
                font-weight: 650;
            }

            [class*="st-key-linha_subtarefa_"] [data-testid="stColumn"]:nth-child(3) {
                grid-column: 2;
                grid-row: 2;
            }

            [class*="st-key-linha_subtarefa_"] [data-testid="stColumn"]:nth-child(3) p {
                color: var(--academico-texto-suave);
                font-size: 0.78rem;
            }

            [class*="st-key-linha_subtarefa_"] [data-testid="stColumn"]:nth-child(4) {
                grid-column: 1 / -1;
                grid-row: 3;
                padding-top: 0.35rem;
            }

            [class*="st-key-linha_subtarefa_"] [data-testid="stColumn"]:nth-child(4) p {
                color: var(--academico-texto-suave);
                font-size: 0.86rem;
                line-height: 1.45;
            }

            [class*="st-key-area_inserir_subtarefa_"] {
                height: 0.95rem;
                min-height: 0.95rem;
                opacity: 0.55;
            }

            [class*="st-key-excluir_tarefa_"] {
                top: 0.75rem !important;
                transform: none !important;
            }
        }

        @media (max-width: 420px) {
            [class*="st-key-linha_tarefa_"] [data-testid="stHorizontalBlock"] {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def iniciar_estado() -> None:
    """Cria os valores usados no estado da página."""

    if "tarefas" not in st.session_state:
        st.session_state.tarefas = carregar_tarefas()
    if "indice_plano_recente" not in st.session_state:
        st.session_state.indice_plano_recente = None
    if "indice_plano_aberto" not in st.session_state:
        st.session_state.indice_plano_aberto = None
    if "subtarefas_editaveis" not in st.session_state:
        st.session_state.subtarefas_editaveis = {}
    if "editor_subtarefa" not in st.session_state:
        st.session_state.editor_subtarefa = None
    if "indice_tarefa_em_edicao" not in st.session_state:
        st.session_state.indice_tarefa_em_edicao = None
    if "mensagem_plano" not in st.session_state:
        st.session_state.mensagem_plano = None


def reiniciar_estado_dependente_tarefas() -> None:
    """Descarta seleções que podem apontar para índices antigos."""

    st.session_state.indice_plano_recente = None
    st.session_state.indice_plano_aberto = None
    st.session_state.subtarefas_editaveis = {}
    st.session_state.editor_subtarefa = None
    st.session_state.indice_tarefa_em_edicao = None
    st.session_state.mensagem_plano = None


def validar_formulario(
    prazo: str,
    prioridade: str,
    duracao: float,
) -> list[str]:
    """Valida os campos antes de gerar a tarefa."""

    erros = []

    if not validar_data(prazo):
        erros.append("Escolha uma data de prazo válida.")
    if not validar_prioridade(prioridade):
        erros.append("Escolha uma prioridade válida.")
    if not validar_numero_positivo(duracao):
        erros.append("A duração estimada deve ser maior que zero.")

    return erros


def obter_subtarefas_editaveis(indice_tarefa: int, plano):
    """Obtém a lista editável da tarefa e preserva seu estado."""

    chave = str(indice_tarefa)
    tarefa = st.session_state.tarefas[indice_tarefa]

    if chave not in st.session_state.subtarefas_editaveis:
        if tarefa.subtarefas_personalizadas is None:
            subtarefas = converter_subtarefas(plano.subtarefas)
        else:
            subtarefas = normalizar_subtarefas(
                tarefa.subtarefas_personalizadas
            )
        st.session_state.subtarefas_editaveis[chave] = subtarefas

    return st.session_state.subtarefas_editaveis[chave]


def persistir_subtarefas_editaveis(
    indice_tarefa: int,
    subtarefas,
) -> None:
    """Atualiza o estado e salva a personalização no JSON."""

    chave = str(indice_tarefa)
    subtarefas_normalizadas = normalizar_subtarefas(subtarefas)
    tarefa = st.session_state.tarefas[indice_tarefa]
    tarefa.subtarefas_personalizadas = subtarefas_normalizadas
    st.session_state.subtarefas_editaveis[chave] = subtarefas_normalizadas

    nomes_atuais = {
        subtarefa["nome"]
        for subtarefa in subtarefas_normalizadas
    }
    tarefa.subtarefas_concluidas = [
        nome
        for nome in tarefa.subtarefas_concluidas
        if nome in nomes_atuais
    ]
    tarefa.concluida = bool(nomes_atuais) and nomes_atuais.issubset(
        set(tarefa.subtarefas_concluidas)
    )
    salvar_tarefas(st.session_state.tarefas)


def abrir_editor_subtarefa(
    acao: str,
    indice_tarefa: int,
    identificador: str = "",
) -> None:
    """Define qual formulário de subtarefa deve aparecer."""

    st.session_state.editor_subtarefa = {
        "acao": acao,
        "indice_tarefa": indice_tarefa,
        "identificador": identificador,
    }


def fechar_editor_subtarefa() -> None:
    """Fecha o formulário ou confirmação em uso."""

    st.session_state.editor_subtarefa = None


def abrir_plano(indice_tarefa: int) -> None:
    """Mantém o plano selecionado aberto durante as interações."""

    st.session_state.indice_plano_aberto = indice_tarefa


def fechar_plano() -> None:
    """Limpa o plano selecionado quando a janela é fechada."""

    st.session_state.indice_plano_aberto = None
    st.session_state.indice_tarefa_em_edicao = None
    st.session_state.mensagem_plano = None
    fechar_editor_subtarefa()


def alternar_subtarefa(indice_tarefa: int, nome_subtarefa: str) -> None:
    """Alterna uma subtarefa e salva o progresso."""

    tarefa = st.session_state.tarefas[indice_tarefa]

    if nome_subtarefa in tarefa.subtarefas_concluidas:
        tarefa.subtarefas_concluidas.remove(nome_subtarefa)
        tarefa.concluida = False
    else:
        tarefa.subtarefas_concluidas.append(nome_subtarefa)

    salvar_tarefas(st.session_state.tarefas)


def definir_tarefa_concluida(indice: int, concluida: bool) -> None:
    """Atualiza e salva o estado de conclusão de uma tarefa."""

    st.session_state.tarefas[indice].concluida = concluida
    salvar_tarefas(st.session_state.tarefas)


def abrir_edicao_tarefa(indice_tarefa: int) -> None:
    """Ativa a edição dos critérios da tarefa aberta."""

    st.session_state.indice_tarefa_em_edicao = indice_tarefa


def cancelar_edicao_tarefa() -> None:
    """Fecha a edição sem alterar a tarefa."""

    st.session_state.indice_tarefa_em_edicao = None


def renderizar_editor_dados_tarefa(
    tarefa: Tarefa,
    indice_tarefa: int,
) -> None:
    """Edita prioridade, prazo e duração dentro do planejamento."""

    prioridades = ["baixa", "media", "alta"]
    with st.container(key="editor_dados_planejamento"):
        st.markdown("##### Editar dados do planejamento")

        with st.form(
            f"formulario_editar_tarefa_{indice_tarefa}",
            border=False,
        ):
            coluna_prioridade, coluna_prazo, coluna_duracao = st.columns(3)
            prioridade = coluna_prioridade.selectbox(
                "Prioridade",
                prioridades,
                index=prioridades.index(tarefa.prioridade),
                format_func=lambda valor: (
                    "Média" if valor == "media" else valor.title()
                ),
            )
            prazo = coluna_prazo.date_input(
                "Prazo",
                value=converter_data(tarefa.prazo),
                format="DD/MM/YYYY",
            )
            duracao = coluna_duracao.number_input(
                "Duração estimada",
                min_value=0.5,
                value=float(tarefa.duracao_estimada),
                step=0.5,
                help="Total aproximado de horas para concluir a tarefa.",
            )

            coluna_cancelar, coluna_salvar = st.columns(2)
            cancelar = coluna_cancelar.form_submit_button(
                "Cancelar",
                use_container_width=True,
            )
            salvar = coluna_salvar.form_submit_button(
                "Atualizar planejamento",
                icon=":material/check:",
                type="primary",
                use_container_width=True,
            )

        if cancelar:
            cancelar_edicao_tarefa()
            st.rerun(scope="app")

        if not salvar:
            return

        prazo_formatado = prazo.strftime("%d/%m/%Y")
        erros = validar_formulario(
            prazo_formatado,
            prioridade,
            duracao,
        )
        if erros:
            for erro in erros:
                st.error(erro)
            return

        atualizar_dados_planejamento(
            tarefa,
            prioridade,
            prazo_formatado,
            converter_numero_positivo(
                duracao,
                "Duração estimada",
            ),
        )
        st.session_state.subtarefas_editaveis.pop(
            str(indice_tarefa),
            None,
        )
        salvar_tarefas(st.session_state.tarefas)
        cancelar_edicao_tarefa()
        st.session_state.mensagem_plano = (
            "Dados atualizados e planejamento recalculado."
        )
        st.rerun(scope="app")


def mostrar_detalhes_tarefa(
    tarefa: Tarefa,
    indice_tarefa: int | None,
) -> None:
    """Mostra ou edita os critérios informados pelo usuário."""

    if (
        indice_tarefa is not None
        and st.session_state.indice_tarefa_em_edicao == indice_tarefa
    ):
        renderizar_editor_dados_tarefa(tarefa, indice_tarefa)
        return

    with st.container(key="detalhes_planejamento"):
        st.caption("Dados do planejamento")
        if indice_tarefa is not None:
            st.button(
                "",
                icon=":material/edit:",
                help="Editar prioridade, prazo e duração",
                key=f"editar_dados_tarefa_{indice_tarefa}",
                on_click=abrir_edicao_tarefa,
                args=(indice_tarefa,),
            )

        coluna1, coluna2, coluna3 = st.columns(3)
        coluna1.markdown(f"**Prioridade**  \n{tarefa.prioridade.title()}")
        coluna2.markdown(f"**Prazo**  \n{tarefa.prazo}")
        coluna3.markdown(
            f"**Duração estimada**  \n{tarefa.duracao_estimada:g} hora(s)"
        )


def editor_subtarefa_ativo(
    acao: str,
    indice_tarefa: int,
    identificador: str,
) -> bool:
    """Informa se o editor atual corresponde à subtarefa indicada."""

    editor = st.session_state.editor_subtarefa
    return bool(
        editor
        and editor["acao"] == acao
        and editor["indice_tarefa"] == indice_tarefa
        and editor["identificador"] == identificador
    )


def renderizar_formulario_subtarefa(
    indice_tarefa: int,
    subtarefas,
    acao: str,
    identificador: str,
) -> None:
    """Renderiza o formulário de criação ou edição de uma subtarefa."""

    if acao == "editar":
        subtarefa_atual = next(
            subtarefa
            for subtarefa in subtarefas
            if subtarefa["id"] == identificador
        )
        titulo_formulario = "Editar subtarefa"
        nome_inicial = str(subtarefa_atual["nome"])
        categoria_inicial = str(subtarefa_atual["categoria"])
        motivo_inicial = str(subtarefa_atual["motivo"])
    else:
        subtarefa_atual = None
        titulo_formulario = "Adicionar subtarefa"
        nome_inicial = ""
        categoria_inicial = "execução"
        motivo_inicial = ""

    with st.container(
        key=f"editor_subtarefa_{acao}_{indice_tarefa}_{identificador}"
    ):
        st.markdown(f"##### {titulo_formulario}")

        with st.form(
            f"formulario_subtarefa_{acao}_{indice_tarefa}_{identificador}",
            border=False,
        ):
            coluna_nome, coluna_categoria = st.columns([1.8, 1])
            nome = coluna_nome.text_input(
                "Nome da subtarefa",
                value=nome_inicial,
                placeholder="Ex.: revisar os exemplos do trabalho",
            )
            categoria = coluna_categoria.text_input(
                "Categoria",
                value=categoria_inicial,
                placeholder="Ex.: planejamento",
            )
            motivo = st.text_area(
                "Justificativa",
                value=motivo_inicial,
                placeholder="Explique por que esta etapa faz parte do plano.",
                height=96,
            )

            coluna_cancelar, coluna_salvar = st.columns(2)
            cancelar = coluna_cancelar.form_submit_button(
                "Cancelar",
                use_container_width=True,
            )
            salvar = coluna_salvar.form_submit_button(
                "Salvar subtarefa",
                icon=":material/check:",
                type="primary",
                use_container_width=True,
            )

        if cancelar:
            fechar_editor_subtarefa()
            st.rerun(scope="fragment")

        if not salvar:
            return

        if not nome.strip() or not categoria.strip():
            st.error("Informe o nome e a categoria da subtarefa.")
            return

        nomes_outras_subtarefas = {
            str(subtarefa["nome"]).strip().casefold()
            for subtarefa in subtarefas
            if subtarefa["id"] != identificador
        }
        if nome.strip().casefold() in nomes_outras_subtarefas:
            st.error("Já existe uma subtarefa com esse nome.")
            return

        tarefa = st.session_state.tarefas[indice_tarefa]

        if acao == "editar":
            nome_anterior = str(subtarefa_atual["nome"])
            atualizadas = editar_subtarefa(
                subtarefas,
                identificador,
                nome,
                categoria,
                motivo,
            )
            if nome_anterior in tarefa.subtarefas_concluidas:
                tarefa.subtarefas_concluidas.remove(nome_anterior)
                tarefa.subtarefas_concluidas.append(nome.strip())
        else:
            nova_subtarefa = criar_subtarefa_editavel(
                nome=nome,
                categoria=categoria,
                motivo=motivo,
            )
            atualizadas = inserir_subtarefa_abaixo(
                subtarefas,
                identificador,
                nova_subtarefa,
            )
            tarefa.concluida = False

        persistir_subtarefas_editaveis(indice_tarefa, atualizadas)
        fechar_editor_subtarefa()
        st.rerun(scope="fragment")


def renderizar_confirmacao_exclusao_subtarefa(
    indice_tarefa: int,
    subtarefas,
    identificador: str,
) -> None:
    """Pede confirmação antes de remover uma subtarefa."""

    subtarefa = next(
        item
        for item in subtarefas
        if item["id"] == identificador
    )

    with st.container(
        key=f"confirmacao_subtarefa_{indice_tarefa}_{identificador}"
    ):
        st.write(f'Excluir a subtarefa "{subtarefa["nome"]}"?')
        coluna_cancelar, coluna_excluir = st.columns(2)

        if coluna_cancelar.button(
            "Cancelar",
            key=(
                f"cancelar_exclusao_subtarefa_"
                f"{indice_tarefa}_{identificador}"
            ),
            use_container_width=True,
        ):
            fechar_editor_subtarefa()
            st.rerun(scope="fragment")

        if coluna_excluir.button(
            "Excluir",
            key=(
                f"confirmar_exclusao_subtarefa_"
                f"{indice_tarefa}_{identificador}"
            ),
            icon=":material/delete:",
            type="primary",
            use_container_width=True,
        ):
            tarefa = st.session_state.tarefas[indice_tarefa]
            nome = str(subtarefa["nome"])
            if nome in tarefa.subtarefas_concluidas:
                tarefa.subtarefas_concluidas.remove(nome)

            atualizadas = remover_subtarefa(
                subtarefas,
                identificador,
            )
            persistir_subtarefas_editaveis(
                indice_tarefa,
                atualizadas,
            )
            fechar_editor_subtarefa()
            st.rerun(scope="fragment")


def renderizar_subtarefas_editaveis(plano, indice_tarefa: int) -> None:
    """Exibe a lista interativa de subtarefas do planejamento."""

    subtarefas = obter_subtarefas_editaveis(indice_tarefa, plano)
    tarefa = plano.tarefa
    concluidas = set(tarefa.subtarefas_concluidas)

    if subtarefas:
        with st.container(key="cabecalho_subtarefas"):
            cabecalho = st.columns([0.55, 1.9, 1.05, 2.6])
            for coluna, titulo in zip(
                cabecalho,
                ["Ordem", "Subtarefa", "Categoria", "Motivo"],
            ):
                coluna.caption(titulo)
    else:
        st.info("O plano está sem subtarefas. Adicione uma nova etapa.")

    for subtarefa in subtarefas:
        identificador = str(subtarefa["id"])
        nome = str(subtarefa["nome"])
        concluida = nome in concluidas
        estado = "concluida" if concluida else "pendente"

        with st.container(
            key=f"bloco_subtarefa_{indice_tarefa}_{identificador}"
        ):
            with st.container(
                key=(
                    f"linha_subtarefa_{estado}_{indice_tarefa}_"
                    f"{identificador}"
                )
            ):
                colunas = st.columns(
                    [0.55, 1.9, 1.05, 2.6],
                    vertical_alignment="center",
                )
                colunas[0].write(subtarefa["ordem_logica"])
                colunas[1].write(nome)
                colunas[2].write(subtarefa["categoria"])
                colunas[3].write(subtarefa["motivo"])

                st.button(
                    f"Alternar {nome}",
                    key=(
                        f"alternar_subtarefa_{indice_tarefa}_"
                        f"{identificador}_{estado}"
                    ),
                    on_click=alternar_subtarefa,
                    args=(indice_tarefa, nome),
                )
                st.button(
                    "",
                    icon=":material/drag_indicator:",
                    help=f"Arrastar {nome} para reordenar",
                    key=(
                        f"arrastar_subtarefa_{indice_tarefa}_"
                        f"{identificador}"
                    ),
                )

            if editor_subtarefa_ativo(
                "editar",
                indice_tarefa,
                identificador,
            ):
                renderizar_formulario_subtarefa(
                    indice_tarefa,
                    subtarefas,
                    "editar",
                    identificador,
                )

            if editor_subtarefa_ativo(
                "excluir",
                indice_tarefa,
                identificador,
            ):
                renderizar_confirmacao_exclusao_subtarefa(
                    indice_tarefa,
                    subtarefas,
                    identificador,
                )

            with st.container(
                key=(
                    f"area_inserir_subtarefa_"
                    f"{indice_tarefa}_{identificador}"
                )
            ):
                (
                    _,
                    coluna_adicionar,
                    coluna_editar,
                    coluna_excluir,
                    _,
                ) = st.columns(
                    [1, 0.1, 0.1, 0.1, 1],
                    gap="small",
                    vertical_alignment="center",
                )
                coluna_adicionar.button(
                    "",
                    icon=":material/add:",
                    type="tertiary",
                    help=f"Adicionar subtarefa abaixo de {nome}",
                    key=(
                        f"adicionar_subtarefa_abaixo_"
                        f"{indice_tarefa}_{identificador}"
                    ),
                    on_click=abrir_editor_subtarefa,
                    args=("adicionar", indice_tarefa, identificador),
                )
                coluna_editar.button(
                    "",
                    icon=":material/edit:",
                    type="tertiary",
                    help=f"Editar {nome}",
                    key=(
                        f"acao_editar_subtarefa_"
                        f"{indice_tarefa}_{identificador}"
                    ),
                    on_click=abrir_editor_subtarefa,
                    args=("editar", indice_tarefa, identificador),
                )
                coluna_excluir.button(
                    "",
                    icon=":material/delete:",
                    type="tertiary",
                    help=f"Excluir {nome}",
                    key=(
                        f"acao_excluir_subtarefa_"
                        f"{indice_tarefa}_{identificador}"
                    ),
                    on_click=abrir_editor_subtarefa,
                    args=("excluir", indice_tarefa, identificador),
                )

            if editor_subtarefa_ativo(
                "adicionar",
                indice_tarefa,
                identificador,
            ):
                renderizar_formulario_subtarefa(
                    indice_tarefa,
                    subtarefas,
                    "adicionar",
                    identificador,
                )

    if len(subtarefas) > 1:
        identificadores = [
            str(subtarefa["id"])
            for subtarefa in subtarefas
        ]
        nova_ordem = capturar_nova_ordem(
            indice_tarefa,
            identificadores,
        )
        if nova_ordem and nova_ordem != identificadores:
            atualizadas = reordenar_subtarefas(
                subtarefas,
                nova_ordem,
            )
            ordem_atualizada = [
                str(subtarefa["id"])
                for subtarefa in atualizadas
            ]
            if ordem_atualizada != identificadores:
                persistir_subtarefas_editaveis(
                    indice_tarefa,
                    atualizadas,
                )
                st.rerun(scope="fragment")

    if not subtarefas:
        identificador = ""
        st.button(
            "Adicionar primeira subtarefa",
            icon=":material/add:",
            key=f"adicionar_primeira_subtarefa_{indice_tarefa}",
            on_click=abrir_editor_subtarefa,
            args=("adicionar", indice_tarefa, identificador),
        )

        if editor_subtarefa_ativo(
            "adicionar",
            indice_tarefa,
            identificador,
        ):
            renderizar_formulario_subtarefa(
                indice_tarefa,
                subtarefas,
                "adicionar",
                identificador,
            )


def mostrar_plano_visual(
    plano,
    indice_tarefa: int | None = None,
    mostrar_titulo: bool = True,
) -> None:
    """Mostra o plano completo no Streamlit."""

    if mostrar_titulo:
        st.subheader("Resultado do planejamento")

    coluna1, coluna2, coluna3 = st.columns(3)
    coluna1.metric("Urgência", plano.urgencia)
    coluna2.metric("Pontuação", plano.pontuacao)
    coluna3.metric("Dias restantes", plano.dias_restantes)

    mostrar_detalhes_tarefa(plano.tarefa, indice_tarefa)

    with st.expander("Como o planejador tomou essa decisão?"):
        st.write(plano.justificativa)
        st.markdown(
            """
            - O sistema aplica regras condicionais de prazo, prioridade e duração.
            - O tipo da tarefa define o conjunto inicial de subtarefas.
            - As etapas são ordenadas em planejamento, execução e revisão.
            - O protótipo representa um agente baseado em regras, não uma IA generativa.
            """
        )

    st.markdown("#### Etapas recomendadas")
    renderizar_subtarefas_editaveis(plano, indice_tarefa)


@st.dialog(
    "Resultado do planejamento",
    icon=":material/visibility:",
    width="medium",
    on_dismiss=fechar_plano,
)
def mostrar_plano_em_janela(indice: int) -> None:
    """Mostra o planejamento da tarefa em uma janela separada."""

    tarefa = st.session_state.tarefas[indice]
    st.subheader(tarefa.titulo)
    if tarefa.descricao:
        st.caption(tarefa.descricao)
    if mensagem := st.session_state.pop("mensagem_plano", None):
        st.success(mensagem)

    mostrar_plano_visual(
        gerar_plano(tarefa),
        indice_tarefa=indice,
        mostrar_titulo=False,
    )

    if todas_subtarefas_concluidas(tarefa):
        if tarefa.concluida:
            st.success("Esta tarefa está concluída.")
        else:
            st.success("Todas as etapas foram concluídas.")
            st.write("Deseja marcar esta tarefa como concluída?")
            coluna_agora_nao, coluna_concluir = st.columns(2)

            if coluna_agora_nao.button(
                "Agora não",
                use_container_width=True,
            ):
                st.rerun(scope="app")

            if coluna_concluir.button(
                "Concluir tarefa",
                icon=":material/check:",
                type="primary",
                use_container_width=True,
            ):
                definir_tarefa_concluida(indice, True)
                st.session_state.mensagem_sucesso = (
                    f'Tarefa "{tarefa.titulo}" concluída.'
                )
                st.rerun(scope="app")


@st.dialog(
    "Como a pontuação funciona?",
    icon=":material/help:",
    width="medium",
)
def mostrar_ajuda_pontuacao() -> None:
    """Explica as regras usadas para calcular a pontuação."""

    st.write(
        "A pontuação não é uma nota. Ela serve para comparar as tarefas: "
        "quanto maior o resultado, mais atenção a tarefa deve receber."
    )
    st.markdown("### Fórmula")
    st.markdown(
        "**Pontuação = pontos da prioridade + pontos do prazo "
        "+ bônus de duração**"
    )

    st.markdown("#### Prioridade")
    st.table(
        [
            {"Prioridade": "Baixa", "Pontos": 10},
            {"Prioridade": "Média", "Pontos": 20},
            {"Prioridade": "Alta", "Pontos": 30},
        ]
    )

    st.markdown("#### Prazo")
    st.table(
        [
            {"Dias restantes": "Prazo vencido", "Pontos": 50},
            {"Dias restantes": "0 ou 1 dia", "Pontos": 40},
            {"Dias restantes": "2 ou 3 dias", "Pontos": 30},
            {"Dias restantes": "4 a 7 dias", "Pontos": 20},
            {"Dias restantes": "8 a 14 dias", "Pontos": 10},
            {"Dias restantes": "Mais de 14 dias", "Pontos": 5},
        ]
    )

    st.markdown("#### Duração")
    st.write(
        "Tarefas com duração estimada de **6 horas ou mais** recebem "
        "**10 pontos adicionais**, pois exigem mais planejamento."
    )

    st.markdown("### Exemplos")
    st.markdown(
        """
        **Tarefa alta, faltando 2 dias, duração de 8 horas**

        `30 da prioridade + 30 do prazo + 10 da duração = 70 pontos`

        **Tarefa média, faltando 10 dias, duração de 4 horas**

        `20 da prioridade + 10 do prazo + 0 da duração = 30 pontos`

        **Tarefa baixa, com prazo vencido, duração de 2 horas**

        `10 da prioridade + 50 do prazo + 0 da duração = 60 pontos`
        """
    )
    st.info(
        "Uma tarefa de prioridade baixa pode receber muitos pontos se estiver "
        "atrasada. Isso faz o prazo ter peso real na ordem de atenção."
    )


@st.dialog("Excluir tarefa?", icon=":material/delete:")
def confirmar_exclusao(indice: int) -> None:
    """Pede confirmação antes de excluir uma tarefa."""

    tarefa = st.session_state.tarefas[indice]
    st.write(f'Deseja continuar e excluir a tarefa "{tarefa.titulo}"?')
    coluna_cancelar, coluna_excluir = st.columns(2)

    if coluna_cancelar.button("Cancelar", use_container_width=True):
        st.rerun()

    if coluna_excluir.button(
        "Excluir",
        icon=":material/delete:",
        type="primary",
        use_container_width=True,
    ):
        st.session_state.tarefas.pop(indice)
        reiniciar_estado_dependente_tarefas()
        salvar_tarefas(st.session_state.tarefas)
        st.session_state.mensagem_sucesso = "Tarefa excluída com sucesso."
        st.rerun()


@st.dialog("Limpar tarefas terminadas?", icon=":material/delete_sweep:")
def confirmar_limpeza_tarefas_terminadas() -> None:
    """Pede confirmação antes de excluir todas as tarefas concluídas."""

    quantidade = sum(
        tarefa.concluida
        for tarefa in st.session_state.tarefas
    )
    if not quantidade:
        st.info("Não há tarefas terminadas para limpar.")
        return

    termo = "tarefa terminada" if quantidade == 1 else "tarefas terminadas"
    st.write(
        f"Deseja continuar e excluir {quantidade} {termo}? "
        "Essa ação não pode ser desfeita."
    )
    coluna_cancelar, coluna_limpar = st.columns(2)

    if coluna_cancelar.button("Cancelar", use_container_width=True):
        st.rerun()

    if coluna_limpar.button(
        "Limpar tarefas",
        icon=":material/delete_sweep:",
        type="primary",
        use_container_width=True,
    ):
        st.session_state.tarefas = remover_tarefas_terminadas(
            st.session_state.tarefas
        )
        reiniciar_estado_dependente_tarefas()
        salvar_tarefas(st.session_state.tarefas)
        st.session_state.mensagem_sucesso = (
            f"{quantidade} {termo} removida"
            f"{'' if quantidade == 1 else 's'} com sucesso."
        )
        st.rerun()


def mostrar_sidebar() -> None:
    """Monta a navegação explicativa da barra lateral."""

    with st.sidebar:
        st.subheader("Planejador Acadêmico")
        st.caption(
            "Protótipo de um agente planejador baseado em regras lógicas."
        )
        st.divider()
        st.markdown("#### Como funciona")
        st.markdown(
            """
            1. Informe a tarefa.
            2. Defina prazo e prioridade.
            3. Gere o plano.
            4. Acompanhe as etapas.
            """
        )
        st.divider()
        total = len(st.session_state.tarefas)
        concluidas = sum(tarefa.concluida for tarefa in st.session_state.tarefas)
        st.markdown("#### Progresso geral")
        st.caption(f"{concluidas} de {total} tarefa(s) concluída(s)")
        st.progress(concluidas / total if total else 0)
        st.info(
            "O sistema usa IA simbólica e regras condicionais. "
            "Ele não utiliza IA generativa."
        )
        st.caption("Lógica Aplicada · UCDB")


def mostrar_cabecalho() -> None:
    """Exibe o cabeçalho principal do projeto."""

    st.markdown(
        """
        <header class="app-header">
            <p class="app-kicker">Lógica Aplicada · Agente baseado em regras</p>
            <h1>Planejador Autônomo Acadêmico</h1>
            <p class="app-subtitle">
                Um protótipo acadêmico que transforma tarefas complexas em
                planos de ação organizados, explicáveis e fáceis de acompanhar.
            </p>
        </header>
        """,
        unsafe_allow_html=True,
    )


def mostrar_formulario() -> None:
    """Exibe o formulário de criação de tarefas."""

    st.subheader("Gerar novo plano")
    st.caption(
        "Descreva o objetivo e informe os critérios usados pelo planejador."
    )

    with st.form(
        "formulario_tarefa",
        clear_on_submit=True,
        border=True,
    ):
        titulo = st.text_input(
            "Tarefa principal",
            placeholder="Ex.: preparar o trabalho de Lógica Aplicada",
            help="Informe um objetivo claro e específico.",
        )
        descricao = st.text_area(
            "Descrição",
            placeholder="Contexto, conteúdo esperado ou observações importantes.",
            help="A descrição ajuda a identificar o tipo da tarefa.",
        )

        coluna_tipo, coluna_prioridade = st.columns(2)
        tipo = coluna_tipo.selectbox(
            "Tipo da tarefa",
            TIPOS_DISPONIVEIS,
            help="Escolha a categoria que mais se aproxima do objetivo.",
        )
        prioridade = coluna_prioridade.selectbox(
            "Prioridade",
            ["baixa", "media", "alta"],
            index=1,
            help="A prioridade influencia a pontuação final.",
        )

        coluna_prazo, coluna_duracao = st.columns(2)
        prazo = coluna_prazo.date_input(
            "Prazo",
            value=None,
            format="DD/MM/YYYY",
            help="Digite a data ou escolha pelo calendário.",
        )
        duracao = coluna_duracao.number_input(
            "Duração estimada em horas",
            min_value=0.5,
            step=0.5,
            help="Estime o total de horas necessárias para finalizar a tarefa.",
        )

        enviar = st.form_submit_button(
            "Gerar e salvar plano",
            icon=":material/account_tree:",
            type="primary",
            use_container_width=True,
        )

    if not enviar:
        return

    prazo_formatado = prazo.strftime("%d/%m/%Y") if prazo else ""
    erros = validar_formulario(prazo_formatado, prioridade, duracao)

    if not titulo.strip():
        erros.append("Informe o título da tarefa.")

    if erros:
        for erro in erros:
            st.error(erro)
        return

    tarefa = Tarefa(
        titulo=titulo.strip(),
        descricao=descricao.strip(),
        tipo=tipo,
        prazo=prazo_formatado,
        prioridade=normalizar_prioridade(prioridade),
        duracao_estimada=converter_numero_positivo(
            duracao,
            "Duração estimada",
        ),
    )
    st.session_state.tarefas.append(tarefa)
    salvar_tarefas(st.session_state.tarefas)
    st.session_state.indice_plano_recente = len(st.session_state.tarefas) - 1
    st.session_state.mensagem_sucesso = "Plano gerado e salvo com sucesso."
    st.rerun()


def mostrar_resumo_plano_recente() -> None:
    """Mostra um resumo do último plano criado."""

    indice = st.session_state.indice_plano_recente
    if indice is None or indice >= len(st.session_state.tarefas):
        return

    tarefa = st.session_state.tarefas[indice]
    plano = gerar_plano(tarefa)

    st.markdown("### Plano criado")
    with st.container(key="resumo_plano_recente"):
        st.markdown(f"#### {tarefa.titulo}")
        st.caption(f"Tipo identificado: {plano.tipo_identificado}")
        coluna1, coluna2, coluna3, coluna4 = st.columns(4)
        coluna1.metric("Urgência", plano.urgencia)
        coluna2.metric("Pontuação", plano.pontuacao)
        coluna3.metric("Dias restantes", plano.dias_restantes)
        total_etapas = (
            len(tarefa.subtarefas_personalizadas)
            if tarefa.subtarefas_personalizadas is not None
            else len(plano.subtarefas)
        )
        coluna4.metric("Etapas", total_etapas)
        mostrar_detalhes_tarefa(tarefa)

        st.button(
            "Abrir planejamento completo",
            icon=":material/visibility:",
            type="secondary",
            on_click=abrir_plano,
            args=(indice,),
        )


def mostrar_tarefas_cadastradas(
    criterio_ordenacao: str,
    criterio_filtro: str,
) -> None:
    """Mostra as tarefas salvas e suas ações."""

    proporcoes = [1.2, 2, 1.1, 1, 0.8]
    tarefas_visiveis = filtrar_tarefas(
        ordenar_tarefas(
            st.session_state.tarefas,
            criterio_ordenacao,
        ),
        criterio_filtro,
    )

    if not tarefas_visiveis:
        mensagens = {
            "Tarefas terminadas": "Nenhuma tarefa terminada.",
            "Tarefas atrasadas": "Nenhuma tarefa atrasada.",
        }
        st.info(
            mensagens.get(
                criterio_filtro,
                "Nenhuma tarefa cadastrada ainda.",
            )
        )
        return

    with st.container(key="lista_tarefas"):
        with st.container(key="cabecalho_tarefas"):
            colunas_cabecalho = st.columns(proporcoes)
            for coluna, titulo in zip(
                colunas_cabecalho,
                ["Tarefa", "Tipo", "Prazo", "Prioridade", "Duração"],
            ):
                coluna.caption(titulo)

        for indice, tarefa in tarefas_visiveis:
            valores = [
                tarefa.titulo,
                tarefa.tipo,
                tarefa.prazo,
                tarefa.prioridade,
                f"{tarefa.duracao_estimada:g}",
            ]
            estado = "concluida" if tarefa.concluida else "pendente"

            with st.container(key=f"linha_tarefa_{estado}_{indice}"):
                colunas = st.columns(
                    proporcoes,
                    vertical_alignment="center",
                )

                for coluna, valor in zip(colunas, valores):
                    coluna.write(valor)

                if st.button(
                    "",
                    icon=":material/close:",
                    help=f"Excluir {tarefa.titulo}",
                    key=f"excluir_tarefa_{indice}",
                ):
                    confirmar_exclusao(indice)

                st.button(
                    f"Abrir planejamento de {tarefa.titulo}",
                    key=f"abrir_linha_tarefa_{indice}",
                    on_click=abrir_plano,
                    args=(indice,),
                )


def mostrar_aba_tarefas() -> None:
    """Exibe a listagem e os filtros das tarefas salvas."""

    with st.container(key="cabecalho_secao_tarefas"):
        st.subheader("Tarefas cadastradas")
        st.caption(
            "Clique em uma linha para abrir o plano ou use os controles para filtrar e ordenar."
        )

        with st.container(key="controles_tarefas"):
            (
                coluna_filtro,
                coluna_ordenacao,
                coluna_limpeza,
            ) = st.columns(3, gap="small")

            with coluna_filtro.popover(
                "",
                icon=":material/filter_alt:",
                help="Filtrar tarefas",
            ):
                criterio_filtro = st.radio(
                    "Mostrar",
                    OPCOES_FILTRO_TAREFAS,
                    key="criterio_filtro_tarefas",
                )

            with coluna_ordenacao.popover(
                "",
                icon=":material/sort:",
                help="Ordenar tarefas",
            ):
                criterio_ordenacao = st.radio(
                    "Ordenar por",
                    OPCOES_ORDENACAO,
                    key="criterio_ordenacao_tarefas",
                )

            quantidade_terminadas = sum(
                tarefa.concluida
                for tarefa in st.session_state.tarefas
            )
            if coluna_limpeza.button(
                "",
                icon=":material/delete_sweep:",
                help=(
                    "Limpar tarefas terminadas"
                    if quantidade_terminadas
                    else "Nenhuma tarefa terminada para limpar"
                ),
                key="limpar_tarefas_terminadas",
                disabled=not quantidade_terminadas,
            ):
                confirmar_limpeza_tarefas_terminadas()

    if st.session_state.tarefas:
        mostrar_tarefas_cadastradas(
            criterio_ordenacao,
            criterio_filtro,
        )
    else:
        st.info("Nenhuma tarefa cadastrada ainda.")


def mostrar_sobre_projeto() -> None:
    """Exibe o contexto acadêmico e técnico do projeto."""

    st.subheader("Sobre o projeto")
    st.write(
        "O Planejador Autônomo Acadêmico demonstra como um sistema baseado "
        "em regras pode receber um objetivo amplo, avaliar critérios e "
        "produzir uma sequência organizada de ações."
    )

    with st.expander(
        "Como o planejador toma decisões?",
        expanded=True,
    ):
        st.markdown(
            """
            O sistema considera **prazo**, **prioridade** e **duração estimada**.
            Depois identifica o tipo da tarefa, seleciona um conjunto de etapas
            e organiza a execução em uma ordem lógica.

            A pontuação funciona como um indicador de atenção: tarefas mais
            urgentes, prioritárias ou longas recebem mais pontos.
            """
        )

    with st.expander("Relação com Lógica Aplicada"):
        st.markdown(
            """
            - **Estruturas condicionais:** regras com `if`, `elif` e `else`.
            - **Decomposição de problemas:** uma tarefa ampla vira etapas menores.
            - **Funções:** cada parte do raciocínio possui uma responsabilidade.
            - **Execução sequencial:** as etapas seguem uma ordem recomendada.
            - **Regras de decisão:** critérios objetivos definem urgência e pontos.
            """
        )

    st.info(
        "Este projeto representa IA simbólica: o comportamento é explicado "
        "por regras definidas no código e não por geração de texto."
    )


def mostrar_rodape() -> None:
    """Exibe o rodapé acadêmico."""

    st.markdown(
        """
        <footer class="app-footer">
            Projeto acadêmico desenvolvido para a disciplina de
            Lógica Aplicada — UCDB.
        </footer>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    """Executa a aplicação Streamlit."""

    st.set_page_config(
        page_title="Planejador Autônomo Acadêmico",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="auto",
    )
    aplicar_estilos()
    iniciar_estado()
    mostrar_sidebar()
    mostrar_cabecalho()

    with st.container(key="botao_ajuda_pontuacao"):
        if st.button(
            "",
            icon=":material/help:",
            help="Entenda como a pontuação é calculada",
            key="abrir_ajuda_pontuacao",
        ):
            mostrar_ajuda_pontuacao()

    if mensagem := st.session_state.pop("mensagem_sucesso", None):
        st.success(mensagem)

    aba_plano, aba_tarefas, aba_sobre = st.tabs(
        ABAS_PRINCIPAIS,
        default="Gerar plano",
        key="aba_principal",
        on_change="rerun",
    )

    with aba_plano:
        mostrar_formulario()
        mostrar_resumo_plano_recente()

    with aba_tarefas:
        mostrar_aba_tarefas()

    with aba_sobre:
        mostrar_sobre_projeto()

    indice_plano_aberto = st.session_state.indice_plano_aberto
    if (
        indice_plano_aberto is not None
        and indice_plano_aberto < len(st.session_state.tarefas)
    ):
        mostrar_plano_em_janela(indice_plano_aberto)

    mostrar_rodape()


if __name__ == "__main__":
    main()

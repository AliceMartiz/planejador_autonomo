"""Interface visual do Planejador Autônomo Acadêmico."""

import streamlit as st

from models import Tarefa
from planner import gerar_plano
from storage import carregar_tarefas, salvar_tarefas
from validators import (
    converter_data,
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

OPCOES_ORDENACAO = [
    "Padrão",
    "Prazo mais próximo",
    "Maior pontuação",
    "Prioridade mais alta",
    "Maior duração",
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

        .st-key-cabecalho_secao_tarefas {
            position: relative;
            padding-right: 3.25rem;
        }

        .st-key-filtro_tarefas {
            position: absolute;
            top: 0.15rem;
            right: 0;
            z-index: 4;
            width: 2.75rem;
        }

        .st-key-filtro_tarefas button {
            width: 2.75rem;
            height: 2.75rem;
            padding: 0;
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
            padding: 0.55rem 0.65rem;
            margin: 0.15rem 0;
            border-radius: 7px;
            transition: background-color 160ms ease, opacity 160ms ease;
        }

        [class*="st-key-linha_subtarefa_"]:hover {
            background-color: rgba(47, 107, 95, 0.075);
        }

        [class*="st-key-linha_subtarefa_concluida_"] {
            background-color: rgba(100, 116, 139, 0.07);
        }

        [class*="st-key-linha_subtarefa_concluida_"] p,
        [class*="st-key-linha_subtarefa_concluida_"] code,
        [class*="st-key-linha_subtarefa_concluida_"] span {
            text-decoration: line-through;
            text-decoration-thickness: 1px;
            opacity: 0.52;
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


def validar_formulario(prazo, prioridade, duracao):
    """Valida os campos antes de gerar a tarefa."""

    erros = []

    if not validar_data(prazo):
        erros.append("Escolha uma data de prazo válida.")
    if not validar_prioridade(prioridade):
        erros.append("Escolha uma prioridade válida.")
    if not validar_numero_positivo(duracao):
        erros.append("A duração estimada deve ser maior que zero.")

    return erros


def ordenar_tarefas(tarefas, criterio):
    """Ordena as tarefas sem perder seus índices originais."""

    tarefas_com_indice = list(enumerate(tarefas))

    if criterio == "Prazo mais próximo":
        return sorted(
            tarefas_com_indice,
            key=lambda item: converter_data(item[1].prazo),
        )

    if criterio == "Maior pontuação":
        return sorted(
            tarefas_com_indice,
            key=lambda item: (
                -gerar_plano(item[1]).pontuacao,
                converter_data(item[1].prazo),
            ),
        )

    if criterio == "Prioridade mais alta":
        pesos = {"baixa": 1, "media": 2, "alta": 3}
        return sorted(
            tarefas_com_indice,
            key=lambda item: (
                -pesos[item[1].prioridade],
                converter_data(item[1].prazo),
            ),
        )

    if criterio == "Maior duração":
        return sorted(
            tarefas_com_indice,
            key=lambda item: (
                -item[1].duracao_estimada,
                converter_data(item[1].prazo),
            ),
        )

    return tarefas_com_indice


def alternar_subtarefa(indice_tarefa: int, nome_subtarefa: str) -> None:
    """Alterna uma subtarefa e salva o progresso."""

    tarefa = st.session_state.tarefas[indice_tarefa]

    if nome_subtarefa in tarefa.subtarefas_concluidas:
        tarefa.subtarefas_concluidas.remove(nome_subtarefa)
        tarefa.concluida = False
    else:
        tarefa.subtarefas_concluidas.append(nome_subtarefa)

    salvar_tarefas(st.session_state.tarefas)


def todas_subtarefas_concluidas(tarefa: Tarefa) -> bool:
    """Verifica se todas as subtarefas geradas já foram concluídas."""

    nomes_subtarefas = {
        subtarefa.nome
        for subtarefa in gerar_plano(tarefa).subtarefas
    }
    return bool(nomes_subtarefas) and nomes_subtarefas.issubset(
        set(tarefa.subtarefas_concluidas)
    )


def definir_tarefa_concluida(indice: int, concluida: bool) -> None:
    """Atualiza e salva o estado de conclusão de uma tarefa."""

    st.session_state.tarefas[indice].concluida = concluida
    salvar_tarefas(st.session_state.tarefas)


def mostrar_detalhes_tarefa(tarefa: Tarefa) -> None:
    """Mostra os principais dados informados pelo usuário."""

    coluna1, coluna2, coluna3 = st.columns(3)
    coluna1.markdown(f"**Prioridade**  \n{tarefa.prioridade.title()}")
    coluna2.markdown(f"**Prazo**  \n{tarefa.prazo}")
    coluna3.markdown(
        f"**Duração estimada**  \n{tarefa.duracao_estimada:g} hora(s)"
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

    mostrar_detalhes_tarefa(plano.tarefa)

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

    with st.container(key="cabecalho_subtarefas"):
        cabecalho = st.columns([0.6, 2.2, 1.15, 3])
        for coluna, titulo in zip(
            cabecalho,
            ["Ordem", "Subtarefa", "Categoria", "Motivo"],
        ):
            coluna.caption(titulo)

    tarefa = plano.tarefa
    concluidas = set(tarefa.subtarefas_concluidas)

    for subtarefa in plano.subtarefas:
        concluida = subtarefa.nome in concluidas
        estado = "concluida" if concluida else "pendente"

        with st.container(
            key=(
                f"linha_subtarefa_{estado}_{indice_tarefa}_"
                f"{subtarefa.ordem_logica}"
            )
        ):
            colunas = st.columns(
                [0.6, 2.2, 1.15, 3],
                vertical_alignment="center",
            )
            colunas[0].write(subtarefa.ordem_logica)
            colunas[1].write(subtarefa.nome)
            colunas[2].write(subtarefa.categoria)
            colunas[3].write(subtarefa.motivo)

            st.button(
                f"Alternar {subtarefa.nome}",
                key=(
                    f"alternar_subtarefa_{indice_tarefa}_"
                    f"{subtarefa.ordem_logica}_{estado}"
                ),
                on_click=alternar_subtarefa,
                args=(indice_tarefa, subtarefa.nome),
            )


@st.dialog(
    "Resultado do planejamento",
    icon=":material/visibility:",
    width="medium",
)
def mostrar_plano_em_janela(indice: int) -> None:
    """Mostra o planejamento da tarefa em uma janela separada."""

    tarefa = st.session_state.tarefas[indice]
    st.subheader(tarefa.titulo)
    if tarefa.descricao:
        st.caption(tarefa.descricao)

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
        st.session_state.indice_plano_recente = None
        salvar_tarefas(st.session_state.tarefas)
        st.session_state.mensagem_sucesso = "Tarefa excluída com sucesso."
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
        coluna4.metric("Etapas", len(plano.subtarefas))
        mostrar_detalhes_tarefa(tarefa)

        if st.button(
            "Abrir planejamento completo",
            icon=":material/visibility:",
            type="secondary",
        ):
            mostrar_plano_em_janela(indice)


def mostrar_tarefas_cadastradas(criterio_ordenacao: str) -> None:
    """Mostra as tarefas salvas e suas ações."""

    proporcoes = [1.2, 2, 1.1, 1, 0.8]

    with st.container(key="lista_tarefas"):
        with st.container(key="cabecalho_tarefas"):
            colunas_cabecalho = st.columns(proporcoes)
            for coluna, titulo in zip(
                colunas_cabecalho,
                ["Tarefa", "Tipo", "Prazo", "Prioridade", "Duração"],
            ):
                coluna.caption(titulo)

        for indice, tarefa in ordenar_tarefas(
            st.session_state.tarefas,
            criterio_ordenacao,
        ):
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

                if st.button(
                    f"Abrir planejamento de {tarefa.titulo}",
                    key=f"abrir_linha_tarefa_{indice}",
                ):
                    mostrar_plano_em_janela(indice)


def mostrar_aba_tarefas() -> None:
    """Exibe a listagem e os filtros das tarefas salvas."""

    with st.container(key="cabecalho_secao_tarefas"):
        st.subheader("Tarefas cadastradas")
        st.caption(
            "Clique em uma linha para abrir o plano ou use o filtro para ordenar."
        )

        with st.container(key="filtro_tarefas"):
            with st.popover(
                "",
                icon=":material/filter_list:",
                help="Ordenar tarefas",
            ):
                criterio_ordenacao = st.radio(
                    "Ordenar por",
                    OPCOES_ORDENACAO,
                    key="criterio_ordenacao_tarefas",
                )

    if st.session_state.tarefas:
        mostrar_tarefas_cadastradas(criterio_ordenacao)
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

    mostrar_rodape()


if __name__ == "__main__":
    main()

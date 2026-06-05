"""Interface visual simples com Streamlit."""

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


def aplicar_estilos() -> None:
    """Aplica estilos pontuais da interface."""

    st.markdown(
        """
        <style>
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
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.22);
        }

        @media (max-width: 640px) {
            .st-key-botao_ajuda_pontuacao {
                left: 0.75rem;
                bottom: 0.75rem;
            }

            .st-key-cabecalho_tarefas {
                display: none;
            }

            .st-key-lista_tarefas {
                padding: 0.35rem;
            }

            [class*="st-key-linha_tarefa_"] {
                padding: 0.85rem 0.8rem;
                border-radius: 0.4rem;
            }

            [class*="st-key-linha_tarefa_"] [data-testid="stHorizontalBlock"] {
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: 0.75rem 1rem;
                width: 100%;
            }

            [class*="st-key-linha_tarefa_"] [data-testid="stColumn"] {
                width: auto !important;
                min-width: 0 !important;
            }

            [class*="st-key-linha_tarefa_"] [data-testid="stColumn"]::before {
                display: block;
                margin-bottom: 0.18rem;
                color: rgba(128, 128, 128, 0.95);
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
                font-weight: 600;
            }

            .st-key-cabecalho_subtarefas {
                display: none;
            }

            [class*="st-key-linha_subtarefa_"] {
                padding: 0.75rem;
                margin: 0.3rem 0;
                background-color: rgba(128, 128, 128, 0.045);
            }

            [class*="st-key-linha_subtarefa_"] [data-testid="stHorizontalBlock"] {
                display: grid;
                grid-template-columns: 2rem minmax(0, 1fr);
                gap: 0.25rem 0.65rem;
                width: 100%;
            }

            [class*="st-key-linha_subtarefa_"] [data-testid="stColumn"] {
                width: auto !important;
                min-width: 0 !important;
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
                font-weight: 600;
            }

            [class*="st-key-linha_subtarefa_"] [data-testid="stColumn"]:nth-child(3) {
                grid-column: 2;
                grid-row: 2;
            }

            [class*="st-key-linha_subtarefa_"] [data-testid="stColumn"]:nth-child(3) p {
                color: rgba(128, 128, 128, 0.95);
                font-size: 0.78rem;
            }

            [class*="st-key-linha_subtarefa_"] [data-testid="stColumn"]:nth-child(4) {
                grid-column: 1 / -1;
                grid-row: 3;
                padding-top: 0.35rem;
            }

            [class*="st-key-linha_subtarefa_"] [data-testid="stColumn"]:nth-child(4) p {
                color: rgba(128, 128, 128, 0.95);
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

        [class*="st-key-linha_tarefa_"],
        [class*="st-key-linha_subtarefa_"] {
            position: relative;
            cursor: pointer;
        }

        .st-key-lista_tarefas {
            border: 1px solid rgba(128, 128, 128, 0.35);
            border-radius: 0.5rem;
            padding-bottom: 0.35rem;
            overflow: hidden;
        }

        .st-key-cabecalho_tarefas {
            padding: 0.7rem 0.8rem 0.35rem;
            background-color: rgba(128, 128, 128, 0.035);
        }

        .st-key-cabecalho_subtarefas {
            padding: 0.65rem 0.65rem 0.35rem;
            margin-bottom: 0.25rem;
            border-radius: 0.45rem;
            background-color: rgba(128, 128, 128, 0.09);
        }

        .st-key-cabecalho_secao_tarefas {
            position: relative;
            padding-right: 3.25rem;
        }

        .st-key-filtro_tarefas {
            position: absolute;
            top: 0.2rem;
            right: 0;
            z-index: 4;
            width: 2.75rem;
        }

        .st-key-filtro_tarefas button {
            width: 2.75rem;
            height: 2.75rem;
            padding: 0;
        }

        [class*="st-key-linha_tarefa_"] {
            padding: 0.45rem 0.8rem 0.7rem;
            transition: background-color 160ms ease;
        }

        [class*="st-key-linha_tarefa_"]:hover {
            background-color: rgba(128, 128, 128, 0.1);
        }

        [class*="st-key-linha_tarefa_concluida_"] {
            background-color: rgba(34, 197, 94, 0.14);
        }

        [class*="st-key-linha_tarefa_concluida_"]:hover {
            background-color: rgba(34, 197, 94, 0.2);
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
            transform: translateY(-50%);
            z-index: 3;
        }

        [class*="st-key-linha_subtarefa_"] {
            padding: 0.55rem 0.65rem;
            margin: 0.15rem 0;
            border-radius: 0.45rem;
            transition:
                background-color 160ms ease,
                opacity 160ms ease;
        }

        [class*="st-key-linha_subtarefa_"]:hover {
            background-color: rgba(128, 128, 128, 0.09);
        }

        [class*="st-key-linha_subtarefa_concluida_"] p,
        [class*="st-key-linha_subtarefa_concluida_"] code,
        [class*="st-key-linha_subtarefa_concluida_"] span {
            text-decoration: line-through;
            text-decoration-thickness: 1px;
            opacity: 0.52;
        }

        [class*="st-key-linha_subtarefa_concluida_"] {
            background-color: rgba(128, 128, 128, 0.055);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def iniciar_estado() -> None:
    """Cria a lista de tarefas no estado da página."""

    if "tarefas" not in st.session_state:
        st.session_state.tarefas = carregar_tarefas()


def validar_formulario(prazo, prioridade, duracao):
    """Valida os campos antes de gerar a tarefa."""

    erros = []

    if not validar_data(prazo):
        erros.append("O prazo deve estar no formato dd/mm/aaaa.")
    if not validar_prioridade(prioridade):
        erros.append("A prioridade deve ser baixa, media ou alta.")
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
    """Alterna o estado concluído de uma subtarefa e salva o progresso."""

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


def mostrar_plano_visual(
    plano,
    indice_tarefa: int | None = None,
    mostrar_titulo: bool = True,
) -> None:
    """Mostra o plano em formato visual no Streamlit."""

    if mostrar_titulo:
        st.subheader("Resultado do planejamento")

    coluna1, coluna2, coluna3 = st.columns(3)
    coluna1.metric("Urgência", plano.urgencia)
    coluna2.metric("Pontuação", plano.pontuacao)
    coluna3.metric("Dias restantes", plano.dias_restantes)

    st.write("**Tipo identificado:**", plano.tipo_identificado)
    st.write("**Justificativa:**", plano.justificativa)

    st.write("**Ordem recomendada das subtarefas:**")

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
        **Exemplo 1: tarefa alta, faltando 2 dias, duração de 8 horas**

        `30 da prioridade + 30 do prazo + 10 da duração = 70 pontos`

        **Exemplo 2: tarefa média, faltando 10 dias, duração de 4 horas**

        `20 da prioridade + 10 do prazo + 0 da duração = 30 pontos`

        **Exemplo 3: tarefa baixa, mas com prazo vencido, duração de 2 horas**

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
        salvar_tarefas(st.session_state.tarefas)
        st.session_state.mensagem_sucesso = "Tarefa excluída com sucesso."
        st.rerun()


def mostrar_tarefas_cadastradas(criterio_ordenacao: str) -> None:
    """Mostra as tarefas com uma ação de exclusão em cada linha."""

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

            with st.container(
                key=f"linha_tarefa_{estado}_{indice}",
            ):
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


def main() -> None:
    """Executa a aplicação Streamlit."""

    st.set_page_config(page_title="Planejador Autônomo Acadêmico")
    aplicar_estilos()
    iniciar_estado()
    st.title("Planejador Autônomo Acadêmico")

    with st.container(key="botao_ajuda_pontuacao"):
        if st.button(
            "",
            icon=":material/help:",
            help="Entenda como a pontuação é calculada",
            key="abrir_ajuda_pontuacao",
        ):
            mostrar_ajuda_pontuacao()

    with st.form("formulario_tarefa"):
        titulo = st.text_input("Tarefa principal", placeholder="Ex.: fazer trabalho acadêmico")
        descricao = st.text_area("Descrição", placeholder="Explique rapidamente o que precisa ser feito.")
        tipo = st.selectbox("Tipo da tarefa", TIPOS_DISPONIVEIS)
        prazo = st.date_input(
            "Prazo",
            value=None,
            format="DD/MM/YYYY",
            help="Digite a data ou escolha pelo calendário.",
        )
        prioridade = st.selectbox("Prioridade", ["baixa", "media", "alta"], index=1)
        duracao = st.number_input("Duração estimada em horas", min_value=0.5, step=0.5)
        enviar = st.form_submit_button("Gerar plano")

    if enviar:
        prazo_formatado = prazo.strftime("%d/%m/%Y") if prazo else ""
        erros = validar_formulario(prazo_formatado, prioridade, duracao)

        if not titulo.strip():
            erros.append("Informe o título da tarefa.")

        if erros:
            for erro in erros:
                st.error(erro)
        else:
            tarefa = Tarefa(
                titulo=titulo.strip(),
                descricao=descricao.strip(),
                tipo=tipo,
                prazo=prazo_formatado,
                prioridade=normalizar_prioridade(prioridade),
                duracao_estimada=converter_numero_positivo(duracao, "Duração estimada"),
            )
            st.session_state.tarefas.append(tarefa)
            salvar_tarefas(st.session_state.tarefas)
            st.session_state.mensagem_sucesso = "Tarefa criada e salva com sucesso."

    st.divider()
    with st.container(key="cabecalho_secao_tarefas"):
        st.subheader("Tarefas cadastradas")

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

    if mensagem := st.session_state.pop("mensagem_sucesso", None):
        st.success(mensagem)

    if st.session_state.tarefas:
        mostrar_tarefas_cadastradas(criterio_ordenacao)
    else:
        st.info("Nenhuma tarefa cadastrada ainda.")


if __name__ == "__main__":
    main()

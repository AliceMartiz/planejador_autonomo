"""Componentes visuais usados na lista editável de subtarefas."""

import streamlit as st


HTML_REORDENACAO = '<span class="componente-reordenacao"></span>'

CSS_REORDENACAO = """
.componente-reordenacao {
    display: none;
}

[class*="st-key-linha_subtarefa_"] {
    padding-right: 3rem !important;
}

[class*="st-key-alternar_subtarefa_"] {
    right: 2.65rem !important;
    width: calc(100% - 2.65rem) !important;
}

[class*="st-key-arrastar_subtarefa_"] {
    position: absolute;
    top: 50%;
    right: 0.55rem;
    z-index: 7;
    transform: translateY(-50%);
}

[class*="st-key-arrastar_subtarefa_"] button {
    display: inline-flex;
    width: 1.75rem;
    height: 2rem;
    min-height: 2rem;
    align-items: center;
    justify-content: center;
    padding: 0;
    border: 0;
    border-radius: 5px;
    background: transparent;
    color: var(--st-text-color);
    cursor: grab;
    opacity: 0.38;
    transition:
        color 150ms ease,
        opacity 150ms ease,
        background-color 150ms ease;
    touch-action: none;
}

[class*="st-key-arrastar_subtarefa_"] button:hover,
[class*="st-key-arrastar_subtarefa_"] button:focus-visible {
    background-color: color-mix(
        in srgb,
        var(--st-primary-color) 9%,
        transparent
    );
    color: var(--st-primary-color);
    opacity: 1;
    outline: none;
}

[class*="st-key-arrastar_subtarefa_"] button:active {
    cursor: grabbing;
}

.subtarefa-arrastando {
    opacity: 0.32;
}

.subtarefa-drop-antes::before,
.subtarefa-drop-depois::after {
    position: absolute;
    right: 0.45rem;
    left: 0.45rem;
    z-index: 8;
    height: 2px;
    border-radius: 999px;
    background-color: var(--st-primary-color);
    content: "";
}

.subtarefa-drop-antes::before {
    top: -0.3rem;
}

.subtarefa-drop-depois::after {
    bottom: -0.3rem;
}

.subtarefa-drag-ghost {
    position: fixed;
    z-index: 100000;
    margin: 0;
    pointer-events: none;
    opacity: 0.92;
    transform: rotate(0.4deg);
    box-shadow: 0 8px 22px rgba(30, 47, 61, 0.16);
}

@media (hover: none) {
    [class*="st-key-arrastar_subtarefa_"] button {
        opacity: 0.58;
    }
}
"""

JS_REORDENACAO = """
export default function(component) {
    const { data, parentElement, setTriggerValue } = component;
    parentElement.style.display = "none";

    const prefixo = data?.prefixo;
    const prefixoAlca = data?.prefixo_alca;
    const ordemInformada = Array.isArray(data?.ordem) ? data.ordem : [];
    if (!prefixo || !prefixoAlca || ordemInformada.length < 2) {
        return;
    }

    // Cada rerun substitui a instância anterior e remove seus eventos globais.
    const registros = (
        window.__planejadorArrasteSubtarefas
        ||= Object.create(null)
    );
    registros[prefixo]?.();

    const seletor = `[class*="${prefixo}"]`;
    const seletorAlca = `[class*="${prefixoAlca}"]`;
    let blocos = [];
    let origem = null;
    let destino = null;
    let botaoAtivo = null;
    let inserirAntes = true;
    let fantasma = null;
    let arrastando = false;
    let inicioX = 0;
    let inicioY = 0;
    let deslocamentoX = 0;
    let deslocamentoY = 0;
    let ponteiroAtivo = null;

    const obterId = (bloco) => {
        const classe = Array.from(bloco.classList).find(
            (item) => item.startsWith(prefixo)
        );
        return classe ? classe.slice(prefixo.length) : "";
    };

    const obterBlocos = () => Array.from(
        document.querySelectorAll(seletor)
    ).filter(
        (elemento) => Array.from(elemento.classList).some(
            (classe) => classe.startsWith(prefixo)
        )
    );

    const obterIdAlca = (botao) => {
        const envoltorio = botao?.closest(seletorAlca);
        const classe = envoltorio
            ? Array.from(envoltorio.classList).find(
                (item) => item.startsWith(prefixoAlca)
            )
            : "";
        return classe ? classe.slice(prefixoAlca.length) : "";
    };

    const obterBlocoPorId = (identificador) => obterBlocos().find(
        (bloco) => obterId(bloco) === identificador
    );

    const marcarAlcas = () => {
        document.querySelectorAll(`${seletorAlca} button`).forEach(
            (botao) => {
                if (obterIdAlca(botao)) {
                    botao.classList.add("subtarefa-drag-handle");
                    botao.draggable = false;
                }
            }
        );
    };

    const limparIndicadores = () => {
        blocos.forEach((bloco) => {
            bloco.classList.remove(
                "subtarefa-drop-antes",
                "subtarefa-drop-depois"
            );
        });
    };

    const finalizarVisual = () => {
        limparIndicadores();
        origem?.classList.remove("subtarefa-arrastando");
        fantasma?.remove();
        if (
            botaoAtivo
            && ponteiroAtivo !== null
            && botaoAtivo.hasPointerCapture?.(ponteiroAtivo)
        ) {
            botaoAtivo.releasePointerCapture(ponteiroAtivo);
        }
        origem = null;
        destino = null;
        botaoAtivo = null;
        fantasma = null;
        arrastando = false;
        ponteiroAtivo = null;
    };

    const emitirNovaOrdem = () => {
        const idOrigem = origem ? obterId(origem) : "";
        const idDestino = destino ? obterId(destino) : "";
        if (!idOrigem || !idDestino) {
            return;
        }

        const ordemAtual = obterBlocos()
            .map(obterId)
            .filter(Boolean);
        const novaOrdem = ordemAtual.filter((id) => id !== idOrigem);
        const indiceDestino = novaOrdem.indexOf(idDestino);
        if (indiceDestino < 0) {
            return;
        }
        const indiceInsercao = inserirAntes
            ? indiceDestino
            : indiceDestino + 1;
        novaOrdem.splice(indiceInsercao, 0, idOrigem);

        if (novaOrdem.join("|") !== ordemAtual.join("|")) {
            setTriggerValue("nova_ordem", novaOrdem);
        }
    };

    const iniciarFantasma = (evento) => {
        const retangulo = origem.getBoundingClientRect();
        fantasma = origem.cloneNode(true);
        fantasma.querySelectorAll("button").forEach(
            (botao) => botao.remove()
        );
        fantasma.classList.add("subtarefa-drag-ghost");
        fantasma.style.width = `${retangulo.width}px`;
        fantasma.style.height = `${retangulo.height}px`;
        const camadaSuperior = (
            origem.closest('[data-testid="stDialog"]')
            || origem.closest("dialog")
            || document.querySelector("dialog[open]")
            || origem.closest('[role="dialog"]')
            || document.body
        );
        camadaSuperior.appendChild(fantasma);
        deslocamentoX = evento.clientX - retangulo.left;
        deslocamentoY = evento.clientY - retangulo.top;
        origem.classList.add("subtarefa-arrastando");
    };

    const moverFantasma = (evento) => {
        fantasma.style.left = `${evento.clientX - deslocamentoX}px`;
        fantasma.style.top = `${evento.clientY - deslocamentoY}px`;
    };

    const aoMover = (evento) => {
        if (!origem || evento.pointerId !== ponteiroAtivo) {
            return;
        }

        const distancia = Math.hypot(
            evento.clientX - inicioX,
            evento.clientY - inicioY
        );
        if (!arrastando && distancia < 5) {
            return;
        }

        evento.preventDefault();
        if (!arrastando) {
            arrastando = true;
            iniciarFantasma(evento);
        }
        moverFantasma(evento);

        const elemento = document.elementFromPoint(
            evento.clientX,
            evento.clientY
        );
        const novoDestino = elemento?.closest(seletor);
        limparIndicadores();
        destino = (
            novoDestino
            && novoDestino !== origem
            && blocos.includes(novoDestino)
        ) ? novoDestino : null;

        if (!destino) {
            return;
        }

        const retangulo = destino.getBoundingClientRect();
        inserirAntes = evento.clientY < retangulo.top + retangulo.height / 2;
        destino.classList.add(
            inserirAntes
                ? "subtarefa-drop-antes"
                : "subtarefa-drop-depois"
        );
    };

    const aoSoltar = (evento) => {
        if (!origem || evento.pointerId !== ponteiroAtivo) {
            return;
        }

        if (arrastando) {
            emitirNovaOrdem();
        }
        finalizarVisual();
    };

    // Eventos delegados continuam válidos quando o Streamlit recria as linhas.
    const aoPressionar = (evento) => {
        const botao = evento.target?.closest?.("button");
        const identificador = obterIdAlca(botao);
        if (!identificador) {
            return;
        }

        const bloco = obterBlocoPorId(identificador);
        if (!bloco) {
            return;
        }

        evento.stopPropagation();
        evento.preventDefault();
        blocos = obterBlocos();
        origem = bloco;
        destino = null;
        botaoAtivo = botao;
        inicioX = evento.clientX;
        inicioY = evento.clientY;
        ponteiroAtivo = evento.pointerId;
        botao.setPointerCapture?.(evento.pointerId);
    };

    const impedirClique = (evento) => {
        const botao = evento.target?.closest?.("button");
        if (obterIdAlca(botao)) {
            evento.preventDefault();
            evento.stopPropagation();
            evento.stopImmediatePropagation();
        }
    };

    marcarAlcas();
    const raizObservada = (
        parentElement.closest('[data-testid="stDialog"]')
        || parentElement.parentElement
        || document.body
    );
    const observador = new MutationObserver(marcarAlcas);
    observador.observe(raizObservada, {
        childList: true,
        subtree: true,
    });

    document.addEventListener("pointerdown", aoPressionar, true);
    document.addEventListener("pointermove", aoMover, { passive: false });
    document.addEventListener("pointerup", aoSoltar);
    document.addEventListener("pointercancel", aoSoltar);
    document.addEventListener("click", impedirClique, true);

    let finalizado = false;
    const limparComponente = () => {
        if (finalizado) {
            return;
        }
        finalizado = true;
        observador.disconnect();
        document.removeEventListener("pointerdown", aoPressionar, true);
        document.removeEventListener("pointermove", aoMover);
        document.removeEventListener("pointerup", aoSoltar);
        document.removeEventListener("pointercancel", aoSoltar);
        document.removeEventListener("click", impedirClique, true);
        finalizarVisual();
        document.querySelectorAll(`${seletorAlca} button`).forEach(
            (botao) => botao.classList.remove("subtarefa-drag-handle")
        );
        if (registros[prefixo] === limparComponente) {
            delete registros[prefixo];
        }
    };

    registros[prefixo] = limparComponente;
    return limparComponente;
}
"""


_componente_reordenacao = st.components.v2.component(
    "reordenar_subtarefas",
    html=HTML_REORDENACAO,
    css=CSS_REORDENACAO,
    js=JS_REORDENACAO,
    isolate_styles=False,
)


def capturar_nova_ordem(
    indice_tarefa: int,
    identificadores: list[str],
) -> list[str] | None:
    """Ativa as alças de arraste e retorna a nova ordem escolhida."""

    resultado = _componente_reordenacao(
        key=f"reordenacao_subtarefas_{indice_tarefa}",
        data={
            "prefixo": f"st-key-bloco_subtarefa_{indice_tarefa}_",
            "prefixo_alca": f"st-key-arrastar_subtarefa_{indice_tarefa}_",
            "ordem": identificadores,
        },
        on_nova_ordem_change=lambda: None,
        width="stretch",
        height=0,
    )
    nova_ordem = getattr(resultado, "nova_ordem", None)
    return list(nova_ordem) if nova_ordem else None

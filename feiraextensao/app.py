"""
Aplicação interativa em Streamlit para a Feira de Extensão — SCC0282 (Recuperação de Informação).
Tema: Part-of-Speech Tagging & Recuperação de Informação.
Como o site funciona: veja README.md nesta pasta.
"""

from __future__ import annotations

import html

import streamlit as st

from nlp_engine import POS_INFO, TokenAnalisado, analisar_frase, buscar_documentos


# ============================================================================
# CONFIGURAÇÃO DA PÁGINA E ESTILO
# ============================================================================

st.set_page_config(
    page_title="Como a IA Entende o Português? | USP",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .block-container { padding-top: 1.4rem; padding-bottom: 2.5rem; max-width: 1100px; }

    .hero-banner {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 55%, #312E81 100%);
        padding: 1.5rem 2rem;
        border-radius: 18px;
        margin-bottom: 1.2rem;
    }
    .hero-banner h1 { color: #FFFFFF !important; font-size: 2rem !important; margin: 0 0 0.4rem 0 !important; font-weight: 800 !important; }
    .hero-banner p { color: #CBD5E1 !important; font-size: 1.05rem !important; margin: 0 !important; }

    .token-stage {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 1.1rem;
        margin: 0.8rem 0;
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }
    .token-chip {
        display: inline-flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 8px 12px;
        border-radius: 12px;
        border: 2px solid;
        min-width: 80px;
        text-align: center;
    }
    .token-word { font-size: 1.25rem; font-weight: 800; line-height: 1.2; margin-bottom: 4px; }
    .token-pos { font-size: 0.78rem; font-weight: 700; }
    .token-lemma { font-size: 0.74rem; opacity: 0.85; font-family: monospace; margin-top: 2px; }
    .ambig-badge {
        margin-top: 4px; font-size: 0.68rem; background: #FEF08A; color: #854D0E;
        padding: 1px 7px; border-radius: 999px; font-weight: 700; border: 1px solid #FACC15;
    }

    .info-card {
        background: #FFFFFF;
        color: #0F172A;
        border-radius: 12px;
        padding: 0.8rem 1rem;
        border: 1px solid #E2E8F0;
        border-left: 6px solid #4F46E5;
        margin-bottom: 0.6rem;
    }

    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { height: 48px; padding: 0 18px; font-size: 0.98rem; font-weight: 700; }
    </style>
    """,
    unsafe_allow_html=True,
)


def renderizar_tokens_html(tokens: list[TokenAnalisado], destacar_palavra: str | None = None) -> str:
    """Um cartão colorido por palavra: palavra, classe e (se mudar) a forma base."""
    blocos = ['<div class="token-stage">']
    for t in tokens:
        info = POS_INFO[t.classe]
        destaque = ""
        if destacar_palavra and t.normalizado == destacar_palavra.lower():
            destaque = "box-shadow: 0 0 0 4px #FACC15; transform: scale(1.05);"
        lema_html = (
            f'<span class="token-lemma">→ {html.escape(t.lema)}</span>'
            if t.classe in ("SUB", "VERB", "ADJ") and t.lema != t.normalizado
            else ""
        )
        amb_html = '<span class="ambig-badge">⚡ Ambígua</span>' if t.eh_ambigua else ""
        blocos.append(
            f'<div class="token-chip" style="background:{info["cor_fundo"]}; '
            f'border-color:{info["cor_borda"]}; color:{info["cor_texto"]}; {destaque}">'
            f'<div class="token-word">{html.escape(t.texto)}</div>'
            f'<div class="token-pos">{info["icone"]} {info["nome_curto"]}</div>'
            f"{lema_html}{amb_html}</div>"
        )
    blocos.append("</div>")
    return "".join(blocos)


# ============================================================================
# CONTEÚDO: PALAVRAS GÊMEAS E QUIZ
# ============================================================================

CASOS_AMBIGUIDADE = {
    "🎮 jogo — jogar × o game": {
        "palavra": "jogo",
        "frase_1": "Toda sexta eu jogo bola na quadra e depois treino online.",
        "titulo_1": "Verbo «jogar»",
        "explicacao_1": "Vem depois de **«eu»**, então é uma ação: **Verbo** → `jogar`.",
        "frase_2": "Esse jogo de mundo aberto tem gráficos absurdos.",
        "titulo_2": "Substantivo «jogo»",
        "explicacao_2": "Vem depois de **«Esse»**, então é uma coisa: **Substantivo** → `jogo`.",
    },
    "😂 rio — rir × curso d'água": {
        "palavra": "rio",
        "frase_1": "Eu rio demais com esses vídeos curtos de stand-up.",
        "titulo_1": "Verbo «rir»",
        "explicacao_1": "Depois de **«Eu»** é o verbo *rir*. Um stemmer deixa `rio` nos dois sentidos; com a classe, vira `rir`.",
        "frase_2": "A travessia de caiaque pelo rio exige bastante preparo.",
        "titulo_2": "Substantivo «rio»",
        "explicacao_2": "Depois de **«pelo»** (por + o) é o curso d'água: **Substantivo** → `rio`.",
    },
    "🎤 canto — cantar × lugar": {
        "palavra": "canto",
        "frase_1": "Eu canto na banda da escola desde o ano passado.",
        "titulo_1": "Verbo «cantar»",
        "explicacao_1": "Depois de **«Eu»** é ação: **Verbo** → `cantar`.",
        "frase_2": "Coloquei a mesa do computador no canto do quarto.",
        "titulo_2": "Substantivo «canto»",
        "explicacao_2": "Depois de **«no»** (em + o) é um lugar: **Substantivo** → `canto`.",
    },
    "💳 banco — bancar × instituição": {
        "palavra": "banco",
        "frase_1": "Se todo mundo passar na prova, eu banco o açaí da galera!",
        "titulo_1": "Verbo «bancar»",
        "explicacao_1": "Depois de **«eu»** e antes de «o açaí»: **Verbo** → `bancar`.",
        "frase_2": "Abri minha primeira conta pelo aplicativo do banco digital.",
        "titulo_2": "Substantivo «banco»",
        "explicacao_2": "Depois de **«do»** e antes de «digital»: **Substantivo** → `banco`.",
    },
    "🥭 manga — zombar × fruta": {
        "palavra": "manga",
        "frase_1": "Ele nunca manga dos amigos quando alguém erra a questão.",
        "titulo_1": "Verbo «mangar»",
        "explicacao_1": "Depois de **«Ele nunca»** é ação: **Verbo** → `mangar`.",
        "frase_2": "Comprei um suco de manga gelado depois da aula.",
        "titulo_2": "Substantivo «manga»",
        "explicacao_2": "Depois de **«de»** e antes de «gelado»: **Substantivo** → `manga`.",
    },
    "🏊 nada — nadar × nenhuma coisa": {
        "palavra": "nada",
        "frase_1": "Aquele atleta nada cem metros em menos de um minuto.",
        "titulo_1": "Verbo «nadar»",
        "explicacao_1": "É a ação do sujeito «Aquele atleta»: **Verbo** → `nadar`.",
        "frase_2": "A gente não entendeu nada daquela questão difícil.",
        "titulo_2": "Pronome «nada»",
        "explicacao_2": "Depois de «não entendeu» significa *nenhuma coisa*: **Pronome** (descartado pelo buscador).",
    },
}

QUESTOES_DESAFIO = [
    {
        "categoria": "⚡ Palavra gêmea",
        "frase": "Eu rio toda vez que vejo esse corte, mas nunca nadei naquele rio.",
        "foco_exibicao": "1º «rio» (em «Eu rio»)",
        "correta": "VERB",
        "dica": "Que palavra vem logo antes do primeiro «rio»?",
        "explicacao": "Em **«Eu rio»** é o **Verbo `rir`**. Já em **«naquele rio»** é **Substantivo**.",
    },
    {
        "categoria": "🎮 Gíria da internet",
        "frase": "O time inteiro tankou a partida até o último segundo.",
        "foco_exibicao": "«tankou»",
        "correta": "VERB",
        "dica": "Olhe a terminação «-ou», igual a «jogou», «ganhou»...",
        "explicacao": "Mesmo sendo gíria, a terminação `-ou` e a posição depois do sujeito mostram que é **Verbo (`tankar`)**.",
    },
    {
        "categoria": "🔍 Palavra que o buscador descarta",
        "frase": "Os estudantes pesquisaram sobre inteligência artificial na biblioteca.",
        "foco_exibicao": "«sobre»",
        "correta": "CON",
        "dica": "Essa palavra tem significado próprio ou só liga outras palavras?",
        "explicacao": "**«sobre»** é preposição (**Conector**): ajuda a entender a frase, mas é descartada pelo buscador.",
    },
    {
        "categoria": "🎭 Palavra gêmea",
        "frase": "Deixei o violão encostado no canto escuro do estúdio.",
        "foco_exibicao": "«canto»",
        "correta": "SUB",
        "dica": "Repare no «no» antes e no «escuro» depois.",
        "explicacao": "Entre **«no»** e o adjetivo **«escuro»**, «canto» é um lugar: **Substantivo**.",
    },
    {
        "categoria": "✨ Intensidade",
        "frase": "O novo algoritmo deixou a busca absurdamente rápida.",
        "foco_exibicao": "«absurdamente»",
        "correta": "ADV",
        "dica": "Olhe o final «-mente».",
        "explicacao": "Palavras com `-mente` que intensificam um adjetivo são **Advérbios**.",
    },
    {
        "categoria": "💳 Palavra gêmea",
        "frase": "Relaxa, hoje eu banco o ingresso do cinema pra você!",
        "foco_exibicao": "«banco»",
        "correta": "VERB",
        "dica": "Aqui «banco» é um lugar ou significa «eu pago»?",
        "explicacao": "Depois de **«eu»** e antes de «o ingresso», é o **Verbo `bancar`** (pagar).",
    },
]


# ============================================================================
# BARRA LATERAL: LEGENDA DAS CORES
# ============================================================================

with st.sidebar:
    st.markdown("### 🎨 Legenda das cores")
    for codigo in ["SUB", "VERB", "ADJ", "ADV", "PRON", "CON"]:
        info = POS_INFO[codigo]
        st.markdown(
            f'<div style="background:{info["cor_fundo"]}; border-left:5px solid {info["cor_borda"]}; '
            f'padding:6px 10px; border-radius:8px; margin-bottom:6px; color:{info["cor_texto"]};">'
            f'<b>{info["icone"]} {info["nome_exibicao"]}</b><br>'
            f'<span style="font-size:0.8rem;">{info["papel"]}</span></div>',
            unsafe_allow_html=True,
        )
    st.caption("Pronomes e conectores ajudam a entender a frase, mas o buscador os descarta.")
    st.markdown("---")
    st.caption(
        "🎓 **Feira de Extensão — ICMC/USP** · SCC0282\n\n"
        "Ana Paula de Abreu Batista · Italo Carlos Martins Bresciani"
    )


# ============================================================================
# BANNER E ABAS
# ============================================================================

st.markdown(
    '<div class="hero-banner">'
    "<h1>⚡ Como o Google e as IAs entendem o português?</h1>"
    "<p>Veja como a <b>etiquetagem gramatical (POS Tagging)</b> ajuda o computador a diferenciar "
    "palavras iguais com sentidos diferentes.</p>"
    "</div>",
    unsafe_allow_html=True,
)

aba_raiox, aba_ambiguidade, aba_busca, aba_desafio, aba_arquitetura = st.tabs(
    ["🔍 Raio-X da Frase", "🎭 Palavras Gêmeas", "🚀 Buscador", "⚡ Desafio", "⚙️ Por Trás do Código"]
)


# ----------------------------------------------------------------------------
# ABA 1: RAIO-X DA FRASE
# ----------------------------------------------------------------------------
with aba_raiox:
    st.write("Digite uma frase e veja a classe gramatical que o computador dá para cada palavra.")

    exemplos = {
        "😂 eu rio × do rio": "Eu rio demais com esses vídeos, mesmo morando perto do rio!",
        "🎮 eu jogo × esse jogo": "Toda sexta eu jogo bola, mas esse jogo novo tá absurdo.",
        "⚡ gíria: tankou": "O time inteiro tankou a partida até o último segundo!",
        "🎤 eu canto × no canto": "Eu canto na banda e deixei meu violão no canto do quarto.",
        "💳 eu banco × um banco": "Hoje eu banco o lanche se a gente achar um banco vazio na praça.",
    }

    if "frase_ativa" not in st.session_state:
        st.session_state.frase_ativa = next(iter(exemplos.values()))

    for i, (col, (rotulo, frase_ex)) in enumerate(zip(st.columns(len(exemplos)), exemplos.items())):
        if col.button(rotulo, width="stretch", key=f"ex_btn_{i}"):
            st.session_state.frase_ativa = frase_ex

    frase_input = st.text_input("✍️ Sua frase:", value=st.session_state.frase_ativa, key="input_raiox")

    if frase_input.strip():
        tokens = analisar_frase(frase_input)
        st.markdown(renderizar_tokens_html(tokens), unsafe_allow_html=True)

        ambiguas = [t for t in tokens if t.eh_ambigua]
        if ambiguas:
            lista = ", ".join(f"**«{t.texto}»** = {POS_INFO[t.classe]['nome_curto']} (`{t.lema}`)" for t in ambiguas)
            st.info(f"⚡ Palavras ambíguas resolvidas pelo contexto: {lista}")

        indexados = [t for t in tokens if not t.eh_stopword]
        descartados = [t for t in tokens if t.eh_stopword and t.classe != "PUNCT"]
        st.markdown("#### 📌 O que o buscador guarda dessa frase")
        if indexados:
            st.success(" ".join(f"`({t.lema}, {POS_INFO[t.classe]['nome_curto']})`" for t in indexados))
        if descartados:
            st.caption("🗑️ Descartadas: " + ", ".join(f"«{t.texto}»" for t in descartados))

        with st.expander("🤔 Por que cada palavra recebeu essa classe?"):
            for t in tokens:
                if t.classe != "PUNCT":
                    st.markdown(f"- **{t.texto}** ({POS_INFO[t.classe]['nome_curto']}): {t.pista_contexto}")


# ----------------------------------------------------------------------------
# ABA 2: PALAVRAS GÊMEAS
# ----------------------------------------------------------------------------
with aba_ambiguidade:
    st.write(
        "Muitas palavras se escrevem igual mas têm sentidos diferentes: «eu **jogo** bola» × «esse **jogo** é bom». "
        "O buscador precisa saber a classe antes de reduzir a palavra à forma base."
    )

    escolha_caso = st.selectbox("Escolha uma palavra:", list(CASOS_AMBIGUIDADE.keys()))
    dados = CASOS_AMBIGUIDADE[escolha_caso]
    palavra_foco = dados["palavra"]

    for col, n in zip(st.columns(2, gap="large"), ("1", "2")):
        with col:
            st.markdown(f"#### {dados['titulo_' + n]}")
            toks = analisar_frase(dados["frase_" + n])
            st.markdown(renderizar_tokens_html(toks, destacar_palavra=palavra_foco), unsafe_allow_html=True)
            alvo = next((x for x in toks if x.normalizado == palavra_foco), toks[0])
            st.markdown(f"✅ Com POS: `{alvo.lema}` · ⚠️ Stemmer sem POS: `{alvo.stem_nltk}`")
            st.caption(dados["explicacao_" + n])

    st.markdown("---")
    frase_dupla = st.text_input(
        f"🧪 Sua vez: escreva uma frase usando «{palavra_foco}» com os dois sentidos",
        value=f"Sempre que eu {palavra_foco}, todo mundo comenta sobre esse {palavra_foco}!",
        key="input_teste_duplo",
    )
    if frase_dupla.strip():
        st.markdown(renderizar_tokens_html(analisar_frase(frase_dupla), destacar_palavra=palavra_foco), unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# ABA 3: SIMULADOR DE BUSCADOR
# ----------------------------------------------------------------------------
with aba_busca:
    st.write(
        "Pesquise numa coleção de 8 textos e compare dois buscadores: um que só olha as letras "
        "da palavra e outro que também sabe a classe gramatical."
    )

    consultas_demo = [
        "Eu rio muito com vídeos",
        "Travessia pelo rio gelado",
        "Eu canto na escola",
        "Mesa no canto da parede",
        "Eu jogo com meu time",
        "Lançamento do novo jogo",
        "Eu banco o lanche da galera",
        "Abrir conta no banco digital",
    ]

    if "query_ativa" not in st.session_state:
        st.session_state.query_ativa = consultas_demo[0]

    cols_q = st.columns(4)
    for idx_q, q_str in enumerate(consultas_demo):
        if cols_q[idx_q % 4].button(f"🔍 {q_str}", width="stretch", key=f"q_btn_{idx_q}"):
            st.session_state.query_ativa = q_str

    query_user = st.text_input("Sua pesquisa:", value=st.session_state.query_ativa, key="input_query_ri")

    if query_user.strip():
        res = buscar_documentos(query_user)
        semanticos: list[TokenAnalisado] = res["termos_semanticos"]  # type: ignore
        if semanticos:
            st.caption(
                "Termos procurados: " + " · ".join(f"`({t.lema}, {POS_INFO[t.classe]['nome_curto']})`" for t in semanticos)
            )

        colunas = (
            ("⚠️ Sem POS Tagging", "Só compara letras/radical: confunde palavras gêmeas.",
             res["resultados_sem_pos"], "#F59E0B", "#FFFBEB"),
            ("✅ Com POS Tagging", "Compara (forma base, classe): traz só o sentido certo.",
             res["resultados_com_pos"], "#10B981", "#ECFDF5"),
        )
        for col, (titulo, legenda, resultados, borda, fundo) in zip(st.columns(2, gap="large"), colunas):
            with col:
                st.markdown(f"#### {titulo}")
                st.caption(legenda)
                if not resultados:
                    st.info("Nenhum documento encontrado.")
                for item in resultados:  # type: ignore
                    d = item["documento"]
                    st.markdown(
                        f'<div class="info-card" style="border-left-color:{borda}; background:{fundo};">'
                        f"<b>{d.icone} {html.escape(d.titulo)}</b>"
                        f'<div style="font-size:0.85rem; margin-top:4px; color:#334155;">'
                        f'Encontrou: {html.escape(", ".join(item["matches"]))}</div></div>',
                        unsafe_allow_html=True,
                    )


# ----------------------------------------------------------------------------
# ABA 4: DESAFIO (QUIZ)
# ----------------------------------------------------------------------------
with aba_desafio:
    for chave, inicial in (("q_idx", 0), ("q_score", 0), ("q_done", False), ("q_hit", False)):
        st.session_state.setdefault(chave, inicial)

    p1, p2, p3 = st.columns(3)
    p1.metric("🏆 Pontos", st.session_state.q_score)
    p2.metric("📍 Rodada", f"{st.session_state.q_idx + 1} / {len(QUESTOES_DESAFIO)}")
    if p3.button("🔄 Recomeçar", width="stretch"):
        st.session_state.q_idx = 0
        st.session_state.q_score = 0
        st.session_state.q_done = False
        st.rerun()

    questao = QUESTOES_DESAFIO[st.session_state.q_idx]

    st.markdown(
        '<div style="background:#0F172A; color:#F8FAFC; border-radius:16px; padding:1.5rem; margin:1rem 0;">'
        f'<div style="color:#818CF8; font-weight:800; font-size:0.85rem; text-transform:uppercase;">{questao["categoria"]}</div>'
        f'<div style="font-size:1.45rem; font-weight:700; margin:10px 0; color:#FFFFFF;">“{questao["frase"]}”</div>'
        f'<div style="font-size:1.05rem; color:#CBD5E1;">Qual é a classe de <b style="color:#FACC15;">{questao["foco_exibicao"]}</b>?</div>'
        "</div>",
        unsafe_allow_html=True,
    )

    with st.expander("💡 Dica"):
        st.write(questao["dica"])

    cols_alt = st.columns(3)
    for i, cod_a in enumerate(["SUB", "VERB", "ADJ", "ADV", "CON"]):
        if cols_alt[i % 3].button(
            f"{POS_INFO[cod_a]['icone']} {POS_INFO[cod_a]['nome_exibicao']}",
            key=f"alt_{st.session_state.q_idx}_{cod_a}",
            width="stretch",
            disabled=st.session_state.q_done,
        ):
            st.session_state.q_done = True
            st.session_state.q_hit = cod_a == questao["correta"]
            if st.session_state.q_hit:
                st.session_state.q_score += 10
                st.balloons()
            st.rerun()

    if st.session_state.q_done:
        if st.session_state.q_hit:
            st.success(f"✅ **Acertou! (+10 pts)** {questao['explicacao']}")
        else:
            certa = POS_INFO[questao["correta"]]
            st.error(f"❌ **Quase!** A resposta é **{certa['icone']} {certa['nome_exibicao']}**. {questao['explicacao']}")

        st.markdown(renderizar_tokens_html(analisar_frase(questao["frase"])), unsafe_allow_html=True)

        if st.session_state.q_idx + 1 < len(QUESTOES_DESAFIO):
            if st.button("➡️ Próxima", type="primary", width="stretch"):
                st.session_state.q_idx += 1
                st.session_state.q_done = False
                st.rerun()
        else:
            st.success(f"🏁 **Fim!** Você fez **{st.session_state.q_score} de {len(QUESTOES_DESAFIO) * 10} pontos**.")


# ----------------------------------------------------------------------------
# ABA 5: POR TRÁS DO CÓDIGO
# ----------------------------------------------------------------------------
with aba_arquitetura:
    st.markdown(
        """
        1. **spaCy** (`pt_core_news_sm`) separa a frase em palavras e dá a classe gramatical de cada uma (UPOS).
        2. **Regras de contexto** corrigem as palavras gêmeas: depois de «o / no / do / esse» → Substantivo; depois de «eu / ele / não» → Verbo.
        3. **Lematização**: cada palavra vira sua forma base usando a classe (`rio` + Verbo → `rir`). Comparamos com o **stemmer RSLP do NLTK**, que só corta letras e dá o mesmo radical para os dois sentidos (`jogo` → `jog`).
        4. **Indexação**: pronomes e conectores são descartados; o resto vira o par `(forma base, classe)` usado na busca.
        """
    )

    frase_tec = st.text_input(
        "Frase para inspecionar:",
        value="Eu rio demais com esses vídeos, mesmo morando perto do rio!",
        key="input_tabela_tec",
    )
    if frase_tec.strip():
        st.dataframe(
            [
                {
                    "Palavra": t.texto,
                    "Classe": f"{POS_INFO[t.classe]['icone']} {POS_INFO[t.classe]['nome_curto']}",
                    "UPOS (spaCy)": t.upos_spacy,
                    "Forma base (lema)": t.lema,
                    "Radical (stemmer NLTK)": t.stem_nltk,
                    "Vai pro buscador?": "não" if t.eh_stopword else "sim",
                }
                for t in analisar_frase(frase_tec)
            ],
            width="stretch",
            hide_index=True,
        )

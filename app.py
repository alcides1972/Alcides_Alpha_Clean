import math
import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import streamlit.components.v1 as components

from data import get_data
from scoring import calcular_score, classificar

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="ALPHA",
    layout="wide"
)

# =========================================================
# CARGA PRINCIPAL DE DADOS
# =========================================================
df = get_data()

if df is None:

    st.error(
        "get_data() retornou None — revise data.py"
    )

    st.stop()

if not isinstance(df, pd.DataFrame):

    st.error(
        "get_data() não retornou DataFrame válido."
    )

    st.stop()

# SUBSTITUA TODO ESSE BLOCO POR:

# =========================================================
# VALIDAÇÃO PRINCIPAL SEGURA
# =========================================================
if df is None:

    st.error(
        "get_data() retornou None."
    )

    st.stop()

if not isinstance(df, pd.DataFrame):

    st.error(
        "get_data() não retornou DataFrame."
    )

    st.stop()

# Se vier vazio, NÃO parar sistema.
if df.empty:

    st.warning(
        "Base vazia no momento — carregando modo diagnóstico."
    )

    df = pd.DataFrame(
        [
            {
                "Ticker": "PETR4",
                "longName": "Modo Diagnóstico",
                "currentPrice": 0,
                "marketCap": 0
            }
        ]
    )
# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.title("ALPHA")
st.sidebar.caption("Institutional Equity Intelligence")
st.sidebar.write("Monitoramento estratégico B3")

# =========================================================
# MENU COM SCROLL REAL + TÍTULOS EXATOS
# APAGUE TODO O BLOCO ANTIGO “MENU COM SCROLL REAL”
# E COLE ESTE BLOCO INTEIRO NO LUGAR
# =========================================================
st.sidebar.markdown("---")
st.sidebar.subheader("📌 Navegação Rápida")

menu_links = {
    "🏆 Watchlist Premium": "watchlist-premium",
    "🌍 Radar de Setores": "radar-setores",
    "🏦 Fluxo Institucional Hoje": "fluxo-inst",
    "📅 Prognóstico Bimestral": "prognostico",
    "🔎 Consulta Individual": "consulta",
    "📈 Gráfico Avançado": "grafico",
    "🧠 Diagnóstico Institucional": "diagnostico",
    "🚨 Alerta Institucional": "alerta",
    "📡 Radar Institucional": "radar",
    "🚦 Semáforo Institucional": "semaforo",
    "🎯 Preço Alvo": "preco-alvo",
    "⚡ Catalisadores": "catalisadores",
    "🏅 Ranking Geral": "ranking"
}

for nome, ancora in menu_links.items():

    st.sidebar.markdown(
        f"""
        <a href="#{ancora}" target="_self" style="
            text-decoration:none;
            font-size:15px;
            display:block;
            padding:4px 0;
        ">
            {nome}
        </a>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# FUNÇÃO PARA TÍTULOS COM ÂNCORA
# =========================================================
def titulo_secao(id_secao, texto):
    st.markdown(
        f'<h3 id="{id_secao}">{texto}</h3>',
        unsafe_allow_html=True
    )


# =========================================================
# CACHE
# =========================================================
@st.cache_data(ttl=300)
def carregar_dados():
    return get_data()

# =========================================================
# ESTILO
# =========================================================
st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(
            135deg,
            #0b1220,
            #1e293b,
            #334155
        );
        color: #f8fafc;
    }

    /* =========================================================
    SIDEBAR
    ========================================================= */
    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            rgba(15,23,42,0.96),
            rgba(30,41,59,0.96)
        );
        border-right: 1px solid rgba(255,255,255,0.06);
    }

    /* =========================================================
    TEXTOS
    ========================================================= */
    h1, h2, h3, h4, h5, h6 {
        color: #f8fafc !important;
        font-weight: 800 !important;
    }

    p, div, span, label {
        color: #e2e8f0 !important;
    }

    /* =========================================================
    KPIs
    ========================================================= */
    .stMetric {
        background: rgba(255,255,255,0.06);
        padding: 16px;
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 4px 14px rgba(0,0,0,0.18);
    }

    /* =========================================================
    EXPANDER
    ========================================================= */
    div[data-testid="stExpander"] {
        background: rgba(255,255,255,0.05);
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.08);
    }

    /* =========================================================
    SELECTBOX / INPUT
    ========================================================= */
    div[data-baseweb="select"] > div {
        background-color: rgba(255,255,255,0.06) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
    }

    /* =========================================================
    DATAFRAME
    ========================================================= */
    div[data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    /* =========================================================
    BUTTONS
    ========================================================= */
    .stButton > button {
        background: rgba(255,255,255,0.08);
        color: white;
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.10);
        font-weight: 600;
    }

    .stButton > button:hover {
        background: rgba(255,255,255,0.14);
        border: 1px solid rgba(255,255,255,0.18);
    }

    /* =========================================================
    SCROLLBAR
    ========================================================= */
    ::-webkit-scrollbar {
        width: 10px;
    }

    ::-webkit-scrollbar-track {
        background: #0f172a;
    }

    ::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #475569;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# HEADER
# =========================================================
col_titulo, col_logo = st.columns([5, 1])

with col_titulo:
    st.title("ALPHA – Institutional Equity Intelligence")

with col_logo:
    try:
        st.image("bull.png", width=180)
    except:
        pass

st.caption("Ranking B3 | Atualização automática | Score institucional")
def render_top_bar(df):
    ticker_html_items = []

    for _, row_ticker in df.iterrows():

        ticker_nome = row_ticker["Ticker"]

        try:
            hist_dia = yf.Ticker(
                f"{ticker_nome}.SA"
            ).history(period="2d")

            if len(hist_dia) >= 2:

                preco_atual = hist_dia["Close"].iloc[-1]
                preco_anterior = hist_dia["Close"].iloc[-2]

                variacao = (
                    (preco_atual - preco_anterior)
                    / preco_anterior
                ) * 100

                if variacao >= 0:
                    seta = "▲"
                    cor = "#22c55e"
                else:
                    seta = "▼"
                    cor = "#ef4444"

                ticker_html_items.append(
                    f"""
                    <span style='
                        margin-right:40px;
                        font-weight:bold;
                        color:white;
                        font-size:16px;
                        white-space:nowrap;
                    '>

                    {ticker_nome}

                    <span style='color:{cor};'>
                        {seta} {variacao:.2f}%
                    </span>

                    </span>
                    """
                )

        except:
            continue

    ticker_html = "".join(ticker_html_items)

    barra_topo = f"""
    <div style="
        width:100%;
        background-color:black;
        overflow:hidden;
        white-space:nowrap;
        padding:3px 0;
        border-bottom:1px solid rgba(255,255,255,0.15);
        margin-bottom:2px;
    ">

        <div style="
            display:inline-block;
            padding-left:100%;
            animation: ticker-scroll 80s linear infinite;
        ">

            {ticker_html}

        </div>

    </div>

    <style>

    @keyframes ticker-scroll {{

        0% {{
            transform: translateX(0);
        }}

        100% {{
            transform: translateX(-100%);
        }}

    }}

    </style>
    """

    components.html(
        barra_topo,
        height=42
    )
   
# =========================================================
# DADOS
# =========================================================
df = carregar_dados()

if df is not None and not df.empty:

    render_top_bar(df)

else:

    st.error(
        "Dados não carregados corretamente. Verifique get_data()."
    )
def render_macro_panel():
    macro_ativos = {
        "USD/BRL": "BRL=X",
        "EUR/BRL": "EURBRL=X",
        "IBOV": "^BVSP",
        "S&P500": "^GSPC",
        "BTC": "BTC-USD",
        "Brent": "BZ=F",
        "Ouro": "GC=F"
    }

    macro_cards = []

    for nome, ticker_macro in macro_ativos.items():

        try:

            hist_macro = yf.Ticker(
                ticker_macro
            ).history(period="2d")

            if len(hist_macro) >= 2:

                valor_atual = hist_macro["Close"].iloc[-1]
                valor_anterior = hist_macro["Close"].iloc[-2]

                variacao = (
                    (valor_atual - valor_anterior)
                    / valor_anterior
                ) * 100

                if variacao >= 0:
                    seta = "▲"
                    cor = "#22c55e"
                else:
                    seta = "▼"
                    cor = "#ef4444"

                macro_cards.append(
                    f"""
                    <span style='
                        margin-right:18px;
                        color:white;
                        font-size:12px;
                        white-space:nowrap;
                    '>

                        <strong>{nome}</strong>
                        {valor_atual:,.2f}

                        <span style='color:{cor}; font-weight:bold;'>
                            {seta} {variacao:.2f}%
                        </span>

                    </span>
                    """
                )

        except:
            continue

    macro_html = "".join(macro_cards)

    painel_macro = f"""
    <div style="
        width:100%;
        background:#050505;
        padding:1px 10px;
        overflow:hidden;
        white-space:nowrap;
        border-bottom:1px solid rgba(255,255,255,0.12);
        margin-bottom:8px;
    ">

        {macro_html}

    </div>
    """

    components.html(
        painel_macro,
        height=28
    )

if df is None or df.empty:
    st.error("Nenhum dado carregado.")
    st.stop()

# =========================================================
# SCORE
# =========================================================
df["Score"] = df.apply(calcular_score, axis=1)

df["Classificação"] = df["Score"].apply(classificar)

df["Preço Justo"] = (
    df["currentPrice"] * (
        1 + ((df["Score"] - 5) * 0.10)
    )
)

df["Upside %"] = (
    ((df["Preço Justo"] / df["currentPrice"]) - 1) * 100
)

# PROBLEMA REAL:
# O df principal existe, mas o FILTRO INSTITUCIONAL está zerando df_filtrado.
# Ou seja: o app carrega, mas depois algum filtro remove todos os ativos.

# =========================================================
# LOCALIZE TODO O BLOCO:
# FILTRO INSTITUCIONAL
# =========================================================

# E SUBSTITUA COMPLETAMENTE POR ESTE:

# =========================================================
# FILTRO INSTITUCIONAL (VERSÃO SEGURA)
# =========================================================
filtro = st.sidebar.selectbox(
    "Filtro Institucional",
    [
        "Todos",
        "Compra Forte",
        "Compra",
        "Neutro",
        "Atenção"
    ],
    key="filtro_institucional_sidebar"
)

df_filtrado = df.copy()

# =====================================================
# FILTRO CONDICIONAL
# =====================================================
if (
    filtro != "Todos" and
    "Classificação" in df_filtrado.columns
):

    df_temp = df_filtrado[
        df_filtrado["Classificação"] == filtro
    ].copy()

    # Se filtro não encontrar ativos,
    # mantém base geral ao invés de zerar sistema
    if not df_temp.empty:

        df_filtrado = df_temp

# =====================================================
# GARANTIA FINAL
# =====================================================
if df_filtrado.empty:

    df_filtrado = df.copy()
# =========================================================
# KPIs
# =========================================================
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Ações analisadas",
        len(df)
    )

with col2:

    if not df.empty:
        top_ticker = (
            df.sort_values(
                "Score",
                ascending=False
            )
            .iloc[0]["Ticker"]
        )
    else:
        top_ticker = "-"

    st.metric(
        "Top Score",
        top_ticker
    )

with col3:

    if not df.empty:
        score_medio = round(
            df["Score"].mean(),
            2
        )
    else:
        score_medio = 0

    st.metric(
        "Score Médio",
        score_medio
    )
st.metric("Score Médio", score_medio)

# =========================================================
# MELHOR OPORTUNIDADE HOJE
# =========================================================
if not df.empty:

    melhor_ativo = df.sort_values(
        ["Upside %", "Score"],
        ascending=False
    ).iloc[0]

    ticker_top = melhor_ativo["Ticker"]

    empresa_top = melhor_ativo.get(
        "longName",
        ticker_top
    )

    upside_top = round(
        melhor_ativo["Upside %"],
        2
    )

    score_top = round(
        melhor_ativo["Score"],
        2
    )

    classificacao_top = melhor_ativo["Classificação"]

    st.info(
        f"🏆 Melhor Oportunidade Hoje: {ticker_top} — {empresa_top} | "
        f"Score: {score_top} | Upside: {upside_top}% | "
        f"{classificacao_top}"
    )
from datetime import datetime
# =========================================================
# WATCHLIST PREMIUM
# =========================================================
st.subheader("⭐ Watchlist Premium Day")

watchlist = df[
    (df["Score"] >= 7) &
    (df["Upside %"] >= 15)
].sort_values(
    ["Score", "Upside %"],
    ascending=False
)

if not watchlist.empty:

    colunas_watch = [
        "Ticker",
        "currentPrice",
        "Score",
        "Preço Justo",
        "Upside %",
        "Classificação"
    ]

    st.dataframe(
        watchlist[colunas_watch].head(10),
        use_container_width=True,
        height=320
    )

else:

    st.info(
        "Nenhum ativo atingiu critério premium hoje."
    )
    # =========================================================
# RADAR DE SETORES
# =========================================================
st.subheader("🌍 Radar de Setores")

setores = {
    "Financeiro": ["ITUB4", "BBDC4", "BBAS3", "SANB11", "BPAC11"],
    "Energia": ["PETR4", "PRIO3", "ELET3", "TAEE11", "CPFE3", "EQTL3"],
    "Consumo": ["ABEV3", "LREN3", "VULC3", "ASAI3"],
    "Construção": ["CYRE3", "EZTC3", "DIRR3", "CURY3"],
    "Logística": ["RAIL3", "RENT3", "CCRO3"],
    "Tecnologia": ["TOTS3", "POSI3", "WEGE3"]
}

dados_setores = []

for setor, lista_tickers in setores.items():

    df_setor = df[
        df["Ticker"].isin(lista_tickers)
    ]

    if not df_setor.empty:

        media_score = round(
            df_setor["Score"].mean(),
            2
        )

        media_upside = round(
            df_setor["Upside %"].mean(),
            2
        )

        forca_setorial = round(
            (media_score * 0.6) +
            (media_upside / 10 * 0.4),
            2
        )

        dados_setores.append({
            "Setor": setor,
            "Score Médio": media_score,
            "Upside Médio %": media_upside,
            "Força Setorial": forca_setorial
        })

df_setores = pd.DataFrame(
    dados_setores
).sort_values(
    "Força Setorial",
    ascending=False
)

def cor_setor(val):

    try:

        if val >= 7:
            return "background-color: rgba(34,197,94,0.35); color:white;"

        elif val >= 5:
            return "background-color: rgba(250,204,21,0.25); color:white;"

        else:
            return "background-color: rgba(239,68,68,0.30); color:white;"

    except:
        return ""

styled_setores = (
    df_setores.style
    .map(cor_setor, subset=["Força Setorial"])
)

st.dataframe(
    styled_setores,
    use_container_width=True,
    height=320
)
# =========================================================
# FLUXO INSTITUCIONAL HOJE
# =========================================================
col_fluxo1, col_fluxo2 = st.columns([8,2])

with col_fluxo1:
    st.subheader("🏦 Fluxo Institucional Hoje")

with col_fluxo2:
    with st.expander("ℹ Entender"):
        st.markdown(
            """
            **Volume Relativo**  
            Volume atual ÷ média 20 pregões  
            >1.5 = forte  
            1.0–1.5 = normal  
            <1.0 = fraco  

            **Momentum**  
            EMA9 > EMA21 = positivo  

            **Score Fluxo**  
            8–10 forte  
            6–8 bom  
            4–6 moderado  
            """
        )

fluxo_lista = []

for ticker_fluxo in df["Ticker"].tolist():

    try:

        hist_fluxo = yf.Ticker(
            f"{ticker_fluxo}.SA"
        ).history(period="6mo")

        if hist_fluxo.empty or len(hist_fluxo) < 25:
            continue

        # =========================================================
        # VOLUME AJUSTADO
        # =========================================================
        if hist_fluxo["Volume"].iloc[-1] == 0:

            volume_atual = hist_fluxo["Volume"].iloc[-2]

        else:

            volume_atual = hist_fluxo["Volume"].iloc[-1]


        volume_medio = (
            hist_fluxo["Volume"]
            .tail(21)
            .head(20)
            .mean()
        )

        if pd.isna(volume_medio) or volume_medio <= 0:
            continue


        volume_ratio = volume_atual / volume_medio


        # =========================================================
        # MOMENTUM
        # =========================================================
        ema9 = hist_fluxo["Close"].ewm(
            span=9
        ).mean().iloc[-1]

        ema21 = hist_fluxo["Close"].ewm(
            span=21
        ).mean().iloc[-1]


        momentum = (
            "Positivo"
            if ema9 > ema21
            else "Negativo"
        )


        # =========================================================
        # SCORE
        # =========================================================
        score_fluxo_ind = round(
            (
                min(volume_ratio, 3) * 2
            ) +
            (
                4 if momentum == "Positivo" else 1
            ),
            2
        )


        # =========================================================
        # LEITURA
        # =========================================================
        if volume_ratio >= 1.5:

            leitura_volume = "Fluxo Forte"

        elif volume_ratio >= 1.0:

            leitura_volume = "Normal"

        else:

            leitura_volume = "Fraco"


        # =========================================================
        # APPEND
        # =========================================================
        fluxo_lista.append({

            "Ticker": ticker_fluxo,

            "Volume Relativo": round(
                volume_ratio,
                2
            ),

            "Leitura Volume": leitura_volume,

            "Momentum": momentum,

            "Score Fluxo": score_fluxo_ind
        })

    except Exception:
        continue
        # =========================================================
        # EXPLICAÇÃO RESUMIDA PARA TABELA
        # =========================================================
        if volume_ratio >= 1.5:
            leitura_volume = "Fluxo Forte"

        elif volume_ratio >= 1.0:
            leitura_volume = "Normal"

        else:
            leitura_volume = "Fraco"

        fluxo_lista.append({

            "Ticker": ticker_fluxo,

            "Volume Relativo": round(
                volume_ratio,
                2
            ),

            "Leitura Volume": leitura_volume,

            "Momentum": momentum,

            "Score Fluxo": score_fluxo_ind
        })

    except:
        continue


df_fluxo = pd.DataFrame(
    fluxo_lista
)

# =========================================================
# RENDERIZAÇÃO FINAL — FLUXO
# =========================================================
df_fluxo = pd.DataFrame(
    fluxo_lista
)

if not df_fluxo.empty and "Score Fluxo" in df_fluxo.columns:

    df_fluxo = df_fluxo.sort_values(
        "Score Fluxo",
        ascending=False
    )

    def cor_fluxo(val):

        try:

            if val >= 8:
                return "background-color: rgba(34,197,94,0.35); color:white;"

            elif val >= 6:
                return "background-color: rgba(250,204,21,0.25); color:white;"

            else:
                return "background-color: rgba(239,68,68,0.30); color:white;"

        except:
            return ""

    styled_fluxo = (
        df_fluxo.head(15)
        .style
        .map(
            cor_fluxo,
            subset=["Score Fluxo"]
        )
    )

    st.dataframe(
        styled_fluxo,
        use_container_width=True,
        height=420
    )

else:

    st.warning(
        "Sem dados de fluxo suficientes no momento."
    )

# =========================================================
# GUIA RESUMIDO — FLUXO INSTITUCIONAL
# =========================================================
with st.expander("📘 Entender Volume Relativo | Momentum | Score Fluxo"):

    st.markdown(
        """
        **Volume Relativo**  
        Relação entre volume atual e média dos últimos 20 pregões.  
        **>1.5:** entrada institucional forte  
        **1.0–1.5:** normal  
        **<1.0:** fraco  

        **Momentum**  
        Compara EMA9 vs EMA21.  
        **Positivo:** força compradora de curto prazo  
        **Negativo:** pressão vendedora  

        **Score Fluxo**  
        Combina volume + momentum.  

        **8–10:** fluxo institucional forte  
        **6–8:** bom  
        **4–6:** moderado  
        **<4:** fraco  
        """
    )
# =========================================================
# FILTRO REFINADO INSTITUCIONAL
# COLE IMEDIATAMENTE ABAIXO DO BLOCO “🏆 Melhor Oportunidade Hoje”
# =========================================================
st.markdown("---")

st.markdown(
    """
    <div style="
        font-size:22px;
        font-weight:800;
        margin-bottom:8px;
    ">
        🎯 Fluxo + Compra Forte + Barra >70% + Técnico
    </div>
    """,
    unsafe_allow_html=True
)

filtro_refinado = []

for _, row in df.iterrows():

    try:

        ticker_ref = row["Ticker"]

        hist_ref = yf.Ticker(
            f"{ticker_ref}.SA"
        ).history(
            period="3mo"
        )

        if hist_ref.empty or len(hist_ref) < 25:
            continue

        # =====================================================
        # FLUXO
        # =====================================================
        volume_medio = hist_ref["Volume"].rolling(
            20
        ).mean().iloc[-1]

        volume_atual = hist_ref["Volume"].iloc[-1]

        if volume_medio <= 0:
            continue

        volume_ratio = volume_atual / volume_medio

        fluxo_positivo = volume_ratio > 1.2

        # =====================================================
        # TÉCNICO
        # =====================================================
        ema9 = hist_ref["Close"].ewm(
            span=9
        ).mean().iloc[-1]

        ema21 = hist_ref["Close"].ewm(
            span=21
        ).mean().iloc[-1]

        tecnico_positivo = ema9 > ema21

        # =====================================================
        # BARRA COMPRADORA
        # =====================================================
        candle = hist_ref.iloc[-1]

        amplitude = candle["High"] - candle["Low"]

        if amplitude <= 0:
            continue

        barra_compradora = (
            (candle["Close"] - candle["Low"]) /
            amplitude
        ) * 100

        barra_forte = barra_compradora >= 70

        # =====================================================
        # CLASSIFICAÇÃO
        # =====================================================
        compra_forte = (
            row["Classificação"] == "Compra Forte"
        )

        # =====================================================
        # CONVERGÊNCIA
        # =====================================================
        if (
            fluxo_positivo and
            tecnico_positivo and
            barra_forte and
            compra_forte
        ):

            filtro_refinado.append(
                f"{ticker_ref} ({barra_compradora:.1f}%)"
            )

    except Exception:
        continue

# =========================================================
# EXIBIÇÃO
# =========================================================
if filtro_refinado:

    st.success(
        " | ".join(filtro_refinado)
    )

else:

    st.warning(
        "Não encontrado no momento."
    )

# =========================================================
# 🚨 SCANNER PROFISSIONAL AUTOMÁTICO
# =========================================================

st.markdown("### 🚨 Scanner Profissional Automático")

scanner_alertas = []

for _, row in df.iterrows():

    try:

        ticker_scan = row["Ticker"]

        hist_scan = yf.Ticker(
            f"{ticker_scan}.SA"
        ).history(
            period="3mo"
        )

        if hist_scan.empty or len(hist_scan) < 25:
            continue

        # =====================================================
        # VOLUME
        # =====================================================
        volume_medio = hist_scan["Volume"].rolling(
            20
        ).mean().iloc[-1]

        volume_atual = hist_scan["Volume"].iloc[-1]

        if volume_atual == 0 and len(hist_scan) > 1:
            volume_atual = hist_scan["Volume"].iloc[-2]

        if volume_medio <= 0:
            continue

        volume_ratio = volume_atual / volume_medio

        # =====================================================
        # MÉDIAS
        # =====================================================
        ema9 = hist_scan["Close"].ewm(
            span=9
        ).mean().iloc[-1]

        ema21 = hist_scan["Close"].ewm(
            span=21
        ).mean().iloc[-1]

        tecnico_ok = ema9 > ema21

        # =====================================================
        # BARRA
        # =====================================================
        candle = hist_scan.iloc[-1]

        amplitude = candle["High"] - candle["Low"]

        if amplitude <= 0:
            continue

        barra_pct = (
            (candle["Close"] - candle["Low"]) /
            amplitude
        ) * 100

        # =====================================================
        # ROMPIMENTO
        # =====================================================
        maxima_20 = hist_scan["High"].rolling(
            20
        ).max().iloc[-2]

        rompimento = candle["Close"] > maxima_20

        # =====================================================
        # CLASSIFICAÇÃO
        # =====================================================
        compra_forte = (
            row.get("Classificação") == "Compra Forte"
        )

        # =====================================================
        # SCORE SCANNER
        # =====================================================
        score_scan = 0

        if volume_ratio > 1.5:
            score_scan += 3

        elif volume_ratio > 1.2:
            score_scan += 2

        if tecnico_ok:
            score_scan += 2

        if barra_pct >= 70:
            score_scan += 2

        if rompimento:
            score_scan += 3

        if compra_forte:
            score_scan += 2

        # =====================================================
        # ALERTA
        # =====================================================
        if score_scan >= 8:

            if score_scan >= 10:
                nivel = "🔥 PRIORIDADE MÁXIMA"

            elif score_scan >= 9:
                nivel = "⚡ FORTE"

            else:
                nivel = "📌 MONITORAR"

            scanner_alertas.append(
                f"{nivel} | {ticker_scan} | Score {score_scan} | Vol {volume_ratio:.2f}x | Barra {barra_pct:.1f}%"
            )

    except Exception:
        continue

# =========================================================
# EXIBIÇÃO
# =========================================================
if scanner_alertas:

    for alerta in scanner_alertas[:12]:

        st.info(
            alerta
        )

else:

    st.warning(
        "Nenhum scanner institucional crítico no momento."
    )
# =========================================================
# PROGNÓSTICO BIMESTRAL INSTITUCIONAL
# =========================================================

hoje = datetime.today()

meses = [
    "Janeiro", "Fevereiro", "Março", "Abril",
    "Maio", "Junho", "Julho", "Agosto",
    "Setembro", "Outubro", "Novembro", "Dezembro"
]

mes_atual = hoje.month - 1

# Regra rolling dia 15
if hoje.day >= 15:
    mes_inicio = (mes_atual + 1) % 12
    mes_fim = (mes_atual + 2) % 12
else:
    mes_inicio = mes_atual
    mes_fim = (mes_atual + 1) % 12

titulo_prognostico = (
    f"Prognóstico {meses[mes_inicio]} - {meses[mes_fim]}"
)

st.subheader(titulo_prognostico)

# Score institucional avançado simplificado
df["Score_Prognostico"] = (
    (df["Score"] * 0.40) +
    (
        df["Upside %"].clip(lower=0, upper=100) / 10
    ) * 0.35 +
    (
        df["revenueGrowth"].fillna(0).clip(lower=-1, upper=1) * 10
    ) * 0.25
)

# =========================================================
# TOP 3 ATENÇÃO
# =========================================================
st.subheader("Top 3 Atenção")

worst3 = df.sort_values(
    "Upside %",
    ascending=True
)[
    [
        "Ticker",
        "currentPrice",
        "Preço Justo",
        "Upside %",
        "Score"
    ]
]

st.dataframe(
    worst3.head(3),
    use_container_width=True
)

# =========================================================
# CONSULTA
# =========================================================
st.subheader("Consulta Individual")

df["Busca"] = (
    df["Ticker"] + " — " +
    df["longName"].fillna("Nome indisponível")
)

busca = st.selectbox(
    "Selecione ou digite ticker / empresa:",
    sorted(df["Busca"].tolist())
)

ticker = busca.split(" — ")[0]

row = df[df["Ticker"] == ticker].iloc[0]

nome_empresa = row.get(
    "longName",
    "Nome indisponível"
)

st.write(f"### {ticker} - {nome_empresa}")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Preço Atual",
        f"R$ {row['currentPrice']:.2f}"
    )

with col2:
    st.metric(
        "Score",
        f"{row['Score']}"
    )

with col3:
    st.metric(
        "Classificação",
        row["Classificação"]
    )

with col4:
    st.metric(
        "Preço Justo",
        f"R$ {row['Preço Justo']:.2f}"
    )

with col5:
    st.metric(
        "Upside",
        f"{row['Upside %']:.2f}%"
    )

# =========================================================
# GRAFICO
# =========================================================
st.subheader("Gráfico Avançado")

period_map = {
    "1H": ("7d", "1h"),
    "4H": ("60d", "4h"),
    "1D": ("6mo", "1d"),
    "1W": ("2y", "1wk"),
    "1M": ("5y", "1mo"),
    "1Y": ("5y", "3mo"),
    "5Y": ("max", "1mo"),
}

col1, col2 = st.columns(2)

with col1:
   periodo_escolhido = st.selectbox(
    "Período",
    list(period_map.keys()),
    index=2
)

with col2:
    tipo_grafico = st.selectbox(
        "Tipo de gráfico",
        ["Candlestick","Linha"]
    )

period, interval = period_map[periodo_escolhido]

hist = yf.Ticker(
    f"{ticker}.SA"
).history(
    period=period,
    interval=interval
)

if hist.empty:
    st.warning("Sem dados históricos.")
    st.stop()
    # =========================================================
# INDICADORES
# =========================================================
hist["EMA9"] = hist["Close"].ewm(span=9).mean()
hist["EMA21"] = hist["Close"].ewm(span=21).mean()
hist["EMA200"] = hist["Close"].ewm(span=200).mean()

delta = hist["Close"].diff()

gain = delta.where(
    delta > 0,
    0
).rolling(14).mean()

loss = (
    -delta.where(delta < 0, 0)
).rolling(14).mean()

rs = gain / loss

hist["RSI"] = 100 - (
    100 / (1 + rs)
)
# =========================================================
# GRÁFICO AVANÇADO EXPANSÍVEL
# =========================================================
with st.expander("📈 Expandir Gráfico Avançado"):

    if tipo_grafico == "Linha":

        st.line_chart(hist["Close"])

    else:

        fig = go.Figure(
            data=[
                go.Candlestick(
                    x=hist.index,
                    open=hist["Open"],
                    high=hist["High"],
                    low=hist["Low"],
                    close=hist["Close"]
                )
            ]
        )

        fig.add_trace(
            go.Scatter(
                x=hist.index,
                y=hist["EMA9"],
                name="EMA9",
                line=dict(width=1)
            )
        )

        fig.add_trace(
            go.Scatter(
                x=hist.index,
                y=hist["EMA21"],
                name="EMA21",
                line=dict(width=1)
            )
        )

        fig.update_layout(

            height=420,

            xaxis_rangeslider_visible=False,

            hovermode="x unified",

            plot_bgcolor="#0f172a",
            paper_bgcolor="#0f172a",

            font=dict(
                color="white"
            ),

            margin=dict(
                l=5,
                r=5,
                t=10,
                b=5
            ),

            xaxis=dict(
                showgrid=True,
                gridcolor="rgba(255,255,255,0.08)",

                showspikes=True,
                spikecolor="yellow",
                spikesnap="cursor",
                spikemode="across",
                spikethickness=1,

                color="white"
            ),

            yaxis=dict(
                side="right",

                showgrid=True,
                gridcolor="rgba(255,255,255,0.08)",

                showspikes=True,
                spikecolor="yellow",
                spikesnap="cursor",
                spikemode="across",
                spikethickness=1,

                color="white"
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displayModeBar": True,
                "scrollZoom": True
            }
        )

    # =========================================================
    # GUIA
    # =========================================================
    with st.expander("📘 Como interpretar este gráfico?"):

        st.markdown(
            """
            ### Leitura Institucional Simplificada

            **EMA9:** tendência curta / força imediata  
            **EMA21:** tendência intermediária  
            **EMA200:** tendência estrutural  

            **RSI < 35:** possível sobrevenda / reação  
            **RSI > 70:** sobrecompra / risco corretivo  

            **Volume alto + preço subindo:** acumulação institucional  
            **Volume alto + preço caindo:** distribuição institucional  

            **Breakout:** rompimento de máxima  
            **Pullback:** correção saudável  
            """
        )
  
# =========================================================
# INDICADORES
# =========================================================
hist["EMA9"] = hist["Close"].ewm(span=9).mean()
hist["EMA21"] = hist["Close"].ewm(span=21).mean()
hist["EMA200"] = hist["Close"].ewm(span=200).mean()

delta = hist["Close"].diff()

gain = delta.where(
    delta > 0,
    0
).rolling(14).mean()

loss = (
    -delta.where(delta < 0, 0)
).rolling(14).mean()

rs = gain / loss

hist["RSI"] = 100 - (
    100 / (1 + rs)
)
# =========================================================
# SCORE FLUXO GLOBAL
# =========================================================
if "Volume" in hist.columns:

    volume_medio = hist["Volume"].rolling(20).mean().iloc[-1]

    if pd.notna(volume_medio) and volume_medio > 0:

        volume_ratio = (
            hist["Volume"].iloc[-1] / volume_medio
        )

    else:
        volume_ratio = 1

else:
    volume_ratio = 1


if volume_ratio > 1.5:
    score_fluxo = 8

elif volume_ratio > 1.1:
    score_fluxo = 6

else:
    score_fluxo = 4

# =========================================================
# DIAGNOSTICO
# =========================================================
st.subheader("Diagnóstico Institucional")

if row["Upside %"] > 25:
    barato_msg = "Forte subvalorização"

elif row["Upside %"] > 10:
    barato_msg = "Preço atrativo"

else:
    barato_msg = "Próximo do preço justo"

ultima = hist.iloc[-1]

bullish_score = 0
bearish_score = 0

# EMA9 x EMA21
if ultima["EMA9"] > ultima["EMA21"]:
    bullish_score += 30
    tendencia_msg = "Alta"
else:
    bearish_score += 30
    tendencia_msg = "Baixa"

# EMA21 x EMA200
if ultima["EMA21"] > ultima["EMA200"]:
    bullish_score += 25
else:
    bearish_score += 25

# RSI
if ultima["RSI"] < 35:
    bullish_score += 20
    rsi_msg = "Sobrevendido"

elif ultima["RSI"] > 70:
    bearish_score += 20
    rsi_msg = "Sobrecomprado"

else:
    rsi_msg = "Neutro"

# PRECO X EMA21
if ultima["Close"] > ultima["EMA21"]:
    bullish_score += 25
    ema21_msg = "Acima EMA21"
else:
    bearish_score += 25
    ema21_msg = "Abaixo EMA21"

total = bullish_score + bearish_score

if total > 0:
    prob_compra = round(
        (bullish_score / total) * 100,
        1
    )
else:
    prob_compra = 50

prob_venda = round(
    100 - prob_compra,
    1
)

if prob_compra >= 70:
    momento_msg = "Alta probabilidade compradora"

elif prob_compra >= 55:
    momento_msg = "Viés comprador"

elif prob_venda >= 70:
    momento_msg = "Pressão vendedora"

else:
    momento_msg = "Neutro"

preco_status = (
    "👍 SIM"
    if row["Upside %"] > 10
    else "👎 NÃO"
)

momento_status = (
    "👍 SIM"
    if prob_compra >= 55
    else "👎 NÃO"
)

st.write(f"**Preço descontado?** {preco_status}")
st.write(f"**Momento certo?** {momento_status}")

st.write(f"**Tendência:** {tendencia_msg}")
st.write(f"**RSI:** {rsi_msg}")
st.write(f"**EMA21:** {ema21_msg}")
st.write(f"**Momento:** {momento_msg}")
# =========================================================
# ALERTA INSTITUCIONAL AUTOMÁTICO
# =========================================================
st.subheader("Alerta Institucional")

alertas = []

# Breakout
max_20 = hist["High"].rolling(20).max().iloc[-1]

if hist["Close"].iloc[-1] >= max_20:
    alertas.append("🚀 Breakout técnico relevante")

# Pullback saudável
if (
    hist["Close"].iloc[-1] > hist["EMA21"].iloc[-1]
    and hist["Close"].iloc[-1] < hist["EMA9"].iloc[-1]
):
    alertas.append("🛒 Pullback em tendência de alta")

# RSI
if hist["RSI"].iloc[-1] > 70:
    alertas.append("⚠ Sobrecomprado / risco corretivo")

elif hist["RSI"].iloc[-1] < 35:
    alertas.append("🔥 Sobrevendido / possível reação")

# Fallback
if not alertas:
    alertas.append("🔎 Sem setup dominante no momento")

# Exibição
for alerta in alertas:

    st.markdown(
        f"""
        <div style="
            padding:10px;
            margin-bottom:8px;
            border-radius:10px;
            background:rgba(255,255,255,0.08);
            border:1px solid rgba(255,255,255,0.15);
            font-size:15px;
            font-weight:600;
        ">
            {alerta}
        </div>
        """,
        unsafe_allow_html=True
    )
# =========================================================
# RADAR INSTITUCIONAL
# =========================================================
st.subheader("Radar Institucional")

# Score Fundamentalista
score_fund = row["Score"]

# Score Técnico
score_tecnico = round(prob_compra / 10, 2)

# Volume relativo
volume_medio_alerta = hist["Volume"].rolling(20).mean().iloc[-1]

if volume_medio_alerta > 0:
    volume_ratio_alerta = (
        hist["Volume"].iloc[-1] / volume_medio_alerta
    )
else:
    volume_ratio_alerta = 1

# Score Fluxo
volume_medio = hist["Volume"].rolling(20).mean().iloc[-1]

if volume_medio > 0:
    volume_ratio = hist["Volume"].iloc[-1] / volume_medio
else:
    volume_ratio = 1

# Score Macro
ibov_hist = yf.Ticker("^BVSP").history(period="1mo")
dolar_hist = yf.Ticker("BRL=X").history(period="1mo")

score_macro = 5

if not ibov_hist.empty:
    if ibov_hist["Close"].iloc[-1] > ibov_hist["Close"].mean():
        score_macro += 2

if not dolar_hist.empty:
    if dolar_hist["Close"].iloc[-1] < dolar_hist["Close"].mean():
        score_macro += 3

score_macro = min(score_macro, 10)


# Classificação visual
def classificar_radar(score):
    if score >= 8:
        return "Forte"
    elif score >= 6:
        return "Positivo"
    elif score >= 4:
        return "Neutro"
    else:
        return "Fraco"


# Cards principais
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Fundamentalista",
        round(score_fund, 2),
        classificar_radar(score_fund)
    )

with col2:
    st.metric(
        "Técnico",
        score_tecnico,
        classificar_radar(score_tecnico)
    )

with col3:
    st.metric(
        "Fluxo",
        score_fluxo,
        classificar_radar(score_fluxo)
    )

with col4:
    st.metric(
        "Macro",
        score_macro,
        classificar_radar(score_macro)
    )


# =========================================================
# DETALHAR RADAR INSTITUCIONAL
# =========================================================
with st.expander("📡 Detalhar Radar Institucional"):

    radar_lista = []

    for _, row in df.iterrows():

        try:

            ticker_radar = row["Ticker"]

            hist_radar = yf.Ticker(
                f"{ticker_radar}.SA"
            ).history(
                period="3mo"
            )

            if hist_radar.empty or len(hist_radar) < 25:
                continue

            # =====================================================
            # VOLUME / FLUXO
            # =====================================================
            volume_medio = hist_radar["Volume"].rolling(
                20
            ).mean().iloc[-1]

            volume_atual = hist_radar["Volume"].iloc[-1]

            # Ajuste pós-fechamento
            if volume_atual == 0 and len(hist_radar) > 1:
                volume_atual = hist_radar["Volume"].iloc[-2]

            if volume_medio <= 0:
                continue

            volume_ratio = volume_atual / volume_medio

            # =====================================================
            # TÉCNICO
            # =====================================================
            ema9 = hist_radar["Close"].ewm(
                span=9
            ).mean().iloc[-1]

            ema21 = hist_radar["Close"].ewm(
                span=21
            ).mean().iloc[-1]

            momentum = (
                "Positivo"
                if ema9 > ema21
                else "Negativo"
            )

            # =====================================================
            # BARRA COMPRADORA
            # =====================================================
            candle = hist_radar.iloc[-1]

            amplitude = candle["High"] - candle["Low"]

            if amplitude > 0:

                barra_compradora = round(
                    (
                        (candle["Close"] - candle["Low"]) /
                        amplitude
                    ) * 100,
                    2
                )

            else:

                barra_compradora = 0

            # =====================================================
            # SCORE RADAR
            # =====================================================
            score_radar = round(
                (
                    min(volume_ratio, 3) * 2
                ) +
                (
                    3 if ema9 > ema21 else 0
                ) +
                (
                    3 if barra_compradora >= 70 else 0
                ),
                2
            )

            radar_lista.append(
                {
                    "Ticker": ticker_radar,
                    "Volume Relativo": round(
                        volume_ratio,
                        2
                    ),
                    "Momentum": momentum,
                    "Barra Compradora %": barra_compradora,
                    "Classificação": row.get(
                        "Classificação",
                        "N/A"
                    ),
                    "Score Radar": score_radar
                }
            )

        except Exception:
            continue

    if radar_lista:

        df_radar = pd.DataFrame(
            radar_lista
        ).sort_values(
            "Score Radar",
            ascending=False
        )

        st.dataframe(
            df_radar,
            use_container_width=True,
            height=420
        )

    else:

        st.warning(
            "Sem dados disponíveis no momento."
        )
# =========================================================
# SEMÁFORO OPERACIONAL
# =========================================================
st.subheader("Semáforo Operacional")

if prob_compra >= 70 and score_fluxo >= 6 and score_macro >= 6:
    semaforo = "🟢 Entrada Favorável"
    semaforo_msg = "Convergência entre técnico, fluxo e macro."
elif prob_compra >= 55:
    semaforo = "🟡 Aguardar Confirmação"
    semaforo_msg = "Viés positivo, porém sem alinhamento completo."
else:
    semaforo = "🔴 Risco Elevado"
    semaforo_msg = "Baixa vantagem estatística no momento."

st.info(f"{semaforo} | {semaforo_msg}")
# =========================================================
# PREÇO-ALVO INSTITUCIONAL
# =========================================================
st.subheader("Preço-Alvo Institucional")

# ATR
hist["H-L"] = hist["High"] - hist["Low"]
hist["H-PC"] = abs(hist["High"] - hist["Close"].shift(1))
hist["L-PC"] = abs(hist["Low"] - hist["Close"].shift(1))

hist["TR"] = hist[
    ["H-L", "H-PC", "L-PC"]
].max(axis=1)

atr = hist["TR"].rolling(14).mean().iloc[-1]

preco_atual = hist["Close"].iloc[-1]

# Multiplicadores dinâmicos
fator_score = max(row["Score"], 1) / 10
fator_prob = prob_compra / 100

alvo_30 = preco_atual + (
    atr * 8 * fator_score * fator_prob
)

alvo_60 = preco_atual + (
    atr * 16 * fator_score * fator_prob
)

stop_tecnico = preco_atual - (atr * 2)

risco = preco_atual - stop_tecnico
retorno_30 = alvo_30 - preco_atual

if risco > 0:
    rr_30 = retorno_30 / risco
else:
    rr_30 = 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Preço Atual",
        round(preco_atual, 2)
    )

with col2:
    st.metric(
        "Alvo 30D",
        round(alvo_30, 2)
    )

with col3:
    st.metric(
        "Alvo 60D",
        round(alvo_60, 2)
    )

with col4:
    st.metric(
        "Stop Técnico",
        round(stop_tecnico, 2)
    )

st.write(
    f"**Risco/Retorno 30D:** {round(rr_30,2)}"
)
# =========================================================
# CATALISADORES INSTITUCIONAIS
# =========================================================
st.subheader("Catalisadores Institucionais")

pontos_positivos = []
pontos_risco = []

# =========================================================
# FUNDAMENTOS
# =========================================================
if pd.notna(row.get("returnOnEquity")):

    if row["returnOnEquity"] > 0.15:
        pontos_positivos.append("📈 ROE robusto")

    elif row["returnOnEquity"] < 0.08:
        pontos_risco.append("⚠ ROE fraco")


if pd.notna(row.get("revenueGrowth")):

    if row["revenueGrowth"] > 0.10:
        pontos_positivos.append("🚀 Crescimento de receita")

    elif row["revenueGrowth"] < 0:
        pontos_risco.append("⚠ Receita em retração")


if pd.notna(row.get("dividendYield")):

    if row["dividendYield"] > 0.06:
        pontos_positivos.append("💰 Dividend yield atrativo")


if pd.notna(row.get("debtToEquity")):

    if row["debtToEquity"] > 150:
        pontos_risco.append("⚠ Endividamento elevado")


if pd.notna(row.get("trailingPE")):

    if row["trailingPE"] > 18:
        pontos_risco.append("⚠ Valuation esticado")


# =========================================================
# TÉCNICO / FLUXO
# =========================================================
if prob_compra >= 70:
    pontos_positivos.append("📊 Força técnica compradora")

elif prob_compra < 45:
    pontos_risco.append("⚠ Pressão técnica vendedora")


if score_fluxo >= 6:
    pontos_positivos.append("🏦 Fluxo institucional positivo")

else:
    pontos_risco.append("⚠ Fluxo sem convicção")


# =========================================================
# MACRO
# =========================================================
if score_macro >= 7:
    pontos_positivos.append("🌍 Ambiente macro favorável")

elif score_macro <= 4:
    pontos_risco.append("⚠ Macro pressionado")


# Fallback
if not pontos_positivos:
    pontos_positivos.append("🔎 Sem catalisador positivo dominante")

if not pontos_risco:
    pontos_risco.append("🔎 Sem risco crítico dominante")


# =========================================================
# EXIBIÇÃO
# =========================================================
col1, col2 = st.columns(2)

with col1:

    st.write("### Vetores Positivos")

    for item in pontos_positivos:

        st.markdown(
            f"""
            <div style="
                padding:8px;
                margin-bottom:6px;
                border-radius:8px;
                background:rgba(34,197,94,0.12);
                border:1px solid rgba(34,197,94,0.25);
            ">
                {item}
            </div>
            """,
            unsafe_allow_html=True
        )

with col2:

    st.write("### Vetores de Risco")

    for item in pontos_risco:

        st.markdown(
            f"""
            <div style="
                padding:8px;
                margin-bottom:6px;
                border-radius:8px;
                background:rgba(239,68,68,0.10);
                border:1px solid rgba(239,68,68,0.25);
            ">
                {item}
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================================
# BARRA
# =========================================================
barra_html = f"""
<div style="
    width:100%;
    display:flex;
    justify-content:center;
    align-items:center;
    padding:8px 0;
">

    <div style="
        display:flex;
        align-items:center;
        justify-content:center;
        width:50px;
        font-size:26px;
    ">
        🐂
    </div>

    <div style="
        width:75%;
        max-width:750px;
        height:36px;
        display:flex;
        border-radius:12px;
        overflow:hidden;
        border:1px solid rgba(255,255,255,0.35);
        background:rgba(255,255,255,0.08);
    ">

        <div style="
            width:{prob_compra}%;
            background:#16a34a;
            display:flex;
            justify-content:center;
            align-items:center;
            color:white;
            font-weight:bold;
            font-size:15px;
            height:100%;
        ">
            {prob_compra}%
        </div>

        <div style="
            width:{prob_venda}%;
            background:#dc2626;
            display:flex;
            justify-content:center;
            align-items:center;
            color:white;
            font-weight:bold;
            font-size:15px;
            height:100%;
        ">
            {prob_venda}%
        </div>

    </div>

    <div style="
        display:flex;
        align-items:center;
        justify-content:center;
        width:50px;
        font-size:26px;
    ">
        🐻
    </div>

</div>
"""
components.html(
    barra_html,
    height=95
)

# =========================================================
# RANKING
# =========================================================
st.subheader("Ranking Geral")

itens_por_pagina = 10

if "pagina_ranking" not in st.session_state:
    st.session_state.pagina_ranking = 1

total_paginas = math.ceil(
    len(df_filtrado) / itens_por_pagina
)

inicio = (
    (st.session_state.pagina_ranking - 1)
    * itens_por_pagina
)

fim = inicio + itens_por_pagina

df_pagina = df_filtrado.iloc[inicio:fim].copy()

if "Empresa" not in df_pagina.columns:
    df_pagina["Empresa"] = df_pagina["longName"]

colunas_exibir = [
    "Empresa",
    "Ticker",
    "currentPrice",
    "Score",
    "Classificação",
    "Preço Justo",
    "Upside %"
]

def colorir_classificacao(val):

    if val == "Compra Forte":
        return "background-color: rgba(34,197,94,0.35); color:white;"

    elif val == "Compra":
        return "background-color: rgba(59,130,246,0.35); color:white;"

    elif val == "Neutro":
        return "background-color: rgba(234,179,8,0.35); color:white;"

    elif val == "Atenção":
        return "background-color: rgba(239,68,68,0.35); color:white;"

    return ""

df_style = (
    df_pagina[colunas_exibir]
    .style
    .map(
        colorir_classificacao,
        subset=["Classificação"]
    )
)

# =========================================================
# HEATMAP RANKING GERAL
# =========================================================
def colorir_upside(val):

    try:

        if val >= 20:
            return "background-color: rgba(34,197,94,0.45); color:white;"

        elif val >= 10:
            return "background-color: rgba(132,204,22,0.35); color:white;"

        elif val >= 0:
            return "background-color: rgba(250,204,21,0.25); color:white;"

        else:
            return "background-color: rgba(239,68,68,0.35); color:white;"

    except:
        return ""


def colorir_score(val):

    try:

        if val >= 7:
            return "background-color: rgba(34,197,94,0.40); color:white;"

        elif val >= 5:
            return "background-color: rgba(132,204,22,0.30); color:white;"

        elif val >= 3:
            return "background-color: rgba(250,204,21,0.25); color:white;"

        else:
            return "background-color: rgba(239,68,68,0.30); color:white;"

    except:
        return ""


styled_df = (
    df_pagina[colunas_exibir]
    .style
    .map(colorir_upside, subset=["Upside %"])
    .map(colorir_score, subset=["Score"])
)

st.dataframe(
    styled_df,
    use_container_width=True,
    height=420
)

# =========================================================
# NAVEGAÇÃO
# =========================================================
col1, col2, col3 = st.columns([1,2,1])

with col1:

    if st.button("⬅ Página anterior"):

        if st.session_state.pagina_ranking > 1:
            st.session_state.pagina_ranking -= 1

with col2:

    st.markdown(
        f"""
        <div style='text-align:center;
                    font-size:18px;
                    font-weight:bold;'>

        Página {st.session_state.pagina_ranking}
        de {total_paginas}

        </div>
        """,
        unsafe_allow_html=True
    )

with col3:

    if st.button("Próxima página ➡"):

        if (
            st.session_state.pagina_ranking
            < total_paginas
        ):
            st.session_state.pagina_ranking += 1

# =========================================================
# 🏦 RANKING AÇÕES MAIORES DIVIDENDOS
# =========================================================
st.markdown("---")
titulo_secao(
    "ranking-dividendos",
    "🏦 Ranking Ações Maiores Dividendos"
)

with st.expander("📊 Exibir Ranking de Dividendos"):

    dividendos_lista = []

    for _, row in df.iterrows():

        ticker_div = row["Ticker"]

        try:

            ativo_div = yf.Ticker(f"{ticker_div}.SA")

            dividendos = ativo_div.dividends

            if dividendos.empty:
                continue

            ultimo_ano = dividendos[
                dividendos.index >= (
                    pd.Timestamp.now() - pd.DateOffset(months=12)
                )
            ]

            if ultimo_ano.empty:
                continue

            dividendo_anual = round(
                float(ultimo_ano.sum()),
                4
            )

            data_com = dividendos.index[-1].strftime(
                "%d/%m/%Y"
            )

            pagamentos = []

            for data_pgto, valor_pgto in ultimo_ano.items():

                pagamentos.append(
                    f"{data_pgto.strftime('%b')}: {valor_pgto:.2f}"
                )

            meses_pagamento = " | ".join(
                pagamentos
            )

            try:
                setor = ativo_div.info.get(
                    "sector",
                    "N/A"
                )
            except:
                setor = "N/A"

            dividendos_lista.append(
                {
                    "Ticker": ticker_div,
                    "Data Com": data_com,
                    "Dividendos Anuais": dividendo_anual,
                    "Meses Pagamento": meses_pagamento,
                    "Setor": setor
                }
            )

        except:
            continue

    # =====================================================
    # DATAFRAME FINAL
    # =====================================================
    if dividendos_lista:

        df_dividendos = pd.DataFrame(
            dividendos_lista
        ).sort_values(
            "Dividendos Anuais",
            ascending=False
        )

        itens_por_pagina_div = 10

        if "pagina_dividendos" not in st.session_state:
            st.session_state.pagina_dividendos = 1

        total_paginas_div = math.ceil(
            len(df_dividendos) / itens_por_pagina_div
        )

        inicio_div = (
            (st.session_state.pagina_dividendos - 1)
            * itens_por_pagina_div
        )

        fim_div = inicio_div + itens_por_pagina_div

        st.dataframe(
            df_dividendos.iloc[inicio_div:fim_div],
            use_container_width=True,
            height=420
        )

        # =================================================
        # PAGINAÇÃO
        # =================================================
        col1, col2, col3 = st.columns([1,2,1])

        with col1:

            if st.button(
                "⬅ Dividendos",
                key="div_prev"
            ):

                if st.session_state.pagina_dividendos > 1:
                    st.session_state.pagina_dividendos -= 1

        with col2:

            st.markdown(
                f"""
                <div style='text-align:center;
                            font-size:18px;
                            font-weight:bold;'>

                Página {st.session_state.pagina_dividendos}
                de {total_paginas_div}

                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:

            if st.button(
                "Dividendos ➡",
                key="div_next"
            ):

                if (
                    st.session_state.pagina_dividendos
                    < total_paginas_div
                ):
                    st.session_state.pagina_dividendos += 1

    else:

        st.warning(
            "Nenhum dividendo encontrado via fonte atual."
        )
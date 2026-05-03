import streamlit as st
import pandas as pd
from data import get_data
from scoring import calcular_score, classificar

# Configuração da página
st.set_page_config(
    page_title="Alcides Alpha V1",
    layout="wide"
)

# Título
st.title("ALCIDES ALPHA – Institutional Equity Intelligence")
st.subheader("Ranking B3 | Atualização automática | Score institucional")

# Cache de 5 minutos
@st.cache_data(ttl=300)
def carregar_dados():
    df = get_data()

    # Score
    df["Score"] = df.apply(calcular_score, axis=1)
    df["Classificação"] = df["Score"].apply(classificar)

    # Fair Value simples
    df["Preço Justo Est."] = df["Preço"] * (1 + (df["Score"] * 0.05))

    # Upside %
    df["Upside %"] = ((df["Preço Justo Est."] - df["Preço"]) / df["Preço"]) * 100

    # Ordenar por Score
    df = df.sort_values(by="Score", ascending=False)

    return df

# Carregar dados
df = carregar_dados()

# Métricas topo
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Ações analisadas", len(df))

with col2:
    melhor = df.iloc[0]["Ticker"]
    st.metric("Top Score", melhor)

with col3:
    media_score = round(df["Score"].mean(), 2)
    st.metric("Score Médio", media_score)

# Tabela principal
st.dataframe(
    df,
    use_container_width=True
)

# Consulta individual
st.subheader("Consulta individual")

ticker_escolhido = st.selectbox(
    "Selecione o ticker:",
    df["Ticker"]
)

linha = df[df["Ticker"] == ticker_escolhido].iloc[0]

st.write(f"### {ticker_escolhido}")
st.write(f"**Preço Atual:** {linha['Preço']}")
st.write(f"**Score:** {linha['Score']}")
st.write(f"**Classificação:** {linha['Classificação']}")
st.write(f"**Preço Justo Estimado:** {round(linha['Preço Justo Est.'], 2)}")
st.write(f"**Upside Potencial:** {round(linha['Upside %'], 2)}%")
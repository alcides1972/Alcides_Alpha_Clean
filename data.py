import streamlit as st
import yfinance as yf
import pandas as pd


@st.cache_data(ttl=1800)
def get_data():

    # =========================================================
    # UNIVERSO B3
    # =========================================================
    tickers = [

        "ITUB4", "BBDC4", "BBAS3", "SANB11", "BPAC11",

        "PETR4", "VALE3", "PRIO3", "SUZB3", "CSNA3",
        "GGBR4", "USIM5", "BRAP4",

        "ABEV3", "LREN3", "VULC3", "ASAI3", "PETZ3",

        "WEGE3", "ELET3", "TAEE11", "CMIG4",
        "CPFE3", "EQTL3", "UGPA3",

        "CYRE3", "EZTC3", "DIRR3", "CURY3",

        "HAPV3", "RDOR3", "RADL3", "FLRY3",

        "RAIL3", "RENT3", "CCRO3",

        "TOTS3", "POSI3",

        "VIVT3", "TIMS3",

        "JBSS3", "BRFS3", "MRFG3", "SMTO3",

        "YDUQ3", "COGN3", "DXCO3", "EMBR3", "MULT3"
    ]

    dados = []

    # =========================================================
    # COLETA PRINCIPAL
    # =========================================================
    for ticker in tickers:

        try:

            ativo = yf.Ticker(
                f"{ticker}.SA"
            )

            hist = ativo.history(
                period="5d"
            )

            if hist.empty:
                continue

            preco_series = hist["Close"].dropna()

            if preco_series.empty:
                continue

            preco_atual = float(
                preco_series.iloc[-1]
            )

            try:
                info = ativo.info
            except Exception:
                info = {}

            dados.append(
                {
                    "Ticker": ticker,
                    "longName": info.get(
                        "longName",
                        ticker
                    ),
                    "currentPrice": preco_atual,
                    "marketCap": info.get(
                        "marketCap",
                        0
                    ),
                    "trailingPE": info.get(
                        "trailingPE",
                        None
                    ),
                    "priceToBook": info.get(
                        "priceToBook",
                        None
                    ),
                    "returnOnEquity": info.get(
                        "returnOnEquity",
                        None
                    ),
                    "debtToEquity": info.get(
                        "debtToEquity",
                        None
                    ),
                    "dividendYield": info.get(
                        "dividendYield",
                        None
                    ),
                    "revenueGrowth": info.get(
                        "revenueGrowth",
                        None
                    ),
                    "profitMargins": info.get(
                        "profitMargins",
                        None
                    ),
                }
            )

        except Exception:
            continue

    # =========================================================
    # DATAFRAME
    # =========================================================
    df = pd.DataFrame(
        dados
    )

    if df.empty:
        return pd.DataFrame()

    # =========================================================
    # CAMPOS NUMÉRICOS
    # =========================================================
    campos_numericos = [
        "currentPrice",
        "marketCap",
        "trailingPE",
        "priceToBook",
        "returnOnEquity",
        "debtToEquity",
        "dividendYield",
        "revenueGrowth",
        "profitMargins"
    ]

    for col in campos_numericos:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    # =========================================================
    # FILTRO PREÇO VÁLIDO
    # =========================================================
    df = df[
        df["currentPrice"].notna()
    ]

    df = df[
        df["currentPrice"] > 0
    ]

    if df.empty:
        return pd.DataFrame()

    # =========================================================
    # ORDENAÇÃO
    # =========================================================
    if "marketCap" in df.columns:

        df = df.sort_values(
            by="marketCap",
            ascending=False
        )

    return df
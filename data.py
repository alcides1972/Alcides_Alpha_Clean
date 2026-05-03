import yfinance as yf
import pandas as pd

# Lista inicial de ações B3
TICKERS = [
    "ITUB4.SA",
    "BBDC4.SA",
    "BBAS3.SA",
    "PETR4.SA",
    "VALE3.SA",
    "WEGE3.SA",
    "RENT3.SA",
    "VULC3.SA",
    "CURY3.SA"
]

def get_data():
    dados = []

    for ticker in TICKERS:
        try:
            acao = yf.Ticker(ticker)
            info = acao.info

            dados.append({
                "Ticker": ticker.replace(".SA", ""),
                "Preço": info.get("currentPrice", None),
                "P/L": info.get("trailingPE", None),
                "P/VP": info.get("priceToBook", None),
                "ROE": info.get("returnOnEquity", None),
                "Dividend Yield": info.get("dividendYield", None)
            })

        except Exception:
            dados.append({
                "Ticker": ticker.replace(".SA", ""),
                "Preço": None,
                "P/L": None,
                "P/VP": None,
                "ROE": None,
                "Dividend Yield": None
            })

    return pd.DataFrame(dados)
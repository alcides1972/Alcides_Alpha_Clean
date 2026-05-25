import pandas as pd

def calcular_score(row):

    score = 0

    trailing_pe = row.get("trailingPE")
    price_to_book = row.get("priceToBook")
    roe = row.get("returnOnEquity")
    dividend_yield = row.get("dividendYield")

    # P/L
    if pd.notna(trailing_pe) and trailing_pe > 0:
        if trailing_pe < 10:
            score += 2
        elif trailing_pe < 15:
            score += 1

    # P/VP
    if pd.notna(price_to_book) and price_to_book > 0:
        if price_to_book < 1.5:
            score += 2
        elif price_to_book < 3:
            score += 1

    # ROE
    if pd.notna(roe):
        if roe > 0.20:
            score += 2
        elif roe > 0.10:
            score += 1

    # Dividend Yield
    if pd.notna(dividend_yield):
        if dividend_yield > 0.08:
            score += 2
        elif dividend_yield > 0.04:
            score += 1

    return score


def classificar(score):

    if score >= 7:
        return "Compra Forte"

    elif score >= 5:
        return "Compra"

    elif score >= 3:
        return "Neutro"

    return "Atenção"
def calcular_score(row):
    score = 0

    # P/L
    if row["P/L"] is not None:
        if row["P/L"] < 10:
            score += 2
        elif row["P/L"] < 15:
            score += 1

    # P/VP
    if row["P/VP"] is not None:
        if row["P/VP"] < 1.5:
            score += 2
        elif row["P/VP"] < 3:
            score += 1

    # ROE
    if row["ROE"] is not None:
        if row["ROE"] > 0.20:
            score += 2
        elif row["ROE"] > 0.10:
            score += 1

    # Dividend Yield
    if row["Dividend Yield"] is not None:
        if row["Dividend Yield"] > 0.08:
            score += 2
        elif row["Dividend Yield"] > 0.04:
            score += 1

    return score


def classificar(score):
    if score >= 7:
        return "Compra Forte"
    elif score >= 5:
        return "Compra"
    elif score >= 3:
        return "Neutro"
    else:
        return "Atenção"
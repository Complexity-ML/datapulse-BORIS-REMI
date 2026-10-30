import pandas as pd


def revenue_by_region(df: pd.DataFrame) -> pd.Series:
    """Chiffre d'affaires par region, du plus eleve au plus faible."""
    result = df.groupby("region")["montant"].sum()
    return result.round(2).sort_values(ascending=False)


def total_revenue(df: pd.DataFrame) -> float:
    """Chiffre d'affaires total."""
    return round(float(df["montant"].sum()), 2)

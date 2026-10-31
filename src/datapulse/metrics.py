import os
import pandas as pd


def revenue_by_region(df: pd.DataFrame) -> pd.Series:
    """Chiffre d'affaires par region, du plus eleve au plus faible."""
    result = df.groupby("region")["montant"].sum()
    return result.round(2).sort_values(ascending=False)


def total_revenue(df: pd.DataFrame) -> float:
    """Chiffre d'affaires total."""
    return round(float(df["montant"].sum()), 2)


def average_basket(df: pd.DataFrame) -> pd.Series:
    """Panier moyen par region."""
    result = df.groupby("region")["montant"].mean()
    return result.round(2).sort_values(ascending=False)


def sales_by_category(df: pd.DataFrame) -> pd.Series:
    """Nombre de ventes par categorie, du plus vendu au moins vendu."""
    return df.groupby("categorie").size().sort_values(ascending=False)
import pandas as pd

from datapulse.metrics import revenue_by_region, total_revenue


def df_exemple():
    return pd.DataFrame({
        "region": ["Occitanie", "Occitanie", "Bretagne"],
        "montant": [100.0, 50.0, 80.0],
        "categorie": ["Electromenager", "Informatique", "Informatique"],
    })


def test_revenue_by_region():
    result = revenue_by_region(df_exemple())
    assert result["Occitanie"] == 150.0
    assert result["Bretagne"] == 80.0


def test_total_revenue():
    assert total_revenue(df_exemple()) == 230.0

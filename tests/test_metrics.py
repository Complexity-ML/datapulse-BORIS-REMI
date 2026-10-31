import pandas as pd
import pytest

from datapulse.metrics import (
    revenue_by_region,
    revenue_share_by_category,
    total_revenue,
)


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


def test_average_basket():
    from datapulse.metrics import average_basket
    result = average_basket(df_exemple())
    assert result["Occitanie"] == 75.0


def test_sales_by_category():
    from datapulse.metrics import sales_by_category
    result = sales_by_category(df_exemple())
    assert result["Informatique"] == 2
    assert result["Electromenager"] == 1

    

def test_sales_by_region():
    from datapulse.metrics import sales_by_region
    result = sales_by_region(df_exemple())
    assert result["Occitanie"] == 2
    assert result["Bretagne"] == 1


def test_revenue_share_by_category():
    df = df_exemple()
    original = df.copy(deep=True)

    result = revenue_share_by_category(df)

    expected = pd.Series(
        [56.52, 43.48],
        index=pd.Index(["Informatique", "Electromenager"], name="categorie"),
        name="montant",
    )
    pd.testing.assert_series_equal(result, expected)
    pd.testing.assert_frame_equal(df, original)


@pytest.mark.parametrize("amounts", [[0.0, 0.0], [100.0, -100.0]])
def test_revenue_share_by_category_zero_total(amounts):
    df = pd.DataFrame({"categorie": ["A", "B"], "montant": amounts})

    with pytest.raises(ValueError, match="chiffre d'affaires total est nul"):
        revenue_share_by_category(df)


def test_revenue_share_by_category_empty():
    result = revenue_share_by_category(df_exemple().iloc[:0])

    assert result.empty
    assert result.index.name == "categorie"
    assert result.name == "montant"
    assert result.dtype == float


def test_revenue_share_by_category_excludes_missing_categories():
    df = pd.DataFrame({
        "categorie": ["A", "B", None],
        "montant": [60.0, 40.0, 900.0],
    })

    result = revenue_share_by_category(df)

    assert result.to_dict() == {"A": 60.0, "B": 40.0}
    assert result.sum() == 100.0


def test_revenue_share_by_category_without_categories():
    df = pd.DataFrame({"categorie": [None], "montant": [100.0]})

    assert revenue_share_by_category(df).empty


def test_revenue_share_by_category_includes_refunds():
    df = pd.DataFrame({
        "categorie": ["A", "A", "B"],
        "montant": [120.0, -20.0, -20.0],
    })

    result = revenue_share_by_category(df)

    assert result.to_dict() == {"A": 125.0, "B": -25.0}

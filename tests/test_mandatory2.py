import pytest
from src.analysis.homemade.mandatory2 import ranking_nopd


@pytest.mark.parametrize("year", [2021, 2022, 2023])
def test_ranking_contains_rank_header(year):
    result = ranking_nopd(year)
    assert isinstance(result, str)
    assert "Rank" in result
    assert f"Season {year}" in result

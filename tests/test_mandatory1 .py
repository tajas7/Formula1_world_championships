import pytest
from src.analysis.homemade.mandatory1 import at_least_n_races_nopd


@pytest.mark.parametrize("n", [20, 30, 50])
def test_at_least_n_races_nopd_title(n):
    result = at_least_n_races_nopd(n)
    assert f"Drivers who won more than {n} races" in result

import pytest
from src.analysis.pandas.q5_graph import most_constructor_championships_won
from src.analysis.pandas.q6_graph import nationalities


@pytest.mark.parametrize("func, filename", [
    (most_constructor_championships_won, "test_championships.png"),
    (nationalities, "test_nationalities.png"),
])
def test_graph_generation_and_save(tmp_path, func, filename):
    path = tmp_path / filename
    func(save_path=str(path))

    assert path.exists()
    assert path.stat().st_size > 0

import pytest

collect_ignore = ["test_offseason_e2e.py"]

@pytest.fixture
def season_id():
    return 1

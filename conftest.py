import pytest

from src import store


@pytest.fixture(scope="function")
def clear_storage():
    yield
    store.clear()

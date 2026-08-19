# TODO: Validate
from __future__ import annotations

import pytest
from get_around import get_credential

from wampi import Wampi

pytest.register_assert_rewrite("tests.utils")


@pytest.fixture(scope="session")
def client() -> Wampi:
    return Wampi(get_credential("WATCHMODE_API_KEY"))

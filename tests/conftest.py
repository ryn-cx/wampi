# TODO: Validate
import pytest
from get_around import get_credential

from wampi import Wampi
from wampi.constants import API_KEY_CREDENTIAL


@pytest.fixture(scope="session")
def client() -> Wampi:
    return Wampi(get_credential(API_KEY_CREDENTIAL))

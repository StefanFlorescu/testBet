"""Fixture smoke tests without network requests."""

import pytest
import schemathesis
from schemathesis.specs.openapi.checks import unsupported_method

from src.logger import get_logger
from src.config import settings


pytestmark = [pytest.mark.api, pytest.mark.schema]
logger = get_logger("test_schema")
schema = schemathesis.openapi.from_url(settings.api_documentation_url.encoded_string())

@pytest.mark.skip
@schema.parametrize()
def test_api_contract(case):
    case.call_and_validate(
        headers={"x-user-id": settings.user_id},
        excluded_checks=[unsupported_method],
    )

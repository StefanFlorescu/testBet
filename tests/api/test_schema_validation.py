"""Fixture smoke tests without network requests."""

import pytest
import schemathesis
import hypothesis
from src.logger import get_logger
from src.config import settings


pytestmark = [pytest.mark.api, pytest.mark.schema]
logger = get_logger("test_schema")
schema = schemathesis.openapi.from_url(settings.api_documentation_url.encoded_string())

@schema.parametrize()
@hypothesis.settings(max_examples=500)
def test_api_contract(case):
    # response = case.call(
    #     headers={"x-user-id": settings.user_id, "Accept": "application/json", "Content-Type": "application/json"},
    # )
    case.call_and_validate(headers={"x-user-id": settings.user_id})

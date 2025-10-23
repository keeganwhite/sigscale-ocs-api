"""
Pytest configuration and fixtures for integration tests.
"""

import os
import pytest
from sigscale_ocs import OCSClient


@pytest.fixture
def client():
    """
    Create OCS client for testing.

    Requires test credentials in environment variables:
    - SIGSCALE_OCS_URL
    - SIGSCALE_OCS_USERNAME
    - SIGSCALE_OCS_PASSWORD
    - SIGSCALE_OCS_VERIFY_SSL (optional, defaults to true)
    """
    base_url = os.getenv("SIGSCALE_OCS_URL")
    username = os.getenv("SIGSCALE_OCS_USERNAME")
    password = os.getenv("SIGSCALE_OCS_PASSWORD")
    verify_ssl = os.getenv("SIGSCALE_OCS_VERIFY_SSL", "true").lower() == "true"

    if not all([base_url, username, password]):
        pytest.skip(
            "Test credentials not available. Set SIGSCALE_OCS_URL, "
            "SIGSCALE_OCS_USERNAME, and SIGSCALE_OCS_PASSWORD environment variables."
        )

    client = OCSClient(
        base_url=base_url, username=username, password=password, verify_ssl=verify_ssl
    )

    yield client
    client.close()


@pytest.fixture
def test_offering_id(client):
    """Get a real offering ID for testing."""
    from sigscale_ocs import ProductCatalog

    catalog = ProductCatalog(client)
    offerings = catalog.list_offerings()
    if offerings:
        return offerings[0].get("id")
    return None


@pytest.fixture
def test_product_id(client):
    """Get a real product ID for testing."""
    from sigscale_ocs import ProductInventory

    inventory = ProductInventory(client)
    products = inventory.list_products()
    if products:
        return products[0].get("id")
    return None

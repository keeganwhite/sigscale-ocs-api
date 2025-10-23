# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-10-23

### Added

- Initial release of sigscale-ocs-api Python wrapper
- **OCSClient** - Base client with authentication, HTTP methods, and error handling
- **BalanceManagement** (TMF654) - Balance top-ups and bucket operations
  - `create_adjustment()` - Add credits to user accounts
  - `list_buckets()` - Get balance buckets for products
  - `get_bucket()` - Get individual bucket details
  - `format_balance_amount()` - Format amounts for display (e.g., "1000000000b octets" → "953.67 MB")
- **ProductCatalog** (TMF620) - Product offering management
  - `list_offerings()` - List available product offerings
  - `create_offering()` - Create new offerings (may have request format limitations)
  - `delete_offering()` - Delete offerings
  - `list_catalogs()` - List catalogs
  - `list_categories()` - List categories
  - `list_product_specifications()` - List product specifications
- **ProductInventory** (TMF637) - Product subscription management
  - `list_products()` - List product subscriptions
  - `get_product()` - Get subscription details
  - `create_product()` - Create subscriptions (data purchase)
  - `delete_product()` - Delete subscriptions
- **ServiceInventory** (TMF638) - Subscriber/service management
  - `list_services()` - List subscribers/services
  - `get_service()` - Get subscriber details
  - `create_service()` - Add subscribers (SIM card signup)
  - `delete_service()` - Remove subscribers
- **Custom Exception Classes** - Specific error handling
  - `OCSAPIError` - Base API error
  - `AuthenticationError` - 401 Unauthorized
  - `BadRequestError` - 400 Bad Request
  - `NotFoundError` - 404 Not Found
  - `ServerError` - 5xx Server errors
- **Data Models** - Type-safe dataclasses for API entities
  - `ProductOffering`, `Product`, `Service`, `Bucket`, `BalanceAdjustment`
  - `Amount`, `ValidFor`, `ProductRef` for complex nested structures
- **Configuration** - Environment variable support
  - `.env` file support for API credentials
  - SSL verification control for self-signed certificates
- **Integration Tests** - Comprehensive test suite
  - Tests for all core functionality (SIM card creation, data purchase, balance top-up)
  - Real API integration tests with cleanup
  - Fixtures for dynamic test data
- **Examples** - Working code examples
  - `core_example.py` - Essential operations with cleanup
- **Documentation** - Comprehensive README with API reference
- **CI/CD Pipeline** - GitHub Actions workflow for testing and publishing

### Core Use Cases Supported

- **User Signup** - Add subscribers/services for SIM cards
- **Data Purchase** - Create product subscriptions
- **Balance Top-Up** - Add credits/data to user accounts
- **Offering Management** - Admin creates/manages product offerings

### Technical Features

- Modern Python package structure with `pyproject.toml`
- Type hints and dataclasses for type safety
- Session management with connection pooling
- Retry logic for failed requests
- Comprehensive error handling
- Clean API design with focused functionality

### Dependencies

- `requests>=2.25.1` - HTTP client
- `python-dotenv>=0.19.0` - Environment variable loading

### Development Dependencies

- `pytest>=6.2.4` - Testing framework
- `pytest-cov>=2.12.1` - Test coverage
- `flake8>=3.9.2` - Code linting
- `black>=21.5b2` - Code formatting
- `mypy>=0.910` - Type checking
- `build>=0.7.0` - Package building
- `twine>=3.4.1` - PyPI uploading

# Port Cleaner

A Python tool for cleaning Port blueprints by removing entities within a specified date range. This tool helps manage and maintain your Port.io workspace by allowing you to selectively remove entities based on their update timestamps.

## Features

- 🔍 Search and delete entities within a specific date range
- 🔐 Secure authentication with Port.io API
- ⚡ Asynchronous operations for better performance
- 🛡️ Configurable deletion options
- 📦 Modular and maintainable codebase

## Prerequisites

- Python 3.8 or higher
- Port.io account with API credentials
- Access to the Port.io API

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd port-cleaner
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The tool requires the following configuration parameters:

| Parameter | Description | Required |
|-----------|-------------|----------|
| `client-id` | Your Port.io client ID | Yes |
| `client-secret` | Your Port.io client secret | Yes |
| `api-url` | Port.io API URL (default: https://api.getport.io/v1) | No |
| `integration-identifier` | Your integration identifier | Yes |
| `integration-type` | Type of integration (e.g., gitlab, github) | Yes |
| `from-date` | Start date in ISO format | Yes |
| `to-date` | End date in ISO format | Yes |
| `blueprint-identifiers` | List of blueprint identifiers to clean | Yes |

## Usage

### Basic Usage

```bash
python main.py \
  --client-id YOUR_CLIENT_ID \
  --client-secret YOUR_CLIENT_SECRET \
  --api-url https://api.getport.io/v1 \
  --integration-identifier YOUR_INTEGRATION_ID \
  --integration-type YOUR_INTEGRATION_TYPE \
  --from-date 2025-05-13T00:00:00.000Z \
  --to-date 2025-05-13T23:59:59.999Z \
  --blueprint-identifiers blueprint1 blueprint2
```

### Example with GitLab Integration

```bash
python main.py \
  --client-id 9BSlEex5gW8JRt5OwB03f7W5fxtiduCF \
  --client-secret ZEUtwlXHZ1ggRJdDi89NCiaJkpyseY7C3lx5IehjtwN4lbcmN377K9AhCTLut6fD \
  --api-url https://api.getport.io/v1 \
  --integration-identifier my-gitlab-integration \
  --integration-type gitlab \
  --from-date 2025-05-13T00:00:00.000Z \
  --to-date 2025-05-13T23:59:59.999Z \
  --blueprint-identifiers service
```

## Project Structure

```
port_cleaner/
├── core/           # Core functionality
│   ├── auth.py     # Authentication and token management
│   ├── cleaner.py  # Main cleaner class implementation
│   └── entities.py # Entity management and operations
├── utils/          # Utility functions
│   └── helpers.py  # Helper functions and utilities
|   └── models.py   # Data models and schemas
├── config/         # Configuration management
│   └── settings.py # Configuration settings and defaults
└── tests/          # Test files
```

## Development

### Setting Up Development Environment

1. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. Run tests:
   ```bash
   pytest
   ```

### Code Style

The project follows PEP 8 style guidelines. To check your code style:

```bash
flake8 port_cleaner tests
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Security

- Never commit your Port.io credentials to version control
- Use environment variables or secure secret management for sensitive data
- Keep your dependencies up to date

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers. 

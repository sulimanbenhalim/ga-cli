# Contributing to ga-cli

Thank you for your interest in contributing to ga-cli! This document provides guidelines for contributing to the project.

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip and virtualenv
- Google Cloud service account with Analytics Admin API access

### Setting Up Your Development Environment

1. Fork and clone the repository:
```bash
git clone https://github.com/sulimanbenhalim/ga-cli.git
cd ga-cli
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e .
pip install -r requirements-dev.txt
```

4. Set up your credentials:
```bash
cp .env.example .env
# Edit .env and add your credentials path
```

## Development Workflow

### Code Style

We use the following tools to maintain code quality:

- **Black** for code formatting
- **Flake8** for linting
- **mypy** for type checking

Before submitting a PR, run:

```bash
# Format code
black ga_cli/ tests/

# Check linting
flake8 ga_cli/ tests/

# Type checking
mypy ga_cli/
```

### Testing

We aim for >80% test coverage. Run tests with:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=ga_cli --cov-report=html --cov-report=term

# Run specific test file
pytest tests/test_validators.py

# Run tests matching pattern
pytest -k "test_account"
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files as `test_<module>.py`
- Use descriptive test names: `test_<function>_<scenario>`
- Use fixtures from `conftest.py` for common test setup
- Mock external API calls

Example:
```python
def test_validate_account_id_with_valid_input():
    """Test validation accepts valid account ID"""
    result = validate_account_id(None, None, "123456")
    assert result == "123456"
```

### Commit Messages

Follow these guidelines for commit messages:

- Keep the summary line concise (max 72 characters)
- Use imperative mood ("Add feature" not "Added feature")
- Reference issues when applicable

Examples:
- `Add input validation for currency codes`
- `Fix credential permission check on Windows`
- `Update README with installation instructions`

## Pull Request Process

1. **Create a feature branch**:
```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes**:
- Write code following our style guidelines
- Add tests for new functionality
- Update documentation as needed

3. **Run tests and checks**:
```bash
pytest
black ga_cli/ tests/ --check
flake8 ga_cli/ tests/
mypy ga_cli/
```

4. **Commit your changes**:
```bash
git add .
git commit -m "Your descriptive commit message"
```

5. **Push to your fork**:
```bash
git push origin feature/your-feature-name
```

6. **Open a Pull Request**:
- Provide a clear description of your changes
- Reference any related issues
- Ensure CI checks pass

## Project Structure

```
ga-cli/
├── ga_cli/
│   ├── __init__.py           # Package version
│   ├── cli.py                # Main CLI entry point
│   ├── auth.py               # Authentication manager
│   ├── config.py             # Configuration management
│   ├── validators.py         # Input validation
│   ├── errors.py             # Error handling
│   ├── logging_config.py     # Logging setup
│   ├── retry.py              # Retry logic
│   ├── decorators.py         # Common decorators
│   ├── output.py             # Output helpers
│   ├── commands/             # Command modules
│   │   ├── accounts.py
│   │   ├── properties.py
│   │   └── datastreams.py
│   └── formatters/           # Output formatters
│       ├── table.py
│       └── json.py
├── tests/                    # Test suite
├── setup.py                  # Package setup
└── requirements*.txt         # Dependencies
```

## Adding New Features

### Adding a New Command

1. Create command module in `ga_cli/commands/`:
```python
import click
from ga_cli.decorators import with_client

@click.group()
def mycommand():
    """Description of command group"""
    pass

@mycommand.command()
@click.pass_context
@with_client
def list(ctx):
    """List resources"""
    client = ctx.obj['client']
    # Implementation
```

2. Register command in `ga_cli/cli.py`:
```python
from ga_cli.commands.mycommand import mycommand
cli.add_command(mycommand)
```

3. Add tests in `tests/test_mycommand.py`

4. Update README.md with usage examples

### Adding Input Validators

Add validators to `ga_cli/validators.py`:

```python
def validate_my_field(ctx, param, value):
    """Validate my field"""
    if value and not meets_criteria(value):
        raise click.BadParameter("Invalid value")
    return value
```

Use in commands:
```python
@click.argument('my_field', callback=validate_my_field)
```

## Reporting Issues

When reporting issues, please include:

- Description of the problem
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python version, ga-cli version)
- Relevant error messages or logs

## Security Issues

Please do not report security vulnerabilities in public issues. Instead, email suliman.benhalim@binary.ly with details.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Assume good intentions

## Questions?

Feel free to open an issue for questions or join our [community channel/forum].

Thank you for contributing to ga-cli!

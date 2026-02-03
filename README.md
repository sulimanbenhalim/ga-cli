# GA CLI - Google Analytics Command Line Interface

A command-line interface tool for managing Google Analytics 4 properties, accounts, and data streams.

## Features

- List and manage Google Analytics accounts
- Create and manage GA4 properties
- Manage data streams and retrieve measurement IDs
- Beautiful table output with Rich
- JSON output support
- Authentication via service account credentials

## Installation

### From source

```bash
cd ga-cli
pip install -e .
```

### Using pip (when published)

```bash
pip install ga-cli
```

## Setup

### 1. Get Google Service Account Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create or select a project
3. Enable the Google Analytics Admin API
4. Create a service account with Analytics Admin permissions
5. Download the JSON credentials file

### 2. Initialize GA CLI

```bash
ga-cli config init
```

This will prompt you for the path to your service account JSON file and test the credentials.

Alternatively, set the environment variable:

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
```

## Usage

### Configuration

```bash
# Initialize with credentials
ga-cli config init

# Show current configuration
ga-cli config show
```

### Accounts

```bash
# List all accounts
ga-cli accounts list

# Get account details
ga-cli accounts get <account-id>

# Output as JSON
ga-cli accounts list --format json
```

### Properties

```bash
# List properties for an account
ga-cli properties list <account-id>

# Get property details
ga-cli properties get <property-id>

# Create a new property
ga-cli properties create <account-id> --name "My Website" --timezone "America/New_York" --currency "USD"

# Delete a property
ga-cli properties delete <property-id>
```

### Data Streams

```bash
# List data streams for a property
ga-cli datastreams list <property-id>

# Get data stream details (including measurement ID)
ga-cli datastreams get <property-id> <stream-id>

# Create a new web data stream
ga-cli datastreams create <property-id> --name "Main Website" --url "https://example.com"
```

## Examples

### Quick workflow to create a new GA4 property

```bash
# 1. List your accounts to get the account ID
ga-cli accounts list

# 2. Create a new property
ga-cli properties create 123456789 --name "BOTCHA" --timezone "Africa/Tripoli"

# 3. Create a web data stream
ga-cli datastreams create 987654321 --name "BOTCHA Website" --url "https://botcha.example.com"

# 4. Get the measurement ID
ga-cli datastreams get 987654321 111222333
```

### Get measurement ID quickly

```bash
# If you know your property and stream IDs
ga-cli datastreams get <property-id> <stream-id> | grep "Measurement ID"
```

## Command Reference

### Global Options

- `--credentials PATH` - Path to service account credentials file
- `--version` - Show version
- `--help` - Show help message

### Output Formats

Most list and get commands support:
- `--format table` (default) - Beautiful table output
- `--format json` - JSON output

## Development

### Setup development environment

```bash
# Clone the repository
git clone <repository-url>
cd ga-cli

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
```

### Run tests

```bash
pytest tests/ -v
```

## Project Structure

```
ga-cli/
├── ga_cli/
│   ├── __init__.py
│   ├── cli.py              # Main CLI entry point
│   ├── auth.py             # Authentication manager
│   ├── config.py           # Configuration manager
│   ├── commands/
│   │   ├── accounts.py     # Account commands
│   │   ├── properties.py   # Property commands
│   │   ├── datastreams.py  # Data stream commands
│   │   └── config.py       # Config commands
│   └── formatters/
│       ├── table.py        # Table formatter
│       └── json.py         # JSON formatter
├── tests/
├── setup.py
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.7+
- Click 8.0+
- google-analytics-admin 0.27.0+
- google-auth 2.0+
- rich 13.0+

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on GitHub.

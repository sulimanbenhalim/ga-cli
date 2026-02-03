# Docker Distribution Guide

## Building and Publishing to Docker Hub

### 1. Build the image locally

```bash
cd /Users/sulimanbenhalim/Desktop/Development/ga-cli
docker build -t sulimanbenhalim/ga-cli:0.1.0 .
docker tag sulimanbenhalim/ga-cli:0.1.0 sulimanbenhalim/ga-cli:latest
```

### 2. Test the image

```bash
# Test help command
docker run sulimanbenhalim/ga-cli:latest --help

# Test version
docker run sulimanbenhalim/ga-cli:latest --version
```

### 3. Login to Docker Hub

```bash
docker login
# Enter your Docker Hub username and password
```

### 4. Push to Docker Hub

```bash
docker push sulimanbenhalim/ga-cli:0.1.0
docker push sulimanbenhalim/ga-cli:latest
```

## Usage Examples

### Basic usage with credentials file

```bash
docker run -v /path/to/credentials.json:/credentials.json \
  sulimanbenhalim/ga-cli:latest accounts list --credentials /credentials.json
```

### Persist configuration

```bash
docker run -v /path/to/credentials.json:/credentials.json \
  -v ~/.ga-cli:/root/.ga-cli \
  sulimanbenhalim/ga-cli:latest config init --credentials /credentials.json
```

### Using environment variable

```bash
docker run -v /path/to/credentials.json:/credentials.json \
  -e GOOGLE_APPLICATION_CREDENTIALS=/credentials.json \
  sulimanbenhalim/ga-cli:latest accounts list
```

### Create an alias for easier usage

```bash
# Add to ~/.bashrc or ~/.zshrc
alias ga-cli='docker run -v ~/.ga-cli:/root/.ga-cli -v $(pwd):/work -w /work sulimanbenhalim/ga-cli:latest'

# Then use it like:
ga-cli accounts list
```

## Automated Builds with GitHub Actions

You can automate Docker builds by creating `.github/workflows/docker-publish.yml` (covered in CI/CD section).

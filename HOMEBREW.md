# Homebrew Distribution Guide

## Setting Up a Homebrew Tap

### 1. Create a homebrew-tap repository on GitHub

```bash
# Go to GitHub and create a new repository named: homebrew-ga-cli
# Repository URL will be: https://github.com/sulimanbenhalim/homebrew-ga-cli
```

### 2. Clone and set up the tap repository

```bash
cd ~/Desktop/Development
git clone https://github.com/sulimanbenhalim/homebrew-ga-cli.git
cd homebrew-ga-cli

# Copy the formula
cp ../ga-cli/Formula/ga-cli.rb ./ga-cli.rb

# Commit and push
git add ga-cli.rb
git commit -m "Add ga-cli formula"
git push origin main
```

### 3. Users can now install via Homebrew

```bash
# Add your tap
brew tap sulimanbenhalim/ga-cli

# Install ga-cli
brew install ga-cli

# Use it
ga-cli --version
ga-cli accounts list
```

## Alternative: Submit to Homebrew Core

For wider distribution, you can submit to the official Homebrew repository:

### Requirements for Homebrew Core

1. Project must be notable (significant user base/activity)
2. Must have stable releases
3. Must have good documentation
4. Must pass all Homebrew audit checks

### Steps to submit

```bash
# Fork homebrew-core
git clone https://github.com/Homebrew/homebrew-core.git
cd homebrew-core

# Create a new branch
git checkout -b ga-cli

# Add your formula to Formula directory
cp /path/to/ga-cli.rb Formula/ga-cli.rb

# Test the formula
brew install --build-from-source Formula/ga-cli.rb
brew test ga-cli
brew audit --strict ga-cli

# If all tests pass, commit and create PR
git add Formula/ga-cli.rb
git commit -m "ga-cli 0.1.0 (new formula)"
git push origin ga-cli

# Create a Pull Request on GitHub
```

## Testing the Formula Locally

```bash
# Test installation from your local formula
brew install --build-from-source Formula/ga-cli.rb

# Test the command
ga-cli --version

# Run formula tests
brew test ga-cli

# Audit the formula
brew audit --strict ga-cli

# Uninstall when done testing
brew uninstall ga-cli
```

## Updating the Formula for New Versions

When releasing a new version (e.g., 0.2.0):

1. Get new tarball URL and SHA256 from PyPI
```bash
curl -s https://pypi.org/pypi/ga4-cli/json | \
  python3 -c "import sys, json; data = json.load(sys.stdin); \
  tarballs = [u for u in data['urls'] if u['packagetype'] == 'sdist']; \
  print(tarballs[0]['url']); \
  print(tarballs[0]['digests']['sha256'])"
```

2. Update the formula:
```ruby
url "https://files.pythonhosted.org/packages/.../ga4_cli-0.2.0.tar.gz"
sha256 "new-sha256-hash"
```

3. Update the test:
```ruby
assert_match "0.2.0", shell_output("#{bin}/ga-cli --version")
```

4. Commit and push to your tap

## Usage After Installation

Once users install via Homebrew:

```bash
# Configuration
ga-cli config init

# List accounts
ga-cli accounts list

# Get help
ga-cli --help
```

## Benefits of Homebrew Distribution

- No Python/pip knowledge required
- Automatic dependency management
- Easy updates with `brew upgrade ga-cli`
- Clean uninstallation with `brew uninstall ga-cli`
- Popular among macOS/Linux developers

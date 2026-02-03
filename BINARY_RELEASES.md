# Binary Releases Guide

## Overview

This guide covers creating and distributing standalone binary releases of ga-cli for users who don't have Python installed.

## How It Works

1. **PyInstaller** bundles Python + ga-cli + all dependencies into a single executable
2. **GitHub Actions** automatically builds binaries for Linux, macOS, and Windows
3. **GitHub Releases** hosts the binaries for download

## Creating a Release

### 1. Update version number

```bash
# Update version in ga_cli/__init__.py
echo '__version__ = "0.2.0"' > ga_cli/__init__.py
```

### 2. Commit and create a git tag

```bash
git add ga_cli/__init__.py
git commit -m "Bump version to 0.2.0"
git tag v0.2.0
git push origin main
git push origin v0.2.0
```

### 3. GitHub Actions automatically:
- Builds binaries for Linux, macOS, Windows
- Creates a GitHub Release
- Uploads binaries as release assets

### 4. Monitor the build

Visit: https://github.com/sulimanbenhalim/ga-cli/actions

The workflow takes about 10-15 minutes to complete.

## Testing Binary Builds Locally

### Install PyInstaller

```bash
pip install pyinstaller
```

### Build for your platform

```bash
cd /Users/sulimanbenhalim/Desktop/Development/ga-cli
pyinstaller ga-cli.spec
```

The binary will be in `dist/ga-cli` (or `dist/ga-cli.exe` on Windows).

### Test the binary

```bash
./dist/ga-cli --version
./dist/ga-cli --help
./dist/ga-cli accounts list
```

## User Installation (Binary)

### Linux

```bash
# Download
curl -L -o ga-cli.tar.gz https://github.com/sulimanbenhalim/ga-cli/releases/download/v0.1.0/ga-cli-linux-amd64.tar.gz

# Extract
tar -xzf ga-cli.tar.gz

# Make executable
chmod +x ga-cli

# Move to PATH
sudo mv ga-cli /usr/local/bin/

# Use it
ga-cli --version
```

### macOS

```bash
# Download
curl -L -o ga-cli.tar.gz https://github.com/sulimanbenhalim/ga-cli/releases/download/v0.1.0/ga-cli-macos-amd64.tar.gz

# Extract
tar -xzf ga-cli.tar.gz

# Make executable
chmod +x ga-cli

# Move to PATH
sudo mv ga-cli /usr/local/bin/

# On first run, macOS may block it - go to System Preferences > Security & Privacy to allow
ga-cli --version
```

### Windows

```powershell
# Download from:
# https://github.com/sulimanbenhalim/ga-cli/releases/download/v0.1.0/ga-cli-windows-amd64.exe.zip

# Extract the ZIP file

# Add to PATH or run from current directory
.\ga-cli.exe --version
```

## Advantages of Binary Distribution

1. **No Python required** - Users don't need Python installed
2. **Single file** - Easy to download and use
3. **Fast startup** - No virtual environment or dependency installation
4. **Version isolation** - Each binary is self-contained

## Limitations

1. **Large file size** - Binaries are 30-50 MB (includes Python runtime)
2. **Platform-specific** - Need separate binaries for each OS
3. **Update process** - Users must manually download new versions
4. **Startup time** - Slightly slower than native Python (2-3 seconds)

## Troubleshooting

### Binary is blocked on macOS

```bash
# Remove quarantine attribute
xattr -d com.apple.quarantine ga-cli
```

### Binary not found on Linux

```bash
# Ensure /usr/local/bin is in PATH
echo $PATH

# Add to PATH if needed
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Windows Defender blocks binary

- This is normal for unsigned executables
- Click "More info" → "Run anyway"
- For production, consider code signing

## Code Signing (Optional)

For production releases, sign your binaries:

### macOS
```bash
# Requires Apple Developer account ($99/year)
codesign --sign "Developer ID Application: Your Name" dist/ga-cli
```

### Windows
```powershell
# Requires code signing certificate
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com dist/ga-cli.exe
```

## Updating PyInstaller Configuration

Edit `ga-cli.spec` to:
- Add hidden imports
- Include data files
- Customize icon
- Configure UPX compression

## CI/CD Workflow

The `.github/workflows/release.yml` file automates:
1. Building on 3 platforms in parallel
2. Compressing binaries
3. Creating GitHub release
4. Uploading assets

Triggered by:
- Pushing a tag: `git push origin v0.2.0`
- Manual dispatch from Actions tab

## Best Practices

1. **Always tag releases** - Use semantic versioning (v0.1.0, v0.2.0, etc.)
2. **Test locally first** - Build and test before tagging
3. **Document changes** - Update CHANGELOG.md
4. **Announce releases** - Update README with latest version
5. **Keep binaries small** - Exclude unnecessary dependencies

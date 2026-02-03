"""Setup configuration for ga-cli package"""

from setuptools import setup, find_packages
from ga_cli import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ga4-cli",
    version=__version__,
    author="Suliman Ben Halim",
    author_email="suliman.benhalim@binary.ly",
    description="Command-line interface for Google Analytics 4",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sulimanbenhalim/ga-cli",
    project_urls={
        "Bug Reports": "https://github.com/sulimanbenhalim/ga-cli/issues",
        "Source": "https://github.com/sulimanbenhalim/ga-cli",
        "Documentation": "https://github.com/sulimanbenhalim/ga-cli#readme",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="google-analytics ga4 cli command-line",
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0,<9.0.0",
        "google-analytics-admin>=0.27.0,<1.0.0",
        "google-auth>=2.0.0,<3.0.0",
        "rich>=13.0.0,<14.0.0",
        "pytz>=2023.3",
    ],
    entry_points={
        "console_scripts": [
            "ga-cli=ga_cli.cli:cli",
        ],
    },
    license="MIT",
)

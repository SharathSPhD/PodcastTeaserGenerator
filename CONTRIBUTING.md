# Contributing to Podcast Teaser Generator

Thank you for considering contributing to Podcast Teaser Generator! This document provides guidelines and instructions for contributing to the project.

## Ways to Contribute

* Reporting bugs and suggesting features
* Improving documentation
* Writing code to fix issues or add features
* Adding tests
* Creating examples and tutorials

## Development Setup

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/yourusername/podcast_teaser.git
   cd podcast_teaser
   ```
3. Create a virtual environment and install development dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -e .
   ```

## Coding Standards

* Follow PEP 8 style guidelines
* Write docstrings for all functions, classes, and modules
* Add comments for complex code sections
* Include type hints where appropriate

## Pull Request Process

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes and commit them with clear, descriptive messages:
   ```bash
   git commit -m "Add feature X" -m "This implements feature X which solves problem Y"
   ```
3. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
4. Open a pull request from your fork to the main repository
5. Make sure your PR includes:
   * A clear description of the changes
   * Any relevant documentation updates
   * Tests if applicable
   * Updates to the CHANGELOG.md file if needed

## Testing

When adding new features or fixing bugs, please include appropriate tests. Run the existing tests to make sure your changes don't break anything:

```bash
pytest
```

## Building Documentation

To build the documentation locally:

1. Install Sphinx and the ReadTheDocs theme:
   ```bash
   pip install sphinx sphinx_rtd_theme
   ```
2. Build the documentation:
   ```bash
   cd docs
   make html
   ```
3. View the documentation by opening `_build/html/index.html` in your browser

## Reporting Bugs

When reporting bugs, please include:

* A clear description of the issue
* Steps to reproduce the problem
* Expected behavior
* Actual behavior
* System information (OS, Python version, etc.)
* If possible, sample audio files that demonstrate the issue

## Feature Requests

Feature requests are welcome! Please provide:

* A clear description of the feature
* Why it would be valuable
* Any ideas on how it might be implemented
* Examples of how it would be used

## Code of Conduct

Please be respectful and considerate of others when contributing. We aim to foster an inclusive and welcoming community. Harassment, discriminatory jokes and language, or other inappropriate behavior will not be tolerated. We expect all contributors to follow these guidelines:

* Use welcoming and inclusive language
* Be respectful of different viewpoints and experiences
* Gracefully accept constructive criticism
* Focus on what is best for the community
* Show empathy towards other community members

## Questions?

If you have any questions about contributing, please open an issue with your question or reach out to the maintainers.

Thank you for your contributions!

# Contributing to ExcelSearchPro

Thank you for your interest in contributing to ExcelSearchPro! We welcome contributions from everyone.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/yourusername/ExcelSearchPro.git
   cd ExcelSearchPro
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

## Development Setup

1. Install development dependencies:
   ```bash
   pip install pytest black flake8 mypy
   ```

2. Run the verification script to ensure everything works:
   ```bash
   python verify_setup.py
   ```

## Making Changes

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and add tests if applicable

3. Run the tests to ensure everything works:
   ```bash
   python verify_setup.py
   pytest
   ```

4. Format your code:
   ```bash
   black .
   ```

5. Check for style issues:
   ```bash
   flake8 .
   ```

6. Commit your changes:
   ```bash
   git add .
   git commit -m "Add your descriptive commit message"
   ```

7. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

8. Create a Pull Request on GitHub

## Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and small
- Add type hints where appropriate

## Testing

- Add tests for new features
- Ensure all existing tests pass
- Test with different file sizes and formats
- Test Unicode filename support

## Reporting Issues

When reporting issues, please include:

- Your operating system and Python version
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Sample files (if applicable, but don't include sensitive data)

## Feature Requests

We welcome feature requests! Please:

- Check if the feature already exists
- Explain the use case
- Provide examples of how it would work
- Consider if it fits the project's scope

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Follow the project's coding standards

## Questions?

Feel free to open an issue for questions or reach out to the maintainers.

Thank you for contributing to ExcelSearchPro!

# Contributing to Sudoku Solver

Thank you for your interest in contributing to Sudoku Solver! We welcome contributions from the community.

## How to Contribute

### Reporting Bugs
- Use GitHub Issues to report bugs
- Include detailed steps to reproduce the issue
- Provide sample images if applicable
- Include your system information (OS, Python version)

### Suggesting Features
- Open a GitHub Issue with the "enhancement" label
- Describe the feature and its use case
- Explain why it would be beneficial

### Code Contributions

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Run tests: `python -c "import main; print('Import successful')"`
5. Commit your changes: `git commit -m 'Add some feature'`
6. Push to the branch: `git push origin feature/your-feature-name`
7. Open a Pull Request

### Code Style
- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep lines under 100 characters

### Testing
- Test your changes on different Sudoku images
- Ensure the application runs without errors
- Verify that existing functionality still works

## Development Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Copy config: `cp config.ini.example config.ini`
4. Add your API key to `config.ini`
5. Run: `python main.py`

## Areas for Contribution

- Improve image processing algorithms
- Add more SAT solving optimizations
- Enhance the GUI design
- Add support for more image formats
- Create unit tests
- Improve documentation

Thank you for contributing!
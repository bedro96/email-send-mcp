# Contributing to Email Send/Receive MCP

Thank you for your interest in contributing to this project! Here are some guidelines to help you get started.

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/email-send-mcp.git
   cd email-send-mcp
   ```

3. Install dependencies:
   ```bash
   # Using uv (recommended)
   uv pip install -e ".[dev]"
   
   # Or using pip
   pip install -e ".[dev]"
   ```

4. Create a `.env` file based on `.env.example`

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_validators.py -v
```

## Code Style

This project follows Python best practices:

- **Black** for code formatting (line length: 88)
- **isort** for import sorting
- **mypy** for type checking
- **ruff** for linting

Run formatters before committing:

```bash
# Format code
black src/ tests/ main.py
isort src/ tests/ main.py

# Type check
mypy src/

# Lint
ruff check src/ tests/
```

## Pull Request Process

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and add tests if applicable

3. Ensure all tests pass and code is formatted:
   ```bash
   pytest tests/ -v
   black src/ tests/ main.py
   isort src/ tests/ main.py
   ```

4. Commit your changes with a clear message:
   ```bash
   git commit -m "Add feature: description of your feature"
   ```

5. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

6. Create a Pull Request from your fork to the main repository

## Adding New Features

When adding new features:

1. **Email Tools**: Add new tools in `src/server.py` using the `@mcp.tool()` decorator
2. **Services**: Add new services in `src/services/` directory
3. **Utilities**: Add helper functions in `src/utils/` directory
4. **Tests**: Add corresponding tests in `tests/` directory
5. **Documentation**: Update README.md with usage examples

### Example: Adding a New Email Tool

```python
# In src/server.py

@mcp.tool()
async def your_new_tool(
    param1: str,
    param2: int = 10
) -> str:
    """Description of your new tool.
    
    Args:
        param1: Description of param1
        param2: Description of param2 (default: 10)
    
    Returns:
        Result description
    """
    # Implementation
    return "result"
```

## Testing Guidelines

- Write tests for all new features
- Maintain or improve code coverage
- Use descriptive test names
- Include both positive and negative test cases
- Mock external dependencies (SMTP, IMAP, POP3 servers)

## Documentation

- Update README.md for user-facing changes
- Add docstrings to all functions and classes
- Include type hints for all parameters and return values
- Add inline comments for complex logic

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Follow the project's coding standards

## Questions?

If you have questions, please:
1. Check existing issues and discussions
2. Search the documentation
3. Open a new issue with the "question" label

Thank you for contributing! 🎉

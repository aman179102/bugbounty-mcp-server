# Contributing to BugBounty MCP Server

First off, thank you for considering contributing! 🎉

## Code of Conduct

This project adheres to the [Contributor Covenant](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### 🐛 Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/gokulapap/bugbounty-mcp-server/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)

### 💡 Suggesting Features

1. Check existing issues for similar suggestions
2. Create a feature request with:
   - Use case and motivation
   - Proposed implementation
   - Alternative approaches considered

### 🔧 Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/gokulapap/bugbounty-mcp-server.git
cd bugbounty-mcp-server

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### 🧪 Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=bugbounty_mcp_server --cov-report=term-missing -v

# Run specific test file
pytest tests/test_config.py -v

# Run tests matching a keyword
pytest -k "test_valid_url" -v

# Run linting
flake8 bugbounty_mcp_server/
mypy bugbounty_mcp_server/ --ignore-missing-imports
black --check bugbounty_mcp_server/
```

### 📝 Code Style

- Follow [PEP 8](https://pep8.org/) guidelines
- Use [Black](https://black.readthedocs.io/) for formatting
- Use [isort](https://pycqa.github.io/isort/) for import ordering
- Add type hints for all function parameters and return types
- Write docstrings for all public methods and classes
- Keep functions focused and under 50 lines where possible

### 🏗️ Pull Request Process

1. **Fork** the repository and create your branch from `main`
2. **Name your branch** descriptively:
   - `feature/add-websocket-testing`
   - `fix/rate-limiter-race-condition`
   - `docs/update-readme-api-section`
3. **Make your changes** following our code style
4. **Add/update tests** for your changes
5. **Run tests** to ensure nothing breaks
6. **Commit** with clear messages:
   ```
   feat: add WebSocket security testing tool
   fix: resolve rate limiter race condition
   docs: update API documentation
   test: add unit tests for WebSocket testing
   ```
7. **Push** to your fork and open a Pull Request
8. **Describe** your changes in the PR template

### ✅ Pull Request Checklist

- [ ] Code follows project style (black, flake8, mypy)
- [ ] Tests added/updated and passing
- [ ] Documentation updated (README, docstrings)
- [ ] No new warnings or errors
- [ ] Security implications considered
- [ ] All commits are signed

### 🏷️ Issue Labels

| Label | Purpose |
|-------|---------|
| `good first issue` | Beginner-friendly issues |
| `help wanted` | Issues needing assistance |
| `bug` | Bug reports |
| `enhancement` | Feature requests |
| `documentation` | Documentation improvements |
| `security` | Security-related issues |

### 🧪 Adding New Tools

To add a new tool:

1. Identify the appropriate tool category module
2. Add a new method following existing patterns
3. Register the tool in `get_tools()` with proper schema
4. Add the tool definition to the class
5. Write unit tests
6. Update documentation

Example:

```python
Tool(
    name="my_new_tool",
    description="Description of what this tool does",
    inputSchema={
        "type": "object",
        "properties": {
            "target": {"type": "string", "description": "Target URL or IP"}
        },
        "required": ["target"]
    }
)
```

### 📚 Resources

- [MCP Protocol Documentation](https://modelcontextprotocol.io/)
- [Python Security Best Practices](https://cheatsheetseries.owasp.org/)
- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)

## Getting Help

- Open an issue for questions
- Join the community discussions
- Check existing documentation

Thank you for contributing! 🚀

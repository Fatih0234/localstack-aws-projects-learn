# Contributing to LocalStack AWS Learning Projects

First off, thank you for considering contributing to this project! It's people like you that make the open source community such a great place to learn, inspire, and create.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Style Guidelines](#style-guidelines)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](./CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/localstack-aws-projects-learn.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Submit a pull request

## How Can I Contribute?

### Reporting Bugs

Before creating a bug report, please check the existing issues to see if the problem has already been reported.

When filing a bug report, please include:

- **A clear title and description**
- **Steps to reproduce** the issue
- **Expected behavior** vs actual behavior
- **Environment details**: Python version, LocalStack version, OS
- **Screenshots** if applicable
- **Code samples** demonstrating the issue

### Suggesting Enhancements

Enhancement suggestions are welcome! Please provide:

- **Use case**: Why is this enhancement needed?
- **Proposed solution**: How would it work?
- **Alternatives considered**: What other approaches did you think about?
- **Additional context**: Screenshots, examples, etc.

### Adding New Projects

Want to add a new learning project? Great! Please include:

- **Learning objectives**: What AWS concepts does it teach?
- **Prerequisites**: What should learners know first?
- **Estimated time**: How long does it take?
- **Architecture diagram**: Visual representation of the solution
- **Complete documentation**: README with setup and usage instructions
- **Working code**: Tested and functional implementation

### Improving Documentation

Documentation improvements are always welcome! This includes:

- Fixing typos and grammar
- Clarifying explanations
- Adding examples and screenshots
- Translating documentation
- Adding troubleshooting guides

## Development Setup

### Prerequisites

- Python 3.11 or higher
- UV package manager
- Docker
- LocalStack account with auth token

### Installation

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/localstack-aws-projects-learn.git
cd localstack-aws-projects-learn

# Set up environment
cp .env.example .env
# Edit .env with your LocalStack auth token

# Install dependencies
uv sync
source .venv/bin/activate

# Verify setup
localstack status
```

### Testing Your Changes

Before submitting a PR, please test your changes:

```bash
# Run the project you're modifying
cd 01-quickstart-s3
python quickstart.py

# Or for project 2
cd 02-serverless-image-resizer/app
./deployment/build-lambdas.sh
./deployment/awslocal/deploy.sh
```

## Style Guidelines

### Python Code Style

We follow PEP 8 with these specifics:

- **Line length**: 100 characters maximum
- **Imports**: Group imports (stdlib, third-party, local)
- **Docstrings**: Use Google style docstrings
- **Type hints**: Add type hints where possible
- **Comments**: Explain WHY, not WHAT

Example:

```python
def process_image(image_path: str, target_size: tuple[int, int]) -> str:
    """Resize an image to target dimensions.
    
    Args:
        image_path: Path to the source image file.
        target_size: Tuple of (width, height) for the output.
        
    Returns:
        Path to the resized image file.
        
    Raises:
        FileNotFoundError: If image_path doesn't exist.
    """
    # Implementation here
    pass
```

### Documentation Style

- Use clear, simple language
- Include code examples
- Add diagrams where helpful
- Keep README files comprehensive
- Use markdown formatting consistently

### Terraform Style

- Use `terraform fmt` before committing
- Document all variables
- Include descriptions for resources
- Use consistent naming conventions

## Commit Messages

Use clear and meaningful commit messages. Structure:

```
type: Short description (50 chars or less)

More detailed explanation if needed. Wrap at 72 characters.
Include motivation for the change and contrast with previous behavior.

- Bullet points are okay
- Use imperative mood ("Add feature" not "Added feature")
- Reference issues: "Fixes #123"
```

Types:
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, missing semi colons, etc)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Build process or auxiliary tool changes

Examples:
- `feat: Add DynamoDB integration to image resizer`
- `fix: Correct S3 bucket notification trigger`
- `docs: Add troubleshooting section for Lambda timeouts`

## Pull Request Process

1. **Update documentation**: Ensure README and docs reflect your changes
2. **Test your changes**: Verify everything works in LocalStack
3. **Update the CHANGELOG** (if one exists) with your changes
4. **Ensure tests pass**: If there are tests, make sure they pass
5. **Submit PR** with a clear description:
   - What problem does it solve?
   - How does it solve it?
   - Any breaking changes?

### PR Review Process

- All PRs require at least one review
- Address review comments promptly
- Keep PRs focused on a single topic
- Large changes should be broken into smaller PRs

### After Your PR is Merged

You can delete your branch and pull the latest changes from main.

## Questions?

Feel free to open an issue with your question or contact the maintainers.

## Recognition

Contributors will be recognized in our README file and release notes.

Thank you for contributing! 🚀

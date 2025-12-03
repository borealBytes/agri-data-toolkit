# Contributing Guide

Thank you for your interest in contributing to the Agricultural Data Toolkit! This guide will help you get started.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project follows a professional and inclusive code of conduct:

- **Be Respectful**: Treat all contributors with respect and professionalism
- **Be Constructive**: Provide helpful, actionable feedback
- **Be Patient**: Remember that contributors have varying experience levels
- **Be Collaborative**: Work together toward common goals
- **Be Open**: Welcome diverse perspectives and approaches

## Getting Started

### Prerequisites

- Ubuntu LTS 20.04+ (or compatible Linux)
- Python 3.9+
- Git 2.25+
- GDAL 3.0+

### Fork and Clone

```bash
# Fork the repository on GitHub (click Fork button)

# Clone your fork
git clone https://github.com/YOUR_USERNAME/agri-data-toolkit.git
cd agri-data-toolkit

# Add upstream remote
git remote add upstream https://github.com/borealBytes/agri-data-toolkit.git
```

### Setup Development Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Verify setup
pytest tests/
```

## Development Workflow

### 1. Sync with Upstream

```bash
# Fetch latest changes
git fetch upstream

# Merge into your main branch
git checkout main
git merge upstream/main

# Push to your fork
git push origin main
```

### 2. Create Feature Branch

```bash
# Create branch with descriptive name
git checkout -b feature/field-boundary-downloader
# or
git checkout -b fix/ssurgo-missing-values
# or
git checkout -b docs/api-reference-update
```

**Branch Naming Conventions**:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Testing improvements

### 3. Make Changes

```bash
# Make your changes
nano src/agri_toolkit/downloaders/field_boundaries.py

# Run tests frequently
pytest tests/test_downloaders/test_field_boundaries.py

# Check code style
black src/
flake8 src/
isort src/
```

### 4. Commit Changes

```bash
# Stage changes
git add src/agri_toolkit/downloaders/field_boundaries.py
git add tests/test_downloaders/test_field_boundaries.py

# Commit with descriptive message
git commit -m "feat: implement field boundary downloader for CLU data"
```

**Commit Message Format**:

```
<type>: <subject>

<body (optional)>

<footer (optional)>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Build/tooling changes

**Examples**:

```bash
git commit -m "feat: add SSURGO soil data downloader"

git commit -m "fix: handle missing soil data for edge fields

Fixed issue where fields on survey boundaries had incomplete
soil data. Now uses nearest neighbor interpolation for missing
map units.

Closes #42"

git commit -m "docs: update installation guide for Ubuntu 24.04"
```

### 5. Push Changes

```bash
# Push to your fork
git push origin feature/field-boundary-downloader
```

### 6. Create Pull Request

1. Go to your fork on GitHub
2. Click "Compare & pull request"
3. Fill out PR template (see below)
4. Wait for review

## Code Standards

### Python Style Guide

We follow **PEP 8** with these tools:

- **Black**: Code formatting (line length: 100)
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking (encouraged)

### Code Formatting

```bash
# Auto-format code
black src/ tests/

# Sort imports
isort src/ tests/

# Check for issues
flake8 src/ tests/

# Type checking (optional but encouraged)
mypy src/
```

### Code Quality Checklist

- [ ] Code follows PEP 8 style guide
- [ ] All functions have docstrings
- [ ] Type hints used where appropriate
- [ ] No hardcoded paths or credentials
- [ ] Error handling implemented
- [ ] Logging used for important events
- [ ] No print statements (use logging)
- [ ] Configuration via YAML, not hardcoded

### Documentation Standards

**Docstring Format** (Google style):

```python
def download_fields(count: int, regions: list[str]) -> gpd.GeoDataFrame:
    """Download field boundaries for specified regions.

    Args:
        count: Number of fields to download.
        regions: List of agricultural regions (e.g., ['corn_belt', 'great_plains']).

    Returns:
        GeoDataFrame containing field boundaries with attributes.

    Raises:
        ValueError: If count is less than 1 or regions is empty.
        APIError: If download fails after retry attempts.

    Example:
        >>> downloader = FieldBoundaryDownloader()
        >>> fields = downloader.download_fields(count=200, regions=['corn_belt'])
        >>> print(len(fields))
        200
    """
    # Implementation
    pass
```

### Testing Standards

- **Coverage**: Aim for >80% code coverage
- **Test Types**: Unit tests (required), integration tests (encouraged)
- **Naming**: `test_<function_name>_<scenario>`
- **Fixtures**: Use pytest fixtures for common setup

**Test Structure**:

```python
import pytest
from agri_toolkit.downloaders import FieldBoundaryDownloader

class TestFieldBoundaryDownloader:
    """Test suite for field boundary downloader."""

    @pytest.fixture
    def downloader(self):
        """Create downloader instance for testing."""
        return FieldBoundaryDownloader(config="config/test_config.yaml")

    def test_download_fields_success(self, downloader):
        """Test successful field download."""
        fields = downloader.download_fields(count=5, regions=['corn_belt'])
        assert len(fields) == 5
        assert 'geometry' in fields.columns

    def test_download_fields_invalid_count(self, downloader):
        """Test that invalid count raises ValueError."""
        with pytest.raises(ValueError, match="count must be positive"):
            downloader.download_fields(count=0, regions=['corn_belt'])
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_downloaders/test_field_boundaries.py

# Run specific test function
pytest tests/test_downloaders/test_field_boundaries.py::test_download_fields_success

# Run with coverage report
pytest --cov=src/agri_toolkit --cov-report=html

# View coverage report
firefox htmlcov/index.html
```

### Writing Tests

1. **Create test file**: `tests/test_<module>/test_<file>.py`
2. **Import module**: `from agri_toolkit.<module> import <class>`
3. **Write test class**: `class Test<ClassName>:`
4. **Write test methods**: `def test_<function>_<scenario>:`
5. **Use assertions**: `assert result == expected`
6. **Use fixtures**: `@pytest.fixture` for setup/teardown

### Test Data

- Store test fixtures in `tests/fixtures/`
- Use small, representative samples
- Don't commit large data files (> 1MB)
- Mock external API calls

## Documentation

### Types of Documentation

1. **Code Documentation**: Docstrings (required)
2. **API Reference**: Auto-generated from docstrings
3. **User Guides**: Markdown files in `docs/`
4. **Examples**: Python scripts in `examples/`
5. **README**: Project overview and quick start

### Building Documentation

```bash
# Install Sphinx
pip install sphinx sphinx-rtd-theme

# Build HTML docs
cd docs/
make html

# View documentation
firefox _build/html/index.html
```

### Documentation Checklist

- [ ] All public functions have docstrings
- [ ] README updated if user-facing changes
- [ ] Examples added for new features
- [ ] API reference generated and reviewed
- [ ] User guide updated if workflow changes

## Pull Request Process

### Before Submitting

- [ ] All tests pass: `pytest`
- [ ] Code formatted: `black src/ tests/`
- [ ] Imports sorted: `isort src/ tests/`
- [ ] Linting clean: `flake8 src/ tests/`
- [ ] Documentation updated
- [ ] Commit messages follow convention
- [ ] Branch up-to-date with main

### PR Template

When creating a PR, include:

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Testing
Describe testing performed:
- Unit tests added/updated
- Manual testing steps
- Test coverage: X%

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] No breaking changes (or documented)

## Related Issues
Closes #<issue_number>
```

### Review Process

1. **Automated Checks**: CI runs tests and linting
2. **Code Review**: Maintainer reviews code
3. **Feedback**: Address reviewer comments
4. **Approval**: Maintainer approves PR
5. **Merge**: Maintainer merges to main

### After Merge

```bash
# Update your local main
git checkout main
git pull upstream main

# Delete feature branch
git branch -d feature/field-boundary-downloader
git push origin --delete feature/field-boundary-downloader
```

## Common Tasks

### Adding a New Data Downloader

1. Create file: `src/agri_toolkit/downloaders/<source>.py`
2. Inherit from `BaseDownloader`
3. Implement `download()` method
4. Add configuration to `config/default_config.yaml`
5. Write tests: `tests/test_downloaders/test_<source>.py`
6. Add documentation: `docs/data_sources.md`
7. Add example: `examples/<source>_usage.py`

### Adding a New Processor

1. Create file: `src/agri_toolkit/processors/<processor>.py`
2. Implement processing functions
3. Write tests: `tests/test_processors/test_<processor>.py`
4. Add example: `notebooks/<processor>_example.ipynb`

### Fixing a Bug

1. Create issue describing bug
2. Create branch: `fix/<bug-description>`
3. Write failing test that reproduces bug
4. Fix bug
5. Verify test passes
6. Submit PR referencing issue

## Getting Help

### Resources

- **Documentation**: [docs/](../)
- **Examples**: [examples/](../../examples/)
- **Issue Tracker**: [GitHub Issues](https://github.com/borealBytes/agri-data-toolkit/issues)
- **Discussions**: [GitHub Discussions](https://github.com/borealBytes/agri-data-toolkit/discussions)

### Questions

1. Check existing documentation
2. Search GitHub issues
3. Ask in GitHub Discussions
4. Create new issue if needed

### Course Students

- Office hours: 30 min before Classes 2-14
- Teaching assistant support
- Course discussion forum

## Recognition

Contributors are recognized in:

- `CONTRIBUTORS.md` file
- Release notes
- GitHub contributors page

Thank you for contributing! 🌾

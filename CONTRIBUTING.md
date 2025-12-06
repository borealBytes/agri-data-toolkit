# Contributing to agri-data-toolkit

Thank you for your interest in contributing! This guide will help you set up your development environment.

## Development Setup

### 1. Clone and Install

```bash
git clone https://github.com/borealBytes/agri-data-toolkit.git
cd agri-data-toolkit
poetry install --with dev
```

### 2. Install Pre-commit Hooks (Recommended)

**Pre-commit hooks automatically format your code before each commit**, ensuring it meets project standards without manual intervention.

```bash
# Install pre-commit hooks
poetry run pre-commit install
```

That's it! Now every time you `git commit`, your code will be automatically:
- ✅ Formatted with Black
- ✅ Imports sorted with isort
- ✅ Linted with flake8
- ✅ Checked for trailing whitespace, file endings, etc.

### 3. Manual Formatting (Optional)

If you want to format files without committing:

```bash
# Format all files
poetry run black src/ tests/
poetry run isort src/ tests/

# Or use pre-commit manually
poetry run pre-commit run --all-files
```

## Code Quality Standards

This project uses:
- **Black** (line-length=100) for code formatting
- **isort** (black profile) for import sorting
- **flake8** for linting
- **mypy** for type checking
- **pytest** for testing

### Without Pre-commit Hooks

If you choose not to use pre-commit hooks, make sure to run these before pushing:

```bash
poetry run black --check src/ tests/
poetry run isort --check-only src/ tests/
poetry run flake8 src/ tests/
poetry run mypy src/ --ignore-missing-imports
poetry run pytest tests/
```

## Workflow

### Standard Workflow (with pre-commit)

```bash
# 1. Create a feature branch
git checkout -b feature/my-feature

# 2. Make your changes
# ... edit files ...

# 3. Commit (automatic formatting happens here!)
git add .
git commit -m "feat: add new feature"

# 4. Push
git push origin feature/my-feature

# 5. Create Pull Request on GitHub
```

### What Happens on Commit?

When you run `git commit` with pre-commit installed:

1. **Black** formats your Python files
2. **isort** sorts your imports
3. **flake8** checks for code issues
4. Files are automatically fixed if possible
5. If fixes were applied, the commit is blocked - review the changes
6. Run `git add .` and `git commit` again
7. If everything passes, commit succeeds ✅

### Bypassing Hooks (Not Recommended)

In rare cases where you need to commit without running hooks:

```bash
git commit --no-verify -m "your message"
```

⚠️ **Warning**: CI/CD will still check your code, so it's better to let pre-commit fix issues locally.

## Testing

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src/agri_toolkit

# Run specific test file
poetry run pytest tests/test_downloaders/test_field_boundaries.py

# Run specific test
poetry run pytest tests/test_downloaders/test_field_boundaries.py::TestFieldBoundaryDownloader::test_download_minimum_fields
```

## Commit Message Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Formatting, missing semicolons, etc.
- `refactor:` - Code restructuring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

Examples:
```
feat: add sentinel-2 image downloader
fix: correct CRS transformation in field boundaries
docs: update README with installation instructions
test: add tests for weather data validation
```

## Pull Request Process

1. Ensure all tests pass locally
2. Update documentation if needed
3. Add the `preview-ready` label to your PR to trigger CI/CD
4. Wait for CI/CD checks to pass
5. Request review if needed

## Getting Help

If you have questions:
- Open an issue on GitHub
- Check existing issues and discussions
- Review the documentation in `/docs`

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

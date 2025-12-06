# CI/CD Workflow

This project uses a **single unified pipeline** that auto-formats code, then runs linting, testing, and building - all in one sequential workflow.

## Overview

```
Push to branch
    ↓
Job 1: Format
   ├─ autopep8 (whitespace)
   ├─ Black (code formatting)
   ├─ isort (import sorting)
   └─ Commit if changes (optional)
    ↓
Job 2: Lint (on formatted code)
   ├─ Black --check
   ├─ isort --check
   ├─ flake8
   └─ mypy
    ↓
Job 3: Test (after lint passes)
   ├─ Install GDAL
   ├─ pytest with coverage
   └─ Upload to Codecov
    ↓
Job 4: Build (after test passes)
   ├─ poetry build
   └─ Upload artifacts (if labeled)
```

## Key Features

✅ **Single workflow** - No race conditions, no complexity
✅ **Auto-format first** - Always formats before CI checks
✅ **Sequential jobs** - Each job waits for previous to pass
✅ **Format commit included** - Commits are part of the pipeline
✅ **Same SHA for all jobs** - All jobs run on formatted code
✅ **Zero maintenance** - Just push code, pipeline handles rest

## Workflow File

**Location**: `.github/workflows/ci.yml`

**Triggers**:
- `push` - Any push to any branch
- `pull_request` - PRs targeting main branch

## Job Details

### Job 1: Format

**Purpose**: Auto-format code using autopep8, Black, and isort

**Steps**:
1. Checkout code
2. Install Poetry and dependencies
3. Run autopep8 (whitespace cleanup)
4. Run Black (code formatting)
5. Run isort (import sorting)
6. Check if formatting made changes
7. If changes: commit and push
8. Export SHA for next jobs

**Key behavior**:
- Commits formatting changes back to the branch
- Uses `github-actions[bot]` as committer
- NO `[skip ci]` tag - we want CI to run on formatted code
- Outputs SHA for downstream jobs to use

**Time**: ~30-60 seconds

### Job 2: Lint

**Purpose**: Validate code quality and style

**Dependencies**: Waits for `format` job

**Checks out**: The SHA from format job (formatted code)

**Steps**:
1. Black --check (formatting validation)
2. isort --check (import order validation)
3. flake8 (style linting)
4. mypy (type checking)

**Time**: ~1-2 minutes

### Job 3: Test

**Purpose**: Run test suite with coverage

**Dependencies**: Waits for `format` and `lint` jobs

**Checks out**: The SHA from format job (formatted code)

**Steps**:
1. Install GDAL system dependencies
2. Run pytest with coverage
3. Upload coverage to Codecov

**Time**: ~3-5 minutes

### Job 4: Build

**Purpose**: Build package and optionally store artifacts

**Dependencies**: Waits for `format`, `lint`, and `test` jobs

**Checks out**: The SHA from format job (formatted code)

**Steps**:
1. Build package with Poetry
2. Check if PR and has `generate-build-artifact` label
3. Upload artifacts if labeled

**Time**: ~1 minute

## Execution Guarantee

✅ **Format always runs first** - Happens before any checks
✅ **All jobs use formatted code** - Same SHA across pipeline
✅ **No race conditions** - Sequential job dependencies
✅ **Atomic commits** - Format commits part of pipeline

## Execution Flow Examples

### Scenario 1: Code needs formatting

```
1. Developer pushes unformatted code
2. Format job runs:
   - Formats code
   - Commits changes (new SHA created)
   - Exports new SHA
3. Lint job runs on formatted SHA
4. Test job runs on formatted SHA
5. Build job runs on formatted SHA

Result: ✅ All pass, branch has 2 commits (original + format)
```

### Scenario 2: Code already formatted

```
1. Developer pushes formatted code
2. Format job runs:
   - Checks code
   - No changes needed
   - Exports current SHA
3. Lint job runs on current SHA
4. Test job runs on current SHA
5. Build job runs on current SHA

Result: ✅ All pass, branch has 1 commit (original)
```

### Scenario 3: Tests fail

```
1. Developer pushes code
2. Format job runs: ✅ Pass
3. Lint job runs: ✅ Pass
4. Test job runs: ❌ Fail
5. Build job skipped (dependency failed)

Result: ❌ Pipeline fails at test stage
```

## Labels

### `generate-build-artifact`

**Purpose**: Control whether to upload build artifacts

**Usage**:
```bash
gh pr edit <PR_NUMBER> --add-label "generate-build-artifact"
```

**Behavior**:
- ✅ With label: Artifacts uploaded for 7 days
- ❌ Without label: Build runs but artifacts not stored

**When to use**:
- Testing pip installation
- Preparing for release
- Sharing with collaborators
- Debugging build issues

**Cost savings**: Most PRs don't need artifacts stored

## For Developers

### Local Development

**Option 1: Pre-commit hooks (Recommended)**
```bash
poetry run pre-commit install
git commit -m "feat: new feature"  # Auto-formats locally
```

**Option 2: Manual formatting**
```bash
poetry run autopep8 --in-place --recursive --select=W src/ tests/
poetry run black src/ tests/
poetry run isort src/ tests/
git commit -m "feat: new feature"
```

**Option 3: Let CI do it**
```bash
git commit -m "feat: new feature"
git push  # Pipeline formats automatically
```

### Understanding Pipeline Status

**Green checkmark (✅)**: All jobs passed
- Code is formatted
- Linting passed
- Tests passed
- Build succeeded

**Red X (❌)**: Pipeline failed
- Check which job failed
- Format job rarely fails (only on syntax errors)
- Lint job fails on style issues
- Test job fails on test failures
- Build job fails on package issues

**Yellow dot (🟡)**: Pipeline running
- Wait for completion
- Typically 5-8 minutes total

## For AI Agents

### Workflow

```bash
# AI agent pushes code via GitHub API
# Pipeline automatically:
1. Formats code (autopep8, Black, isort)
2. Commits formatting if needed
3. Runs lint checks
4. Runs tests
5. Builds package

# No action required from AI!
```

### Benefits

✅ **Zero config** - Just push code
✅ **Auto-fixes formatting** - Don't worry about style
✅ **Clear feedback** - Pass/fail status on PR
✅ **Production ready** - If pipeline passes, code is good

## Troubleshooting

### Format job fails

**Cause**: Usually syntax errors preventing parsing

**Solution**:
```python
# Fix syntax errors first
# Pipeline will format after syntax is valid
```

### Lint job fails

**Cause**: Style issues not auto-fixable

**Common issues**:
- Unused imports (not removed by isort)
- Line too long (>100 chars) in comments/strings
- Type hints missing

**Solution**: Review flake8/mypy errors and fix manually

### Test job fails

**Cause**: Test failures or missing dependencies

**Solution**:
```bash
# Run tests locally
poetry run pytest tests/ -v

# Fix failing tests
# Push changes
```

### Build job fails

**Cause**: Package configuration issues

**Solution**:
```bash
# Test build locally
poetry build

# Fix pyproject.toml issues
# Push changes
```

## Performance

### Typical Times

| Job | Time | Cumulative |
|-----|------|------------|
| Format | 30-60s | 1 min |
| Lint | 1-2 min | 3 min |
| Test | 3-5 min | 8 min |
| Build | 1 min | 9 min |

**Total**: ~5-9 minutes for full pipeline

### Optimization

✅ **Cached dependencies** - Poetry venv cached
✅ **Parallel where possible** - Multiple test runners
✅ **Fail fast** - Lint before expensive tests
✅ **Conditional artifacts** - Only upload when labeled

## Best Practices

### For Solo Developer

1. **Install pre-commit hooks** - Fastest local feedback
2. **Let pipeline handle remote formatting** - For AI commits
3. **Review format commits** - Ensure changes are correct
4. **Only label artifacts when needed** - Save storage

### For Contributors

1. **Fork and clone**
2. **Install pre-commit**: `poetry run pre-commit install`
3. **Make changes**
4. **Commit** (formats locally if hooks installed)
5. **Push** (pipeline formats remotely if needed)
6. **Create PR**
7. **Pipeline runs automatically**
8. **Review and merge**

## Migration Notes

### What Changed (Dec 2025)

**Before**: Two separate workflows
- `auto-format.yml` - Formatted code
- `ci.yml` - Ran checks (via workflow_run)

**After**: Single unified workflow
- `.github/workflows/ci.yml` - Does everything

**Benefits**:
- Simpler architecture
- No workflow_run complexity
- Clearer execution order
- Easier to debug
- Same SHA across all jobs

### Breaking Changes

None! The pipeline still:
- Formats code automatically
- Runs all CI checks
- Works with PRs and pushes
- Uploads artifacts when labeled

## Configuration Files

**Workflow**:
- `.github/workflows/ci.yml` - Main pipeline

**Code Quality**:
- `pyproject.toml` - Black, isort, pytest config
- `.flake8` - Flake8 rules
- `.pre-commit-config.yaml` - Local hooks

## References

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Job dependencies](https://docs.github.com/en/actions/using-workflows/advanced-workflow-features#creating-dependent-jobs)
- [Job outputs](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idoutputs)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [Black Documentation](https://black.readthedocs.io/)
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Full guide

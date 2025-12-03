# CI/CD Workflows

This project uses automated workflows to maintain code quality without manual intervention.

## Overview

```
Code Push (AI Agent or Human)
        ↓
   Auto-Format Workflow
   ├─ Black formatter
   ├─ isort import sorter
   └─ Commit if changes needed
        ↓
   CI/CD Pipeline
   ├─ Lint (Black, isort, flake8, mypy)
   ├─ Test (pytest with coverage)
   └─ Build (poetry build)
        ├─ With 'generate-build-artifact' label → Save artifacts
        └─ Without label → Skip artifacts (saves storage)
```

## Workflows

### 1. Auto-Format Workflow (`.github/workflows/auto-format.yml`)

**Trigger:** Every push to any branch

**Purpose:** Automatically format code to project standards

**Steps:**
1. Checkout code
2. Install Poetry and dependencies
3. Run Black formatter
4. Run isort import sorter
5. If changes detected:
   - Commit with message: `style: auto-format code with Black and isort [skip ci]`
   - Push to same branch
6. If no changes: Skip commit

**Special Notes:**
- Uses `[skip ci]` to prevent infinite loops
- Commits as `github-actions[bot]`
- Runs fast (~30-60 seconds)

### 2. CI/CD Pipeline (`.github/workflows/ci.yml`)

**Trigger:** 
- Push to main branch
- Pull requests with `preview-ready` label
- After auto-format workflow completes

**Jobs:**

#### Job 1: Lint
- Check Black formatting
- Check isort import order
- Run flake8 linting
- Run mypy type checking
- **Fast:** ~1-2 minutes

#### Job 2: Test (runs after lint)
- Install GDAL dependencies
- Run pytest with coverage
- Upload coverage to Codecov
- **Medium:** ~3-5 minutes

#### Job 3: Build (runs after test)
- Build package with Poetry
- **Conditionally** store artifacts (see labels below)
- **Fast:** ~1 minute

**Total Time:** ~5-8 minutes for full pipeline

## Labels

### `preview-ready`

Add this label to PRs to trigger full CI/CD pipeline:

```bash
# Via GitHub UI: Add label "preview-ready" to PR
# Via GitHub CLI:
gh pr edit <PR_NUMBER> --add-label "preview-ready"
```

Without this label:
- Auto-format still runs
- CI/CD waits for label

### `generate-build-artifact` (New!)

**Purpose:** Control whether build artifacts are stored

**Why:** Saves GitHub storage costs by not storing artifacts you'll never use

**Behavior:**
- ✅ **With label:** Build artifacts uploaded to GitHub (7 day retention)
- ⏭️ **Without label:** Build runs successfully but artifacts NOT stored

**When to use:**
```bash
# Add this label when you need the .whl and .tar.gz files
gh pr edit <PR_NUMBER> --add-label "generate-build-artifact"

# Examples:
# - Testing pip installation from built package
# - Preparing for release
# - Sharing package with collaborators
# - Debugging build issues
```

**When to skip:**
- Regular development PRs (default)
- Just running tests
- Code review PRs
- Most daily work

**Cost savings:**
- Typical PR: No artifacts = $0 storage
- With artifacts: ~5-10MB stored for 7 days
- Over dozens of PRs: Significant savings!

**Note:** Build ALWAYS runs (to verify it works), but artifacts only stored when labeled.

## For AI Agents

### Current Workflow

```bash
# AI agent pushes code via GitHub API
# (happens automatically in Perplexity/MCP)

# Auto-format runs automatically
# CI/CD runs automatically
# All checks pass ✓
# No artifacts stored (unless labeled)
```

### No Action Required!

Just push your code. The workflows handle everything:
- ✅ Formatting
- ✅ Import sorting
- ✅ Linting
- ✅ Type checking
- ✅ Testing
- ✅ Building
- 💰 Artifacts only when needed (saves costs)

## For Local Development

### Option 1: Pre-commit Hooks (Recommended)

```bash
# One-time setup
poetry run pre-commit install

# Now git commit automatically formats
git commit -m "feat: new feature"
# ✓ Black runs
# ✓ isort runs
# ✓ flake8 checks
# ✓ Commit succeeds
```

### Option 2: Manual Format

```bash
# Before committing
poetry run black src/ tests/
poetry run isort src/ tests/

git add .
git commit -m "feat: new feature"
```

### Option 3: Let GitHub Do It

```bash
# Just push
git push

# Auto-format workflow fixes it
# CI/CD runs on formatted code
```

## Workflow States

### ✅ Success Path

```
Push → Auto-format (no changes) → CI/CD → All pass ✓ → No artifacts stored
```

### 🔧 Auto-Fix Path

```
Push → Auto-format (changes made) → Auto-commit → CI/CD → All pass ✓
```

### 📦 With Artifacts

```
Push → Add 'generate-build-artifact' label → CI/CD → Build artifacts stored
```

### ❌ Failure Path

```
Push → Auto-format → CI/CD → Tests fail ✗
```

**Note:** Auto-format only fixes formatting, not logic errors or test failures.

## Performance

### Auto-Format Workflow
- **Cached:** ~30 seconds
- **Cold start:** ~60 seconds
- **Cost:** Minimal (runs on push)

### CI/CD Pipeline
- **Lint:** ~1-2 minutes
- **Test:** ~3-5 minutes  
- **Build:** ~1 minute
- **Total:** ~5-8 minutes
- **Cost:** Moderate (only on labeled PRs/main)

### Artifact Storage
- **With label:** ~5-10MB per PR (7 day retention)
- **Without label:** $0 storage cost
- **Savings:** Significant over dozens of PRs

## Troubleshooting

### Auto-format not running?

Check:
1. Workflow file exists: `.github/workflows/auto-format.yml`
2. Push was to a branch (not tag)
3. Check Actions tab on GitHub

### CI/CD not running?

Check:
1. Is this a PR? Does it have `preview-ready` label?
2. Is this main branch?
3. Did auto-format complete?
4. Check Actions tab on GitHub

### Build artifacts not appearing?

Check:
1. Does PR have `generate-build-artifact` label?
2. Did build job complete successfully?
3. Check "Artifacts" section at bottom of workflow run

### Infinite loop?

Should never happen due to `[skip ci]` in commit message.
If it does:
1. Check auto-format commit message includes `[skip ci]`
2. Check CI workflow respects `[skip ci]`

## Best Practices

### For Solo Developer

1. **Install pre-commit hooks locally** (fastest feedback)
2. **Let auto-format handle remote commits** (AI agents)
3. **Add `preview-ready` label before review** (runs full CI)
4. **Only add `generate-build-artifact` when needed** (saves costs)

### For Contributors

1. **Fork and clone**
2. **Install pre-commit hooks**: `poetry run pre-commit install`
3. **Make changes**
4. **Commit** (auto-formatted locally)
5. **Push and create PR**
6. **Auto-format runs remotely** (backup)
7. **Add `preview-ready` when ready**
8. **Add `generate-build-artifact` only if you need the build files**

## Configuration Files

- `.github/workflows/auto-format.yml` - Auto-format workflow
- `.github/workflows/ci.yml` - CI/CD pipeline
- `.pre-commit-config.yaml` - Local pre-commit hooks
- `pyproject.toml` - Black, isort, mypy config
- `.flake8` - Flake8 config

## References

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Pre-commit Framework](https://pre-commit.com/)
- [Black Documentation](https://black.readthedocs.io/)
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Full contribution guide

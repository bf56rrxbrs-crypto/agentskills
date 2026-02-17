# Autonomous PR Review and Management

This repository includes automated workflows for seamless PR review, quality checks, and issue resolution.

## Features

### 1. Automated PR Review (`pr-review.yml`)

Automatically triggered on every PR to provide comprehensive quality analysis:

- **Code Quality Checks**
  - Runs `ruff` linting with GitHub annotations
  - Validates code formatting
  - Executes full test suite

- **Conflict Detection**
  - Automatically checks for merge conflicts
  - Alerts when conflicts are detected

- **Auto-Review Summary**
  - Posts comprehensive review comment on PR
  - Includes file change analysis
  - Shows code quality metrics
  - Reports test results

- **Security Checks**
  - Runs security audits on dependencies
  - Identifies potential vulnerabilities

### 2. Auto-Fix Workflow (`auto-fix.yml`)

Enables automated issue resolution via PR comments:

**Usage:**
- Comment `/fix` on a PR to automatically fix linting and formatting issues
- Comment `/format` to apply code formatting only

**What it does:**
- Runs `ruff check --fix` to fix linting issues
- Applies `ruff format` for consistent formatting
- Commits and pushes changes automatically
- Posts confirmation comment

### 3. Continuous Monitoring (`monitoring.yml`)

Daily health checks and maintenance:

- **Dependency Updates**
  - Checks for outdated dependencies daily
  - Creates issues for available updates
  - Prevents duplicate update notifications

- **Health Checks**
  - Runs full test suite
  - Performs security scans
  - Generates health reports
  - Uploads reports as artifacts

### 4. CLI Auto-Review Command

New `auto-review` command added to `skills-ref` CLI:

```bash
# Run automated review
skills-ref auto-review

# Run and auto-fix issues
skills-ref auto-review --fix

# Output as JSON
skills-ref auto-review --json
```

**Features:**
- Linting checks (via ruff)
- Formatting validation
- Test execution
- Auto-fix capability
- JSON output for CI integration

## Workflow Integration

### PR Lifecycle

1. **PR Created/Updated** → `pr-review.yml` runs automatically
2. **Review Comment Posted** → Includes quality metrics and suggestions
3. **Developer Comments `/fix`** → `auto-fix.yml` applies fixes
4. **Changes Committed** → PR is re-reviewed automatically
5. **All Checks Pass** → PR ready for merge

### Continuous Monitoring

- **Daily (00:00 UTC)** → Health checks run
- **Dependency updates detected** → Issue created
- **Security issues found** → Alerts generated

## Configuration

### Enabling Workflows

All workflows are ready to use once this PR is merged. No additional configuration required.

### Customizing Workflows

Edit workflow files in `.github/workflows/`:

- `pr-review.yml` - Adjust quality check thresholds
- `auto-fix.yml` - Modify auto-fix behavior
- `monitoring.yml` - Change monitoring schedule

### Required Permissions

Workflows use standard GitHub Actions permissions:
- `pull-requests: write` - For posting comments
- `contents: write` - For committing auto-fixes
- `contents: read` - For reading repository content

## Benefits

✅ **Faster Reviews** - Automated quality checks reduce manual review time

✅ **Consistent Standards** - Enforces code quality automatically

✅ **Quick Fixes** - One-command issue resolution

✅ **Proactive Monitoring** - Catches issues before they become problems

✅ **Better Security** - Regular security scans and dependency updates

## Examples

### Example PR Review Comment

```markdown
🤖 Automated PR Review Summary

### Changes Overview
- **Files changed:** 5
- **Code modified:** true
- **Tests modified:** true

### Code Quality
✅ Linting: No issues found
✅ Formatting: Properly formatted

### Test Results
✅ All tests passing
```

### Example Auto-Fix Response

```markdown
🤖 Auto-fix applied! Linting and formatting issues have been resolved.
```

## Troubleshooting

**Workflow not running?**
- Check that Actions are enabled in repository settings
- Verify workflow permissions are granted

**Auto-fix not working?**
- Ensure comment contains exactly `/fix` or `/format`
- Check that the comment is on a PR (not an issue)

**Tests failing?**
- Review test output in workflow logs
- Run `pytest -v` locally to reproduce
- Fix issues and push changes

## Future Enhancements

Potential additions for future versions:

- Automatic PR merging when all checks pass
- AI-powered code suggestions
- Performance benchmarking
- Coverage tracking and reporting
- Integration with external code quality tools
- Automated changelog generation

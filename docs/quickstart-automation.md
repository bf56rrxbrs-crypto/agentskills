# Quick Start: Autonomous PR Management

## For PR Authors

### When You Create a PR

The automation will automatically:
- ✅ Run linting and formatting checks
- ✅ Execute all tests
- ✅ Check for merge conflicts
- ✅ Post a review summary comment

### Need to Fix Issues?

Just comment on your PR:
- `/fix` - Auto-fix linting and formatting issues
- `/format` - Apply code formatting only

The bot will commit and push the fixes automatically.

### Before Requesting Review

Run locally to catch issues early:
```bash
cd skills-ref
skills-ref auto-review --fix .
```

## For Reviewers

### What to Expect

Every PR will have an automated review comment showing:
- Files changed count
- Code quality status (✅ or ⚠️)
- Test results
- Any issues found

### Manual Review Focus

Focus your manual review on:
- Logic and algorithm correctness
- Architecture and design decisions
- Edge cases and error handling
- Documentation clarity

The automation handles:
- Code style and formatting
- Test execution
- Basic quality metrics
- Security checks

## For Maintainers

### Daily Monitoring

The system automatically:
- Runs health checks daily at 00:00 UTC
- Creates issues for dependency updates
- Uploads health reports as artifacts

### Workflow Files

Located in `.github/workflows/`:
- `pr-review.yml` - PR quality checks
- `auto-fix.yml` - Auto-fix on command
- `monitoring.yml` - Daily health checks

### Customization

Edit workflow files to:
- Adjust check thresholds
- Add new quality metrics
- Modify notification behavior
- Change monitoring schedule

## Commands Reference

### CLI Commands
```bash
# Validate a skill
skills-ref validate path/to/skill

# Run automated review
skills-ref auto-review .

# Review and auto-fix
skills-ref auto-review --fix .

# Get JSON output
skills-ref auto-review --json .
```

### PR Comment Commands
- `/fix` - Fix linting and formatting
- `/format` - Apply formatting only

## Troubleshooting

**Workflow not running?**
- Check Actions are enabled in Settings
- Verify workflow permissions

**Auto-fix not working?**
- Must be on a PR (not issue)
- Must include exact command: `/fix` or `/format`

**Want to skip checks?**
- Not recommended, but you can add `[skip ci]` to commit message

## Best Practices

1. **Run locally first**: Use `auto-review --fix` before pushing
2. **Small PRs**: Easier for automation to review
3. **Clear descriptions**: Help reviewers understand context
4. **Fix promptly**: Use `/fix` to quickly resolve issues
5. **Monitor daily**: Check health report artifacts

## Learn More

- [Full Documentation](automation.md)
- [skills-ref README](../skills-ref/README.md)
- [Contributing Guidelines](../CONTRIBUTING.md) (if exists)

# Skills-ref Usage Examples

This directory contains practical examples of using the skills-ref library.

## Basic Usage

### Example 1: Validating a Single Skill

```python
from pathlib import Path
from skills_ref import validate

skill_dir = Path("my-skill")
errors = validate(skill_dir)

if errors:
    print(f"❌ Validation failed:")
    for error in errors:
        print(f"  - {error}")
else:
    print(f"✅ Skill is valid!")
```

### Example 2: Reading Skill Properties

```python
from pathlib import Path
from skills_ref import read_properties

skill_dir = Path("my-skill")
props = read_properties(skill_dir)

print(f"Name: {props.name}")
print(f"Description: {props.description}")
print(f"License: {props.license}")

# Convert to dictionary
data = props.to_dict()
print(f"Properties: {data}")
```

### Example 3: Generating Agent Prompts

```python
from pathlib import Path
from skills_ref import to_prompt

# Single skill
prompt = to_prompt([Path("my-skill")])
print(prompt)

# Multiple skills
skills = [
    Path("skills/pdf-reader"),
    Path("skills/code-formatter"),
    Path("skills/data-analysis")
]
prompt = to_prompt(skills)
print(prompt)
```

## Advanced Usage

### Example 4: Getting Comprehensive Skill Info

```python
from pathlib import Path
from skills_ref import get_skill_info

skill_dir = Path("my-skill")
info = get_skill_info(skill_dir)

print(f"Valid: {info['valid']}")
print(f"Path: {info['path']}")

if info['properties']:
    print(f"Name: {info['properties']['name']}")
    print(f"Description: {info['properties']['description']}")

if info['validation_errors']:
    print("Errors:")
    for error in info['validation_errors']:
        print(f"  - {error}")
```

### Example 5: Batch Validation

```python
from pathlib import Path
from skills_ref import validate

skills_to_check = [
    Path("skills/skill-a"),
    Path("skills/skill-b"),
    Path("skills/skill-c")
]

results = {}
for skill_dir in skills_to_check:
    errors = validate(skill_dir)
    results[skill_dir.name] = {
        'valid': len(errors) == 0,
        'errors': errors
    }

# Print summary
valid_count = sum(1 for r in results.values() if r['valid'])
print(f"\n✅ {valid_count}/{len(results)} skills passed validation")

# Print errors
for skill_name, result in results.items():
    if not result['valid']:
        print(f"\n❌ {skill_name}:")
        for error in result['errors']:
            print(f"  - {error}")
```

### Example 6: Discovering Skills

```python
from pathlib import Path
from skills_ref import count_skills
from skills_ref.parser import find_skill_md

# Count skills in a directory
skills_dir = Path("skills")
count = count_skills(skills_dir, recursive=True)
print(f"Found {count} skills")

# List all skills
for item in skills_dir.iterdir():
    if item.is_dir() and find_skill_md(item):
        print(f"  - {item.name}")
```

### Example 7: CI/CD Integration

```python
#!/usr/bin/env python3
"""CI/CD script to validate all skills."""

import sys
from pathlib import Path
from skills_ref import validate

def main():
    skills_dir = Path("skills")
    all_valid = True
    
    print("Validating skills...")
    
    for skill_dir in skills_dir.iterdir():
        if not skill_dir.is_dir():
            continue
            
        errors = validate(skill_dir)
        if errors:
            all_valid = False
            print(f"❌ {skill_dir.name}: FAILED")
            for error in errors:
                print(f"   {error}")
        else:
            print(f"✅ {skill_dir.name}: OK")
    
    if not all_valid:
        print("\n❌ Validation failed")
        sys.exit(1)
    else:
        print("\n✅ All skills valid")
        sys.exit(0)

if __name__ == "__main__":
    main()
```

## CLI Examples

### Validating Skills

```bash
# Validate a single skill
skills-ref validate my-skill

# Validate multiple skills
skills-ref validate skill-a skill-b skill-c

# Get JSON output (useful for parsing)
skills-ref validate my-skill --json

# Quiet mode (only errors, good for CI)
skills-ref validate my-skill --quiet
```

### Listing Skills

```bash
# List skills in current directory
skills-ref list .

# List recursively
skills-ref list . --recursive

# JSON output
skills-ref list . --json --recursive
```

### Reading Properties

```bash
# Get skill properties as JSON
skills-ref read-properties my-skill

# Use with jq for parsing
skills-ref read-properties my-skill | jq '.name'
```

### Generating Prompts

```bash
# Generate XML prompt for multiple skills
skills-ref to-prompt skill-a skill-b skill-c > available_skills.xml
```

## Error Handling

### Example 8: Handling Errors Gracefully

```python
from pathlib import Path
from skills_ref import read_properties, validate
from skills_ref.errors import SkillError, ParseError, ValidationError

skill_dir = Path("my-skill")

try:
    # Validate first
    errors = validate(skill_dir)
    if errors:
        print("Validation errors found:")
        for error in errors:
            print(f"  - {error}")
    
    # Then read properties
    props = read_properties(skill_dir)
    print(f"Successfully loaded: {props.name}")
    
except ParseError as e:
    print(f"Parse error: {e}")
except ValidationError as e:
    print(f"Validation error: {e}")
except SkillError as e:
    print(f"Skill error: {e}")
```

## Testing

### Example 9: Writing Tests

```python
import pytest
from pathlib import Path
from skills_ref import validate, read_properties

def test_my_skill_is_valid(tmp_path):
    """Test that a skill passes validation."""
    skill_dir = tmp_path / "test-skill"
    skill_dir.mkdir()
    
    (skill_dir / "SKILL.md").write_text("""---
name: test-skill
description: A test skill
---
# Test Skill
""")
    
    errors = validate(skill_dir)
    assert errors == [], f"Expected no errors, got: {errors}"

def test_skill_properties(tmp_path):
    """Test reading skill properties."""
    skill_dir = tmp_path / "test-skill"
    skill_dir.mkdir()
    
    (skill_dir / "SKILL.md").write_text("""---
name: test-skill
description: A test skill
license: MIT
---
Body
""")
    
    props = read_properties(skill_dir)
    assert props.name == "test-skill"
    assert props.description == "A test skill"
    assert props.license == "MIT"
```

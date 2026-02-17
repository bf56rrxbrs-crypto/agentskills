# skills-ref

Reference library for Agent Skills.

> **Note:** This library is intended for demonstration purposes only. It is not meant to be used in production.

## Installation

### macOS / Linux

Using pip:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Or using [uv](https://docs.astral.sh/uv/):

```bash
uv sync
source .venv/bin/activate
```

### Windows

Using pip (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
```

Using pip (Command Prompt):

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
pip install -e .
```

Or using [uv](https://docs.astral.sh/uv/):

```powershell
uv sync
.venv\Scripts\Activate.ps1
```

After installation, the `skills-ref` executable will be available on your `PATH` (within the activated virtual environment).

## Usage

### CLI

#### Validate Skills

Validate one or more skill directories:

```bash
# Validate a single skill
skills-ref validate path/to/skill

# Validate multiple skills at once
skills-ref validate path/to/skill-a path/to/skill-b path/to/skill-c

# Output validation results as JSON
skills-ref validate path/to/skill --json

# Quiet mode (only show errors, useful for CI/CD)
skills-ref validate path/to/skill --quiet
```

#### List Skills

Discover and list skills in a directory:

```bash
# List skills in current directory
skills-ref list .

# List skills recursively
skills-ref list . --recursive

# Output as JSON
skills-ref list . --json
```

#### Read Properties

Read and display skill properties as JSON:

```bash
# Read skill properties (outputs JSON)
skills-ref read-properties path/to/skill
```

#### Generate Prompts

Generate `<available_skills>` XML for agent prompts:

```bash
# Generate <available_skills> XML for agent prompts
skills-ref to-prompt path/to/skill-a path/to/skill-b

# Run automated code review
skills-ref auto-review .

# Run review and auto-fix issues
skills-ref auto-review --fix .

# Output review results as JSON
skills-ref auto-review --json .
```

### Python API

```python
from pathlib import Path
from skills_ref import (
    validate, 
    read_properties, 
    to_prompt,
    get_skill_info,
    count_skills
)

# Validate a skill directory
problems = validate(Path("my-skill"))
if problems:
    print("Validation errors:", problems)

# Read skill properties
props = read_properties(Path("my-skill"))
print(f"Skill: {props.name} - {props.description}")

# Get comprehensive skill information
info = get_skill_info(Path("my-skill"))
print(f"Valid: {info['valid']}")
print(f"Properties: {info['properties']}")

# Count skills in a directory
num_skills = count_skills(Path("skills-directory"), recursive=True)
print(f"Found {num_skills} skills")

# Generate prompt for available skills
prompt = to_prompt([Path("skill-a"), Path("skill-b")])
print(prompt)
```

## Agent Prompt Integration

Use `to-prompt` to generate the suggested `<available_skills>` XML block for your agent's system prompt. This format is recommended for Anthropic's models, but Skill Clients may choose to format it differently based on the model being used.

```xml
<available_skills>
<skill>
<name>
my-skill
</name>
<description>
What this skill does and when to use it
</description>
<location>
/path/to/my-skill/SKILL.md
</location>
</skill>
</available_skills>
```

The `<location>` element tells the agent where to find the full skill instructions.

## Features

### Enhanced Validation

The validator provides helpful error messages with actionable suggestions:

```bash
$ skills-ref validate Invalid-Skill
✗ Validation failed for Invalid-Skill:
  - Skill name 'Invalid-Skill' must be lowercase. Suggestion: 'invalid-skill'
```

### Batch Operations

Validate multiple skills simultaneously:

```bash
$ skills-ref validate skill-a skill-b skill-c
✓ Valid skill: skill-a
✓ Valid skill: skill-b
✗ Validation failed for skill-c:
  - Missing required field in frontmatter: description
```

### JSON Output

Get machine-readable output for automation:

```bash
$ skills-ref validate my-skill --json
{
  "my-skill": {
    "valid": true,
    "errors": []
  }
}
```

### Skill Discovery

Automatically discover skills in a directory tree:

```bash
$ skills-ref list ./skills --recursive
Found 5 skill(s) in ./skills:

  pdf-reader
    Path: ./skills/pdf-reader
    Description: Read and extract text from PDF files

  code-formatter
    Path: ./skills/code-formatter
    Description: Format source code using language-specific formatters
```

## License

Apache 2.0

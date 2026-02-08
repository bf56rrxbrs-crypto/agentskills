"""Skill validation logic."""

import unicodedata
from pathlib import Path
from typing import Optional

from .errors import ParseError
from .parser import find_skill_md, parse_frontmatter

MAX_SKILL_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
MAX_COMPATIBILITY_LENGTH = 500

# Allowed frontmatter fields per Agent Skills Spec
ALLOWED_FIELDS = {
    "name",
    "description",
    "license",
    "allowed-tools",
    "metadata",
    "compatibility",
}


def _validate_name(name: str, skill_dir: Path) -> list[str]:
    """Validate skill name format and directory match.

    Skill names support i18n characters (Unicode letters) plus hyphens.
    Names must be lowercase and cannot start/end with hyphens.
    """
    errors = []

    if not name or not isinstance(name, str) or not name.strip():
        errors.append("Field 'name' must be a non-empty string")
        return errors

    name = unicodedata.normalize("NFKC", name.strip())

    if len(name) > MAX_SKILL_NAME_LENGTH:
        errors.append(
            f"Skill name '{name}' exceeds {MAX_SKILL_NAME_LENGTH} character limit "
            f"({len(name)} chars). Consider using a shorter, more concise name."
        )

    if name != name.lower():
        lowercase_suggestion = name.lower()
        errors.append(
            f"Skill name '{name}' must be lowercase. "
            f"Suggestion: '{lowercase_suggestion}'"
        )

    if name.startswith("-") or name.endswith("-"):
        trimmed = name.strip("-")
        errors.append(
            f"Skill name cannot start or end with a hyphen. Suggestion: '{trimmed}'"
        )

    if "--" in name:
        fixed = name
        while "--" in fixed:
            fixed = fixed.replace("--", "-")
        errors.append(
            f"Skill name cannot contain consecutive hyphens. Suggestion: '{fixed}'"
        )

    if not all(c.isalnum() or c == "-" for c in name):
        errors.append(
            f"Skill name '{name}' contains invalid characters. "
            "Only letters, digits, and hyphens are allowed."
        )

    if skill_dir:
        dir_name = unicodedata.normalize("NFKC", skill_dir.name)
        if dir_name != name:
            errors.append(
                f"Directory name '{skill_dir.name}' must match skill name '{name}'. "
                f"Rename the directory to '{name}' or update the 'name' field in SKILL.md."
            )

    return errors


def _validate_description(description: str) -> list[str]:
    """Validate description format."""
    errors = []

    if not description or not isinstance(description, str) or not description.strip():
        errors.append("Field 'description' must be a non-empty string")
        return errors

    if len(description) > MAX_DESCRIPTION_LENGTH:
        errors.append(
            f"Description exceeds {MAX_DESCRIPTION_LENGTH} character limit "
            f"({len(description)} chars)"
        )

    return errors


def _validate_compatibility(compatibility: str) -> list[str]:
    """Validate compatibility format."""
    errors = []

    if not isinstance(compatibility, str):
        errors.append("Field 'compatibility' must be a string")
        return errors

    if len(compatibility) > MAX_COMPATIBILITY_LENGTH:
        errors.append(
            f"Compatibility exceeds {MAX_COMPATIBILITY_LENGTH} character limit "
            f"({len(compatibility)} chars)"
        )

    return errors


def _validate_metadata_fields(metadata: dict) -> list[str]:
    """Validate that only allowed fields are present."""
    errors = []

    extra_fields = set(metadata.keys()) - ALLOWED_FIELDS
    if extra_fields:
        errors.append(
            f"Unexpected fields in frontmatter: {', '.join(sorted(extra_fields))}. "
            f"Only {sorted(ALLOWED_FIELDS)} are allowed."
        )

    return errors


def validate_metadata(metadata: dict, skill_dir: Optional[Path] = None) -> list[str]:
    """Validate parsed skill metadata.

    This is the core validation function that works on already-parsed metadata,
    avoiding duplicate file I/O when called from the parser.

    Validates:
    - Presence of required fields (name, description)
    - Name format (lowercase, kebab-case, no leading/trailing hyphens, max 64 chars)
    - Description format (non-empty, max 1024 chars)
    - Compatibility format (if present, max 500 chars)
    - No unexpected fields beyond the allowed set
    - Directory name matches skill name (if skill_dir provided)

    Args:
        metadata: Parsed YAML frontmatter dictionary
        skill_dir: Optional path to skill directory (for name-directory match check)

    Returns:
        List of validation error messages with actionable suggestions.
        Empty list means all validation checks passed.

    Example:
        >>> metadata = {"name": "Invalid-Name", "description": "Test"}
        >>> errors = validate_metadata(metadata)
        >>> len(errors) > 0
        True
        >>> any("lowercase" in e for e in errors)
        True
    """
    errors = []
    errors.extend(_validate_metadata_fields(metadata))

    if "name" not in metadata:
        errors.append("Missing required field in frontmatter: name")
    else:
        errors.extend(_validate_name(metadata["name"], skill_dir))

    if "description" not in metadata:
        errors.append("Missing required field in frontmatter: description")
    else:
        errors.extend(_validate_description(metadata["description"]))

    if "compatibility" in metadata:
        errors.extend(_validate_compatibility(metadata["compatibility"]))

    return errors


def validate(skill_dir: Path) -> list[str]:
    """Validate a skill directory.

    Performs comprehensive validation including:
    - Directory exists and is a directory
    - SKILL.md file exists (either SKILL.md or skill.md)
    - Valid YAML frontmatter
    - All required fields present (name, description)
    - Field formats meet specification requirements
    - No unexpected fields present

    Args:
        skill_dir: Path to the skill directory to validate

    Returns:
        List of validation error messages with actionable suggestions.
        Empty list indicates the skill passed all validation checks.

    Example:
        >>> errors = validate(Path("my-skill"))
        >>> if errors:
        ...     for error in errors:
        ...         print(f"Error: {error}")
        ... else:
        ...     print("Skill is valid!")
    """
    skill_dir = Path(skill_dir)

    if not skill_dir.exists():
        return [f"Path does not exist: {skill_dir}"]

    if not skill_dir.is_dir():
        return [f"Not a directory: {skill_dir}"]

    skill_md = find_skill_md(skill_dir)
    if skill_md is None:
        return ["Missing required file: SKILL.md"]

    try:
        content = skill_md.read_text()
        metadata, _ = parse_frontmatter(content)
    except ParseError as e:
        return [str(e)]

    return validate_metadata(metadata, skill_dir)

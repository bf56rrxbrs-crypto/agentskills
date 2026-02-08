"""Utility functions for skills-ref library."""

from pathlib import Path
from typing import Optional

from .errors import SkillError
from .parser import read_properties
from .validator import validate


def get_skill_info(skill_dir: Path) -> dict:
    """Get comprehensive information about a skill.

    Args:
        skill_dir: Path to the skill directory

    Returns:
        Dictionary containing skill properties and validation status

    Example:
        >>> info = get_skill_info(Path("my-skill"))
        >>> print(info["name"])
        my-skill
    """
    skill_dir = Path(skill_dir)

    result = {
        "path": str(skill_dir),
        "valid": False,
        "properties": None,
        "validation_errors": [],
    }

    try:
        props = read_properties(skill_dir)
        result["properties"] = props.to_dict()

        errors = validate(skill_dir)
        result["validation_errors"] = errors
        result["valid"] = len(errors) == 0
    except SkillError as e:
        result["validation_errors"] = [str(e)]

    return result


def count_skills(directory: Path, recursive: bool = False) -> int:
    """Count the number of valid skills in a directory.

    Args:
        directory: Directory to search
        recursive: Whether to search recursively

    Returns:
        Number of valid skills found
    """
    from .parser import find_skill_md

    count = 0

    if recursive:
        for skill_md in directory.rglob("SKILL.md"):
            count += 1
        for skill_md in directory.rglob("skill.md"):
            if not (skill_md.parent / "SKILL.md").exists():
                count += 1
    else:
        for item in directory.iterdir():
            if item.is_dir() and find_skill_md(item):
                count += 1

    return count


def format_validation_error(error: str) -> str:
    """Format a validation error message with better readability.

    Args:
        error: Raw error message

    Returns:
        Formatted error message
    """
    # Add bullet point and indentation
    return f"  • {error}"


def suggest_fix(error: str) -> Optional[str]:
    """Suggest a fix for a validation error.

    Args:
        error: Validation error message

    Returns:
        Suggested fix, or None if no specific fix can be suggested
    """
    if "lowercase" in error.lower():
        return "Convert all characters in the name to lowercase"
    elif "start or end with a hyphen" in error:
        return "Remove leading or trailing hyphens from the name"
    elif "consecutive hyphens" in error:
        return "Replace consecutive hyphens with a single hyphen"
    elif "directory name" in error.lower() and "must match" in error.lower():
        return "Rename the directory or update the name field in SKILL.md"
    elif "exceeds" in error and "character limit" in error:
        return "Shorten the field to meet the character limit"

    return None

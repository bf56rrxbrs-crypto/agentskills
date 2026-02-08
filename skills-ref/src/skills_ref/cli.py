"""CLI for skills-ref library."""

import json
import sys
from pathlib import Path

import click

from .errors import SkillError
from .parser import find_skill_md, read_properties
from .prompt import to_prompt
from .validator import validate


def _is_skill_md_file(path: Path) -> bool:
    """Check if path points directly to a SKILL.md or skill.md file."""
    return path.is_file() and path.name.lower() == "skill.md"


@click.group()
@click.version_option()
def main():
    """Reference library for Agent Skills."""
    pass


@main.command("validate")
@click.argument(
    "skill_paths", type=click.Path(exists=True, path_type=Path), nargs=-1, required=True
)
@click.option("--json", "json_output", is_flag=True, help="Output results as JSON")
@click.option(
    "--quiet", "-q", is_flag=True, help="Only output errors (no success messages)"
)
def validate_cmd(skill_paths: tuple[Path, ...], json_output: bool, quiet: bool):
    """Validate one or more skill directories.

    Checks that each skill has a valid SKILL.md with proper frontmatter,
    correct naming conventions, and required fields.

    Exit codes:
        0: All skills valid
        1: One or more validation errors found
    """
    results = {}
    has_errors = False

    for skill_path in skill_paths:
        if _is_skill_md_file(skill_path):
            skill_path = skill_path.parent

        errors = validate(skill_path)
        results[str(skill_path)] = {"valid": len(errors) == 0, "errors": errors}

        if errors:
            has_errors = True

    if json_output:
        click.echo(json.dumps(results, indent=2))
    else:
        for path, result in results.items():
            if result["valid"]:
                if not quiet:
                    click.echo(f"✓ Valid skill: {path}")
            else:
                click.echo(f"✗ Validation failed for {path}:", err=True)
                for error in result["errors"]:
                    click.echo(f"  - {error}", err=True)

    if has_errors:
        sys.exit(1)


@main.command("read-properties")
@click.argument("skill_path", type=click.Path(exists=True, path_type=Path))
def read_properties_cmd(skill_path: Path):
    """Read and print skill properties as JSON.

    Parses the YAML frontmatter from SKILL.md and outputs the
    properties as JSON.

    Exit codes:
        0: Success
        1: Parse error
    """
    try:
        if _is_skill_md_file(skill_path):
            skill_path = skill_path.parent

        props = read_properties(skill_path)
        click.echo(json.dumps(props.to_dict(), indent=2))
    except SkillError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command("to-prompt")
@click.argument(
    "skill_paths", type=click.Path(exists=True, path_type=Path), nargs=-1, required=True
)
def to_prompt_cmd(skill_paths: tuple[Path, ...]):
    """Generate <available_skills> XML for agent prompts.

    Accepts one or more skill directories.

    Exit codes:
        0: Success
        1: Error
    """
    try:
        resolved_paths = []
        for skill_path in skill_paths:
            if _is_skill_md_file(skill_path):
                resolved_paths.append(skill_path.parent)
            else:
                resolved_paths.append(skill_path)

        output = to_prompt(resolved_paths)
        click.echo(output)
    except SkillError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command("list")
@click.argument("directory", type=click.Path(exists=True, path_type=Path), default=".")
@click.option("--json", "json_output", is_flag=True, help="Output results as JSON")
@click.option("--recursive", "-r", is_flag=True, help="Search recursively for skills")
def list_cmd(directory: Path, json_output: bool, recursive: bool):
    """List all skills found in a directory.

    Scans the given directory (and subdirectories if --recursive is used)
    for valid skill directories containing SKILL.md files.

    Exit codes:
        0: Success
        1: Error
    """
    try:
        skills = _discover_skills(directory, recursive)

        if json_output:
            skills_data = []
            for skill_path in skills:
                try:
                    props = read_properties(skill_path)
                    skills_data.append(
                        {
                            "path": str(skill_path),
                            "name": props.name,
                            "description": props.description,
                        }
                    )
                except SkillError:
                    # Skip skills that can't be read
                    continue
            click.echo(json.dumps(skills_data, indent=2))
        else:
            if not skills:
                click.echo(f"No skills found in {directory}")
            else:
                click.echo(f"Found {len(skills)} skill(s) in {directory}:\n")
                for skill_path in skills:
                    try:
                        props = read_properties(skill_path)
                        click.echo(f"  {props.name}")
                        click.echo(f"    Path: {skill_path}")
                        click.echo(
                            f"    Description: {props.description[:80]}{'...' if len(props.description) > 80 else ''}"
                        )
                        click.echo()
                    except SkillError as e:
                        click.echo(f"  {skill_path} (error: {e})")
                        click.echo()
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


def _discover_skills(directory: Path, recursive: bool) -> list[Path]:
    """Discover skill directories in the given directory.

    Args:
        directory: Directory to search
        recursive: Whether to search recursively

    Returns:
        List of paths to skill directories
    """
    skills = []

    if recursive:
        # Search recursively for SKILL.md files
        for skill_md in directory.rglob("SKILL.md"):
            skills.append(skill_md.parent)
        for skill_md in directory.rglob("skill.md"):
            # Only add if SKILL.md doesn't exist
            if not (skill_md.parent / "SKILL.md").exists():
                skills.append(skill_md.parent)
    else:
        # Only search immediate subdirectories
        for item in directory.iterdir():
            if item.is_dir():
                skill_md = find_skill_md(item)
                if skill_md:
                    skills.append(item)

    return sorted(skills)


if __name__ == "__main__":
    main()

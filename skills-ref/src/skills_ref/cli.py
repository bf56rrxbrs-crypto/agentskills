"""CLI for skills-ref library."""

import json
import subprocess
import sys
from pathlib import Path

import click

from .errors import SkillError
from .parser import read_properties
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
@click.argument("skill_path", type=click.Path(exists=True, path_type=Path))
def validate_cmd(skill_path: Path):
    """Validate a skill directory.

    Checks that the skill has a valid SKILL.md with proper frontmatter,
    correct naming conventions, and required fields.

    Exit codes:
        0: Valid skill
        1: Validation errors found
    """
    if _is_skill_md_file(skill_path):
        skill_path = skill_path.parent

    errors = validate(skill_path)

    if errors:
        click.echo(f"Validation failed for {skill_path}:", err=True)
        for error in errors:
            click.echo(f"  - {error}", err=True)
        sys.exit(1)
    else:
        click.echo(f"Valid skill: {skill_path}")


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


@main.command("auto-review")
@click.argument("path", type=click.Path(exists=True, path_type=Path), default=".")
@click.option("--json", "output_json", is_flag=True, help="Output results as JSON")
@click.option("--fix", is_flag=True, help="Automatically fix issues")
def auto_review_cmd(path: Path, output_json: bool, fix: bool):
    """Perform automated code review and quality checks.

    Checks linting, formatting, tests, and provides suggestions.

    Exit codes:
        0: All checks passed
        1: Issues found
    """
    results = {
        "linting": {"status": "unknown", "issues": []},
        "formatting": {"status": "unknown", "issues": []},
        "tests": {"status": "unknown", "output": ""},
        "overall": "unknown",
    }

    # Change to the path directory if it's a directory
    if path.is_dir():
        original_dir = Path.cwd()
        import os

        os.chdir(path)
    else:
        click.echo("Error: Path must be a directory", err=True)
        sys.exit(1)

    try:
        # Check linting
        lint_result = subprocess.run(
            ["ruff", "check", "."], capture_output=True, text=True
        )
        if lint_result.returncode == 0:
            results["linting"]["status"] = "passed"
        else:
            results["linting"]["status"] = "failed"
            results["linting"]["issues"] = (
                lint_result.stdout.split("\n") if lint_result.stdout else []
            )

            if fix:
                subprocess.run(["ruff", "check", "--fix", "."], capture_output=True)
                results["linting"]["fixed"] = True

        # Check formatting
        format_result = subprocess.run(
            ["ruff", "format", "--check", "."], capture_output=True, text=True
        )
        if format_result.returncode == 0:
            results["formatting"]["status"] = "passed"
        else:
            results["formatting"]["status"] = "failed"
            if fix:
                subprocess.run(["ruff", "format", "."], capture_output=True)
                results["formatting"]["fixed"] = True

        # Run tests
        test_result = subprocess.run(
            ["pytest", "-v", "--tb=short"], capture_output=True, text=True
        )
        if test_result.returncode == 0:
            results["tests"]["status"] = "passed"
        else:
            results["tests"]["status"] = "failed"
            results["tests"]["output"] = test_result.stdout

        # Determine overall status
        if all(
            r["status"] == "passed"
            for r in [results["linting"], results["formatting"], results["tests"]]
        ):
            results["overall"] = "passed"
        else:
            results["overall"] = "failed"

    except FileNotFoundError as e:
        click.echo(f"Error: Required tool not found: {e}", err=True)
        sys.exit(1)
    finally:
        if path.is_dir():
            os.chdir(original_dir)

    # Output results
    if output_json:
        click.echo(json.dumps(results, indent=2))
    else:
        click.echo("\n=== Automated Review Results ===\n")
        click.echo(f"Linting: {results['linting']['status'].upper()}")
        if results["linting"]["issues"]:
            for issue in results["linting"]["issues"][:10]:  # Show first 10
                if issue.strip():
                    click.echo(f"  - {issue}")

        click.echo(f"\nFormatting: {results['formatting']['status'].upper()}")
        click.echo(f"\nTests: {results['tests']['status'].upper()}")

        if fix:
            click.echo("\n✓ Auto-fix applied where possible")

        click.echo(f"\nOverall: {results['overall'].upper()}")

    sys.exit(0 if results["overall"] == "passed" else 1)


if __name__ == "__main__":
    main()

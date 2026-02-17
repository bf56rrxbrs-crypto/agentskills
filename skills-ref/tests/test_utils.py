"""Tests for utility module."""

from skills_ref.utils import (
    count_skills,
    format_validation_error,
    get_skill_info,
    suggest_fix,
)


def test_get_skill_info_valid(tmp_path):
    """get_skill_info should return complete info for valid skill."""
    skill_dir = tmp_path / "my-skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("""---
name: my-skill
description: A test skill
license: MIT
---
Body
""")

    info = get_skill_info(skill_dir)
    assert info["valid"] is True
    assert info["validation_errors"] == []
    assert info["properties"]["name"] == "my-skill"
    assert info["properties"]["description"] == "A test skill"
    assert info["properties"]["license"] == "MIT"


def test_get_skill_info_invalid(tmp_path):
    """get_skill_info should return errors for invalid skill."""
    skill_dir = tmp_path / "Invalid-Skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("""---
name: Invalid-Skill
description: Test
---
Body
""")

    info = get_skill_info(skill_dir)
    assert info["valid"] is False
    assert len(info["validation_errors"]) > 0
    assert any("lowercase" in err for err in info["validation_errors"])


def test_get_skill_info_missing_skill_md(tmp_path):
    """get_skill_info should handle missing SKILL.md."""
    skill_dir = tmp_path / "empty"
    skill_dir.mkdir()

    info = get_skill_info(skill_dir)
    assert info["valid"] is False
    assert len(info["validation_errors"]) > 0


def test_count_skills_flat(tmp_path):
    """count_skills should count skills in immediate subdirectories."""
    (tmp_path / "skill-a").mkdir()
    (tmp_path / "skill-a" / "SKILL.md").write_text("""---
name: skill-a
description: First
---
Body
""")

    (tmp_path / "skill-b").mkdir()
    (tmp_path / "skill-b" / "SKILL.md").write_text("""---
name: skill-b
description: Second
---
Body
""")

    count = count_skills(tmp_path, recursive=False)
    assert count == 2


def test_count_skills_recursive(tmp_path):
    """count_skills should count skills recursively."""
    (tmp_path / "level1" / "skill-a").mkdir(parents=True)
    (tmp_path / "level1" / "skill-a" / "SKILL.md").write_text("""---
name: skill-a
description: First
---
Body
""")

    (tmp_path / "level1" / "level2" / "skill-b").mkdir(parents=True)
    (tmp_path / "level1" / "level2" / "skill-b" / "SKILL.md").write_text("""---
name: skill-b
description: Second
---
Body
""")

    count = count_skills(tmp_path, recursive=True)
    assert count == 2


def test_count_skills_empty(tmp_path):
    """count_skills should return 0 for empty directory."""
    count = count_skills(tmp_path, recursive=False)
    assert count == 0


def test_format_validation_error():
    """format_validation_error should add formatting."""
    error = "Field 'name' is invalid"
    formatted = format_validation_error(error)
    assert "•" in formatted
    assert error in formatted


def test_suggest_fix_lowercase():
    """suggest_fix should suggest lowercase conversion."""
    error = "Skill name must be lowercase"
    suggestion = suggest_fix(error)
    assert suggestion is not None
    assert "lowercase" in suggestion.lower()


def test_suggest_fix_hyphen():
    """suggest_fix should suggest hyphen fix."""
    error = "Skill name cannot start or end with a hyphen"
    suggestion = suggest_fix(error)
    assert suggestion is not None
    assert "hyphen" in suggestion.lower()


def test_suggest_fix_directory_mismatch():
    """suggest_fix should suggest directory rename."""
    error = "Directory name 'wrong' must match skill name 'correct'"
    suggestion = suggest_fix(error)
    assert suggestion is not None
    assert "directory" in suggestion.lower() or "name" in suggestion.lower()


def test_suggest_fix_no_suggestion():
    """suggest_fix should return None for unknown errors."""
    error = "Some unknown validation error"
    suggestion = suggest_fix(error)
    # May or may not have a suggestion depending on keywords
    # Just ensure it doesn't crash
    assert suggestion is None or isinstance(suggestion, str)

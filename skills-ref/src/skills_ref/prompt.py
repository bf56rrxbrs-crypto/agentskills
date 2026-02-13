"""Generate <available_skills> XML prompt block for agent system prompts."""

import html
from pathlib import Path

from .parser import find_skill_md, read_properties


def to_prompt(skill_dirs: list[Path]) -> str:
    """Generate the <available_skills> XML block for inclusion in agent prompts.

    This XML format is what Anthropic uses and recommends for Claude models.
    Skill Clients may format skill information differently to suit their
    models or preferences.

    Args:
        skill_dirs: List of paths to skill directories. Each directory should
            contain a valid SKILL.md file.

    Returns:
        XML string with <available_skills> block containing each skill's
        name, description, and location. Returns an empty block if no
        skills are provided.

    Raises:
        SkillError: If any skill directory is invalid or SKILL.md cannot be parsed.

    Example:
        >>> skills = [Path("pdf-reader"), Path("code-formatter")]
        >>> xml = to_prompt(skills)
        >>> print(xml)
        <available_skills>
        <skill>
        <name>pdf-reader</name>
        <description>Read and extract text from PDF files</description>
        <location>/path/to/pdf-reader/SKILL.md</location>
        </skill>
        <skill>
        <name>code-formatter</name>
        <description>Format source code</description>
        <location>/path/to/code-formatter/SKILL.md</location>
        </skill>
        </available_skills>
    """
    if not skill_dirs:
        return "<available_skills>\n</available_skills>"

    lines = ["<available_skills>"]

    for skill_dir in skill_dirs:
        skill_dir = Path(skill_dir).resolve()
        props = read_properties(skill_dir)

        lines.append("<skill>")
        lines.append("<name>")
        lines.append(html.escape(props.name))
        lines.append("</name>")
        lines.append("<description>")
        lines.append(html.escape(props.description))
        lines.append("</description>")

        skill_md_path = find_skill_md(skill_dir)
        lines.append("<location>")
        lines.append(str(skill_md_path))
        lines.append("</location>")

        lines.append("</skill>")

    lines.append("</available_skills>")

    return "\n".join(lines)

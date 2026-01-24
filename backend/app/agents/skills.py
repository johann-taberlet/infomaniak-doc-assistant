"""
Skill Loader for the agentic system.

Skills are markdown files with YAML frontmatter that define:
- Metadata (name, description, allowed tools, trigger phrases)
- Content (instructions for the agent to execute)

Skills are organized in a directory structure like:
    skills/
    ├── kmeet/
    │   └── start-meeting.md
    ├── kdrive/
    │   └── share-file.md
    └── kchat/
        └── send-message.md

Skill names use the format "category/skill-name" (e.g., "kmeet/start-meeting").
"""

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from backend.app.core.config import get_settings


class SkillNotFoundError(Exception):
    """Raised when a skill file cannot be found."""

    pass


class SkillParseError(Exception):
    """Raised when a skill file has invalid format."""

    pass


@dataclass
class SkillMetadata:
    """Metadata extracted from skill file frontmatter."""

    name: str
    description: str
    allowed_tools: list[str]
    trigger_phrases: list[str] = field(default_factory=list)


@dataclass
class Skill:
    """A loaded skill with metadata and content."""

    metadata: SkillMetadata
    content: str  # Full markdown content (for agent context)


class SkillLoader:
    """
    Loads and parses skill markdown files.

    Skills are markdown files with YAML frontmatter containing metadata.
    The loader discovers skills by scanning the skills directory and
    provides methods to list and load them.
    """

    def __init__(self, skills_dir: str | None = None) -> None:
        """
        Initialize the skill loader.

        Args:
            skills_dir: Path to skills directory. If None, uses settings.skills_dir.
        """
        if skills_dir is None:
            settings = get_settings()
            skills_dir = settings.skills_dir
        self._skills_dir = Path(skills_dir)

    @property
    def skills_dir(self) -> Path:
        """Get the skills directory path."""
        return self._skills_dir

    def list_skills(self) -> list[SkillMetadata]:
        """
        List all available skills with their metadata.

        Returns:
            List of SkillMetadata for all valid skills found.
            Invalid skills are silently skipped.
        """
        skills: list[SkillMetadata] = []

        if not self._skills_dir.exists():
            return skills

        # Scan for .md files in category subdirectories
        for md_file in self._skills_dir.rglob("*.md"):
            # Get relative path from skills_dir
            rel_path = md_file.relative_to(self._skills_dir)

            # Skip files directly in skills_dir (must be in a category)
            if len(rel_path.parts) < 2:
                continue

            try:
                skill = self._load_skill_file(md_file)
                skills.append(skill.metadata)
            except (SkillParseError, SkillNotFoundError):
                # Skip invalid skills
                continue

        return skills

    def load_skill(self, skill_name: str) -> Skill:
        """
        Load a skill by name.

        Args:
            skill_name: Skill name in format "category/skill-name"
                       (e.g., "kmeet/start-meeting")

        Returns:
            The loaded Skill with metadata and content.

        Raises:
            SkillNotFoundError: If the skill file doesn't exist.
            SkillParseError: If the skill file has invalid format.
        """
        skill_path = self._skills_dir / f"{skill_name}.md"

        if not skill_path.exists():
            raise SkillNotFoundError(f"Skill not found: {skill_name}")

        return self._load_skill_file(skill_path)

    def get_skill(self, skill_name: str) -> Skill | None:
        """
        Get a skill by name, or None if not found.

        This is a convenience method that doesn't raise exceptions
        for missing skills.

        Args:
            skill_name: Skill name in format "category/skill-name"

        Returns:
            The loaded Skill, or None if not found or invalid.
        """
        try:
            return self.load_skill(skill_name)
        except (SkillNotFoundError, SkillParseError):
            return None

    def _load_skill_file(self, path: Path) -> Skill:
        """
        Load and parse a skill file.

        Args:
            path: Path to the skill markdown file.

        Returns:
            Parsed Skill object.

        Raises:
            SkillNotFoundError: If the file doesn't exist.
            SkillParseError: If the file format is invalid.
        """
        if not path.exists():
            raise SkillNotFoundError(f"Skill file not found: {path}")

        content = path.read_text(encoding="utf-8")
        frontmatter, markdown = self._parse_skill_file(content)

        # Extract and validate required fields
        name = frontmatter.get("name")
        if not name:
            raise SkillParseError(f"Missing 'name' in frontmatter: {path}")

        description = frontmatter.get("description")
        if not description:
            raise SkillParseError(f"Missing 'description' in frontmatter: {path}")

        allowed_tools = frontmatter.get("allowed-tools", [])
        if not isinstance(allowed_tools, list):
            raise SkillParseError(f"'allowed-tools' must be a list: {path}")

        trigger_phrases = frontmatter.get("trigger-phrases", [])
        if not isinstance(trigger_phrases, list):
            raise SkillParseError(f"'trigger-phrases' must be a list: {path}")

        metadata = SkillMetadata(
            name=name,
            description=description,
            allowed_tools=allowed_tools,
            trigger_phrases=trigger_phrases,
        )

        return Skill(metadata=metadata, content=markdown)

    def _parse_skill_file(self, content: str) -> tuple[dict, str]:
        """
        Parse frontmatter and content from a skill file.

        Args:
            content: Raw file content.

        Returns:
            Tuple of (frontmatter dict, markdown content).

        Raises:
            SkillParseError: If the frontmatter format is invalid.
        """
        if not content.startswith("---"):
            raise SkillParseError("Skill file must start with YAML frontmatter (---)")

        parts = content.split("---", 2)
        if len(parts) < 3:
            raise SkillParseError(
                "Invalid frontmatter format: must have opening and closing ---"
            )

        try:
            frontmatter = yaml.safe_load(parts[1])
        except yaml.YAMLError as e:
            raise SkillParseError(f"Invalid YAML in frontmatter: {e}") from e

        if frontmatter is None:
            frontmatter = {}

        markdown = parts[2].strip()
        return frontmatter, markdown


# =============================================================================
# Singleton Pattern
# =============================================================================

_loader_instance: SkillLoader | None = None


def get_skill_loader() -> SkillLoader:
    """
    Get the singleton SkillLoader instance.

    Returns:
        The global SkillLoader instance.
    """
    global _loader_instance
    if _loader_instance is None:
        _loader_instance = SkillLoader()
    return _loader_instance


def reset_skill_loader() -> None:
    """
    Reset the singleton SkillLoader instance.

    Useful for testing or when skills directory changes.
    """
    global _loader_instance
    _loader_instance = None

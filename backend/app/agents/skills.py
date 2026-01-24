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

import logging
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from backend.app.core.config import get_settings

logger = logging.getLogger(__name__)


class SkillNotFoundError(Exception):
    """Raised when a skill file cannot be found."""

    def __init__(self, skill_name: str, message: str | None = None):
        self.skill_name = skill_name
        super().__init__(message or f"Skill not found: {skill_name}")


class SkillParseError(Exception):
    """Raised when a skill file has invalid format."""

    def __init__(self, path: str | Path, reason: str):
        self.path = Path(path) if isinstance(path, str) else path
        self.reason = reason
        super().__init__(f"{reason}: {path}")


@dataclass
class SkillMetadata:
    """Metadata extracted from skill file frontmatter."""

    name: str
    description: str
    allowed_tools: list[str]
    trigger_phrases: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate metadata fields after initialization."""
        if not self.name or not self.name.strip():
            raise ValueError("name must be non-empty")
        if not self.description or not self.description.strip():
            raise ValueError("description must be non-empty")
        if not isinstance(self.allowed_tools, list):
            raise TypeError("allowed_tools must be a list")
        if not all(isinstance(t, str) for t in self.allowed_tools):
            raise TypeError("allowed_tools must contain only strings")
        if not isinstance(self.trigger_phrases, list):
            raise TypeError("trigger_phrases must be a list")
        if not all(isinstance(t, str) for t in self.trigger_phrases):
            raise TypeError("trigger_phrases must contain only strings")


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
            Invalid skills are logged and skipped.
        """
        skills: list[SkillMetadata] = []
        failed_count = 0

        if not self._skills_dir.exists():
            logger.warning(
                "Skills directory does not exist - no skills available: %s",
                self._skills_dir,
            )
            return skills

        # Scan for .md files in category subdirectories
        for md_file in self._skills_dir.rglob("*.md"):
            # Get relative path from skills_dir
            rel_path = md_file.relative_to(self._skills_dir)

            # Skip files directly in skills_dir (must be in a category)
            if len(rel_path.parts) < 2:
                continue

            try:
                # Compute skill name from path (e.g., "kmeet/start-meeting")
                skill_name = str(rel_path.with_suffix(""))
                skill = self._load_skill_file(md_file, skill_name)
                skills.append(skill.metadata)
            except SkillNotFoundError as e:
                # Race condition: file was deleted between rglob and load
                logger.warning(
                    "Skill file disappeared during listing: %s",
                    e.skill_name,
                )
                failed_count += 1
            except SkillParseError as e:
                # Malformed skill file - this is a configuration error
                logger.error(
                    "Failed to parse skill file (skill will not be available): %s - %s",
                    e.path,
                    e.reason,
                )
                failed_count += 1

        logger.info(
            "Skills loaded: %d successful, %d failed from %s",
            len(skills),
            failed_count,
            self._skills_dir,
        )

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
            raise SkillNotFoundError(skill_name)

        return self._load_skill_file(skill_path, skill_name)

    def get_skill(self, skill_name: str) -> Skill | None:
        """
        Get a skill by name, or None if not found.

        This is a convenience method that doesn't raise exceptions
        for missing skills. Parse errors are logged.

        Args:
            skill_name: Skill name in format "category/skill-name"

        Returns:
            The loaded Skill, or None if not found or invalid.
        """
        try:
            return self.load_skill(skill_name)
        except SkillNotFoundError:
            # Expected case - skill doesn't exist
            return None
        except SkillParseError as e:
            # Skill exists but is malformed - this is a bug that needs fixing
            logger.error(
                "Skill file is malformed and could not be loaded: %s - %s",
                e.path,
                e.reason,
            )
            return None

    def _load_skill_file(self, path: Path, skill_name: str | None = None) -> Skill:
        """
        Load and parse a skill file.

        Args:
            path: Path to the skill markdown file.
            skill_name: Optional skill name for better error messages.

        Returns:
            Parsed Skill object.

        Raises:
            SkillNotFoundError: If the file doesn't exist.
            SkillParseError: If the file format is invalid or unreadable.
        """
        if not path.exists():
            raise SkillNotFoundError(skill_name or str(path))

        # Read file with proper error handling for I/O issues
        try:
            content = path.read_text(encoding="utf-8")
        except PermissionError as e:
            raise SkillParseError(path, f"Permission denied: {e}") from e
        except UnicodeDecodeError as e:
            raise SkillParseError(path, f"File is not valid UTF-8: {e}") from e
        except OSError as e:
            raise SkillParseError(path, f"Cannot read file: {e}") from e

        frontmatter, markdown = self._parse_skill_file(content, path)

        # Extract and validate required fields
        name = frontmatter.get("name")
        if not name:
            raise SkillParseError(path, "Missing 'name' in frontmatter")

        description = frontmatter.get("description")
        if not description:
            raise SkillParseError(path, "Missing 'description' in frontmatter")

        allowed_tools = frontmatter.get("allowed-tools", [])
        if not isinstance(allowed_tools, list):
            raise SkillParseError(path, "'allowed-tools' must be a list")

        trigger_phrases = frontmatter.get("trigger-phrases", [])
        if not isinstance(trigger_phrases, list):
            raise SkillParseError(path, "'trigger-phrases' must be a list")

        metadata = SkillMetadata(
            name=name,
            description=description,
            allowed_tools=allowed_tools,
            trigger_phrases=trigger_phrases,
        )

        return Skill(metadata=metadata, content=markdown)

    def _parse_skill_file(self, content: str, path: Path) -> tuple[dict, str]:
        """
        Parse frontmatter and content from a skill file.

        Args:
            content: Raw file content.
            path: Path to the skill file (for error messages).

        Returns:
            Tuple of (frontmatter dict, markdown content).

        Raises:
            SkillParseError: If the frontmatter format is invalid.
        """
        if not content.startswith("---"):
            raise SkillParseError(path, "Skill file must start with YAML frontmatter (---)")

        parts = content.split("---", 2)
        if len(parts) < 3:
            raise SkillParseError(
                path, "Invalid frontmatter format: must have opening and closing ---"
            )

        try:
            frontmatter = yaml.safe_load(parts[1])
        except yaml.YAMLError as e:
            raise SkillParseError(path, f"Invalid YAML in frontmatter: {e}") from e

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

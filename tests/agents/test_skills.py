"""
Unit tests for the skill loader.
"""

import pytest

from backend.app.agents.skills import (
    Skill,
    SkillLoader,
    SkillMetadata,
    SkillNotFoundError,
    SkillParseError,
    get_skill_loader,
    reset_skill_loader,
)


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def skills_dir(tmp_path):
    """Create a temporary skills directory with test files."""
    # Create category directories
    kmeet_dir = tmp_path / "kmeet"
    kmeet_dir.mkdir()
    kdrive_dir = tmp_path / "kdrive"
    kdrive_dir.mkdir()

    # Create valid skill file
    valid_skill = kmeet_dir / "start-meeting.md"
    valid_skill.write_text(
        """---
name: start-meeting
description: Start a video meeting
allowed-tools:
  - updateState
  - showPanel
trigger-phrases:
  - start a meeting
  - call someone
---

# Start Meeting

This is the skill content.
"""
    )

    # Create skill with minimal frontmatter
    minimal_skill = kdrive_dir / "share-file.md"
    minimal_skill.write_text(
        """---
name: share-file
description: Share a file with users
allowed-tools: []
---

# Share File

Minimal skill content.
"""
    )

    return tmp_path


@pytest.fixture
def empty_skills_dir(tmp_path):
    """Create an empty skills directory."""
    return tmp_path


@pytest.fixture
def invalid_skills_dir(tmp_path):
    """Create a skills directory with invalid skill files."""
    category_dir = tmp_path / "invalid"
    category_dir.mkdir()

    # Missing name
    missing_name = category_dir / "missing-name.md"
    missing_name.write_text(
        """---
description: Missing name field
allowed-tools: []
---

Content here.
"""
    )

    # Invalid YAML
    invalid_yaml = category_dir / "invalid-yaml.md"
    invalid_yaml.write_text(
        """---
name: [invalid
description: bad yaml
---

Content here.
"""
    )

    # No frontmatter
    no_frontmatter = category_dir / "no-frontmatter.md"
    no_frontmatter.write_text("# Just markdown\n\nNo frontmatter here.")

    return tmp_path


@pytest.fixture
def loader(skills_dir):
    """Create a SkillLoader with the test skills directory."""
    return SkillLoader(str(skills_dir))


# =============================================================================
# SkillMetadata Tests
# =============================================================================


class TestSkillMetadata:
    """Tests for SkillMetadata dataclass."""

    def test_creation_with_all_fields(self):
        """Test creating metadata with all fields."""
        metadata = SkillMetadata(
            name="test-skill",
            description="A test skill",
            allowed_tools=["tool1", "tool2"],
            trigger_phrases=["do something", "make it happen"],
        )
        assert metadata.name == "test-skill"
        assert metadata.description == "A test skill"
        assert metadata.allowed_tools == ["tool1", "tool2"]
        assert metadata.trigger_phrases == ["do something", "make it happen"]

    def test_creation_with_defaults(self):
        """Test creating metadata with default trigger_phrases."""
        metadata = SkillMetadata(
            name="test-skill",
            description="A test skill",
            allowed_tools=["tool1"],
        )
        assert metadata.trigger_phrases == []


# =============================================================================
# Skill Tests
# =============================================================================


class TestSkill:
    """Tests for Skill dataclass."""

    def test_creation(self):
        """Test creating a Skill instance."""
        metadata = SkillMetadata(
            name="test-skill",
            description="A test skill",
            allowed_tools=["tool1"],
        )
        skill = Skill(metadata=metadata, content="# Skill Content\n\nSome instructions.")
        assert skill.metadata == metadata
        assert skill.content == "# Skill Content\n\nSome instructions."


# =============================================================================
# SkillLoader Tests
# =============================================================================


class TestSkillLoader:
    """Tests for SkillLoader class."""

    def test_init_with_explicit_path(self, skills_dir):
        """Test initializing loader with explicit path."""
        loader = SkillLoader(str(skills_dir))
        assert loader.skills_dir == skills_dir

    def test_list_skills_empty_dir(self, empty_skills_dir):
        """Test listing skills in empty directory."""
        loader = SkillLoader(str(empty_skills_dir))
        skills = loader.list_skills()
        assert skills == []

    def test_list_skills_nonexistent_dir(self, tmp_path):
        """Test listing skills when directory doesn't exist."""
        loader = SkillLoader(str(tmp_path / "nonexistent"))
        skills = loader.list_skills()
        assert skills == []

    def test_list_skills_with_skills(self, loader):
        """Test listing skills returns metadata for all valid skills."""
        skills = loader.list_skills()
        assert len(skills) == 2

        names = {s.name for s in skills}
        assert "start-meeting" in names
        assert "share-file" in names

    def test_list_skills_skips_invalid(self, invalid_skills_dir):
        """Test that list_skills skips invalid skill files."""
        loader = SkillLoader(str(invalid_skills_dir))
        skills = loader.list_skills()
        # All files in invalid_skills_dir are invalid, so list should be empty
        assert skills == []

    def test_load_skill_success(self, loader):
        """Test loading a valid skill."""
        skill = loader.load_skill("kmeet/start-meeting")

        assert skill.metadata.name == "start-meeting"
        assert skill.metadata.description == "Start a video meeting"
        assert skill.metadata.allowed_tools == ["updateState", "showPanel"]
        assert skill.metadata.trigger_phrases == ["start a meeting", "call someone"]
        assert "# Start Meeting" in skill.content
        assert "This is the skill content." in skill.content

    def test_load_skill_minimal(self, loader):
        """Test loading a skill with minimal frontmatter."""
        skill = loader.load_skill("kdrive/share-file")

        assert skill.metadata.name == "share-file"
        assert skill.metadata.description == "Share a file with users"
        assert skill.metadata.allowed_tools == []
        assert skill.metadata.trigger_phrases == []

    def test_load_skill_not_found(self, loader):
        """Test loading a nonexistent skill raises SkillNotFoundError."""
        with pytest.raises(SkillNotFoundError) as exc_info:
            loader.load_skill("nonexistent/skill")
        assert "nonexistent/skill" in str(exc_info.value)

    def test_load_skill_invalid_yaml(self, invalid_skills_dir):
        """Test loading a skill with invalid YAML raises SkillParseError."""
        loader = SkillLoader(str(invalid_skills_dir))
        with pytest.raises(SkillParseError) as exc_info:
            loader.load_skill("invalid/invalid-yaml")
        assert "Invalid YAML" in str(exc_info.value)

    def test_load_skill_missing_name(self, invalid_skills_dir):
        """Test loading a skill without name raises SkillParseError."""
        loader = SkillLoader(str(invalid_skills_dir))
        with pytest.raises(SkillParseError) as exc_info:
            loader.load_skill("invalid/missing-name")
        assert "Missing 'name'" in str(exc_info.value)

    def test_load_skill_no_frontmatter(self, invalid_skills_dir):
        """Test loading a skill without frontmatter raises SkillParseError."""
        loader = SkillLoader(str(invalid_skills_dir))
        with pytest.raises(SkillParseError) as exc_info:
            loader.load_skill("invalid/no-frontmatter")
        assert "must start with YAML frontmatter" in str(exc_info.value)

    def test_get_skill_returns_skill(self, loader):
        """Test get_skill returns skill when found."""
        skill = loader.get_skill("kmeet/start-meeting")
        assert skill is not None
        assert skill.metadata.name == "start-meeting"

    def test_get_skill_returns_none_not_found(self, loader):
        """Test get_skill returns None when skill not found."""
        skill = loader.get_skill("nonexistent/skill")
        assert skill is None

    def test_get_skill_returns_none_invalid(self, invalid_skills_dir):
        """Test get_skill returns None for invalid skill."""
        loader = SkillLoader(str(invalid_skills_dir))
        skill = loader.get_skill("invalid/invalid-yaml")
        assert skill is None


# =============================================================================
# Singleton Tests
# =============================================================================


class TestSingleton:
    """Tests for singleton pattern."""

    def test_get_skill_loader_returns_same_instance(self):
        """Test that get_skill_loader returns the same instance."""
        reset_skill_loader()
        loader1 = get_skill_loader()
        loader2 = get_skill_loader()
        assert loader1 is loader2

    def test_reset_skill_loader(self):
        """Test that reset_skill_loader creates new instance."""
        reset_skill_loader()
        loader1 = get_skill_loader()
        reset_skill_loader()
        loader2 = get_skill_loader()
        assert loader1 is not loader2

    def test_get_skill_loader_uses_settings(self):
        """Test that get_skill_loader uses settings.skills_dir by default."""
        reset_skill_loader()
        loader = get_skill_loader()
        # Default from settings is "skills"
        assert "skills" in str(loader.skills_dir)


# =============================================================================
# Edge Cases
# =============================================================================


class TestEdgeCases:
    """Tests for edge cases."""

    def test_skill_file_in_root_is_ignored(self, tmp_path):
        """Test that skill files directly in skills_dir are ignored."""
        # Create a file in the root (not in a category subdirectory)
        root_skill = tmp_path / "root-skill.md"
        root_skill.write_text(
            """---
name: root-skill
description: Should be ignored
allowed-tools: []
---

Content.
"""
        )

        loader = SkillLoader(str(tmp_path))
        skills = loader.list_skills()
        assert skills == []

    def test_empty_frontmatter_values(self, tmp_path):
        """Test handling of empty frontmatter."""
        category = tmp_path / "test"
        category.mkdir()
        skill_file = category / "empty.md"
        skill_file.write_text(
            """---
name: empty-skill
description: Empty allowed-tools
allowed-tools:
trigger-phrases:
---

Content.
"""
        )

        loader = SkillLoader(str(tmp_path))
        # This should raise because allowed-tools: without value becomes None
        with pytest.raises(SkillParseError):
            loader.load_skill("test/empty")

    def test_allowed_tools_not_list(self, tmp_path):
        """Test error when allowed-tools is not a list."""
        category = tmp_path / "test"
        category.mkdir()
        skill_file = category / "bad-tools.md"
        skill_file.write_text(
            """---
name: bad-tools
description: allowed-tools should be a list
allowed-tools: "not a list"
---

Content.
"""
        )

        loader = SkillLoader(str(tmp_path))
        with pytest.raises(SkillParseError) as exc_info:
            loader.load_skill("test/bad-tools")
        assert "'allowed-tools' must be a list" in str(exc_info.value)

    def test_trigger_phrases_not_list(self, tmp_path):
        """Test error when trigger-phrases is not a list."""
        category = tmp_path / "test"
        category.mkdir()
        skill_file = category / "bad-triggers.md"
        skill_file.write_text(
            """---
name: bad-triggers
description: trigger-phrases should be a list
allowed-tools: []
trigger-phrases: "not a list"
---

Content.
"""
        )

        loader = SkillLoader(str(tmp_path))
        with pytest.raises(SkillParseError) as exc_info:
            loader.load_skill("test/bad-triggers")
        assert "'trigger-phrases' must be a list" in str(exc_info.value)


# =============================================================================
# Exception Attribute Tests
# =============================================================================


class TestExceptionAttributes:
    """Tests for exception attributes for programmatic access."""

    def test_skill_not_found_error_has_skill_name(self, loader):
        """Test SkillNotFoundError has skill_name attribute."""
        with pytest.raises(SkillNotFoundError) as exc_info:
            loader.load_skill("nonexistent/skill")
        assert exc_info.value.skill_name == "nonexistent/skill"

    def test_skill_parse_error_has_path_and_reason(self, tmp_path):
        """Test SkillParseError has path and reason attributes."""
        category = tmp_path / "test"
        category.mkdir()
        skill_file = category / "bad.md"
        skill_file.write_text("# No frontmatter")

        loader = SkillLoader(str(tmp_path))
        with pytest.raises(SkillParseError) as exc_info:
            loader.load_skill("test/bad")

        assert exc_info.value.path == skill_file
        assert "YAML frontmatter" in exc_info.value.reason


# =============================================================================
# SkillMetadata Validation Tests
# =============================================================================


class TestSkillMetadataValidation:
    """Tests for SkillMetadata self-validation."""

    def test_empty_name_raises_value_error(self):
        """Test creating metadata with empty name raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            SkillMetadata(name="", description="desc", allowed_tools=[])
        assert "name must be non-empty" in str(exc_info.value)

    def test_whitespace_only_name_raises_value_error(self):
        """Test creating metadata with whitespace-only name raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            SkillMetadata(name="   ", description="desc", allowed_tools=[])
        assert "name must be non-empty" in str(exc_info.value)

    def test_empty_description_raises_value_error(self):
        """Test creating metadata with empty description raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            SkillMetadata(name="test", description="", allowed_tools=[])
        assert "description must be non-empty" in str(exc_info.value)

    def test_allowed_tools_not_list_raises_type_error(self):
        """Test creating metadata with non-list allowed_tools raises TypeError."""
        with pytest.raises(TypeError) as exc_info:
            SkillMetadata(name="test", description="desc", allowed_tools="not a list")  # type: ignore
        assert "allowed_tools must be a list" in str(exc_info.value)

    def test_allowed_tools_with_non_strings_raises_type_error(self):
        """Test creating metadata with non-string items in allowed_tools raises TypeError."""
        with pytest.raises(TypeError) as exc_info:
            SkillMetadata(name="test", description="desc", allowed_tools=[1, 2, 3])  # type: ignore
        assert "allowed_tools must contain only strings" in str(exc_info.value)

    def test_trigger_phrases_with_non_strings_raises_type_error(self):
        """Test creating metadata with non-string items in trigger_phrases raises TypeError."""
        with pytest.raises(TypeError) as exc_info:
            SkillMetadata(
                name="test",
                description="desc",
                allowed_tools=[],
                trigger_phrases=[1, 2, 3],  # type: ignore
            )
        assert "trigger_phrases must contain only strings" in str(exc_info.value)


# =============================================================================
# Additional Coverage Tests
# =============================================================================


class TestAdditionalCoverage:
    """Additional tests to improve coverage."""

    def test_load_skill_missing_description(self, tmp_path):
        """Test loading a skill without description raises SkillParseError."""
        category = tmp_path / "test"
        category.mkdir()
        skill_file = category / "no-desc.md"
        skill_file.write_text(
            """---
name: no-desc
allowed-tools: []
---

Content.
"""
        )

        loader = SkillLoader(str(tmp_path))
        with pytest.raises(SkillParseError) as exc_info:
            loader.load_skill("test/no-desc")
        assert "Missing 'description'" in exc_info.value.reason

    def test_frontmatter_missing_closing_delimiter(self, tmp_path):
        """Test skill with missing closing --- in frontmatter."""
        category = tmp_path / "test"
        category.mkdir()
        skill_file = category / "bad-delimiter.md"
        skill_file.write_text(
            """---
name: test
description: Test
allowed-tools: []
Content without closing delimiter.
"""
        )

        loader = SkillLoader(str(tmp_path))
        with pytest.raises(SkillParseError) as exc_info:
            loader.load_skill("test/bad-delimiter")
        assert "opening and closing ---" in exc_info.value.reason

    def test_skill_with_unicode_content(self, tmp_path):
        """Test skill files with unicode content are loaded correctly."""
        category = tmp_path / "test"
        category.mkdir()
        skill_file = category / "unicode.md"
        skill_file.write_text(
            """---
name: unicode-skill
description: Skill avec des caractères spéciaux
allowed-tools: []
---

# Réponse française

Contenu avec des accents: é, è, ç, à
""",
            encoding="utf-8",
        )

        loader = SkillLoader(str(tmp_path))
        skill = loader.load_skill("test/unicode")
        assert "é, è, ç, à" in skill.content
        assert "spéciaux" in skill.metadata.description

    def test_deeply_nested_skill_listing(self, tmp_path):
        """Test behavior of skills in nested subdirectories."""
        deep_dir = tmp_path / "category" / "subcategory"
        deep_dir.mkdir(parents=True)
        skill_file = deep_dir / "deep-skill.md"
        skill_file.write_text(
            """---
name: deep-skill
description: Deeply nested
allowed-tools: []
---

Content.
"""
        )

        loader = SkillLoader(str(tmp_path))
        skills = loader.list_skills()
        # Verify deeply nested skills are found
        assert len(skills) == 1
        assert skills[0].name == "deep-skill"

        # Verify they can be loaded with the correct path
        skill = loader.load_skill("category/subcategory/deep-skill")
        assert skill.metadata.name == "deep-skill"

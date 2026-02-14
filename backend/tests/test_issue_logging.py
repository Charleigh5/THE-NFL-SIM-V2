#!/usr/bin/env python3
"""
Issue Logger Tests
==================
Unit tests for IssueLoggerService.
"""

import os
import tempfile
from pathlib import Path

import pytest

from app.services.issue_logger import IssueEntry, IssueLoggerService, format_issue_entry


class TestFormatIssueEntry:
    """Tests for the format_issue_entry pure function."""

    def test_basic_formatting(self):
        """Entry is formatted correctly."""
        entry = IssueEntry(
            message="Test issue message",
            context="Dashboard",
            page="Mission Control"
        )

        formatted = format_issue_entry(entry)

        assert "Test issue message" in formatted
        assert "Dashboard" in formatted
        assert "Mission Control" in formatted
        assert "###" in formatted  # Markdown header

    def test_no_page_context(self):
        """Entry without page still formats."""
        entry = IssueEntry(
            message="No page specified",
            context="Frontend"
        )

        formatted = format_issue_entry(entry)

        assert "No page specified" in formatted
        assert "Frontend" in formatted


class TestIssueLoggerService:
    """Tests for IssueLoggerService."""

    @pytest.fixture
    def temp_file(self):
        """Create a temporary file for testing."""
        fd, path = tempfile.mkstemp(suffix=".md")
        os.close(fd)
        yield Path(path)
        # Cleanup
        if Path(path).exists():
            os.unlink(path)

    @pytest.fixture
    def logger(self, temp_file):
        """Create an IssueLoggerService with temp file."""
        return IssueLoggerService(output_path=temp_file)

    def test_log_issue_creates_file(self, temp_file):
        """Logging creates file if not exists."""
        # Delete the file first
        temp_file.unlink()
        assert not temp_file.exists()

        logger = IssueLoggerService(output_path=temp_file)
        entry = IssueEntry(message="Test")

        result = logger.log_issue(entry)

        assert result is True
        assert temp_file.exists()

    def test_log_issue_appends(self, logger, temp_file):
        """Multiple issues are appended."""
        entry1 = IssueEntry(message="First issue")
        entry2 = IssueEntry(message="Second issue")

        logger.log_issue(entry1)
        logger.log_issue(entry2)

        content = temp_file.read_text(encoding="utf-8")

        assert "First issue" in content
        assert "Second issue" in content

    def test_file_header_created(self, logger, temp_file):
        """File header is created on first write."""
        # Delete to test header creation
        temp_file.unlink()

        entry = IssueEntry(message="Test")
        logger.log_issue(entry)

        content = temp_file.read_text(encoding="utf-8")

        assert "# Issue Log" in content


@pytest.mark.asyncio
class TestIssueLoggerAsync:
    """Async tests for IssueLoggerService."""

    @pytest.fixture
    def temp_file(self):
        fd, path = tempfile.mkstemp(suffix=".md")
        os.close(fd)
        yield Path(path)
        if Path(path).exists():
            os.unlink(path)

    async def test_log_issue_async(self, temp_file):
        """Async logging works."""
        logger = IssueLoggerService(output_path=temp_file)
        entry = IssueEntry(message="Async test")

        result = await logger.log_issue_async(entry)

        assert result is True
        content = temp_file.read_text(encoding="utf-8")
        assert "Async test" in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

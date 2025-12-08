#!/usr/bin/env python3
"""
Issue Logger Service
====================
Appends user-reported issues to a markdown document.

Context7 Best Practices:
- Pure functions for formatting
- Async file I/O (aiofiles or sync fallback)
- Clear typing
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional
import logging
import asyncio

logger = logging.getLogger(__name__)


@dataclass
class IssueEntry:
    """Represents a single issue report."""
    message: str
    context: str = "Frontend"
    page: Optional[str] = None
    timestamp: Optional[datetime] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


def format_issue_entry(entry: IssueEntry) -> str:
    """
    Format an issue entry as markdown.

    Context7 Best Practice: Pure function for formatting.
    """
    timestamp_str = entry.timestamp.strftime("%Y-%m-%d %H:%M:%S")
    page_info = f" ({entry.page})" if entry.page else ""

    return f"""
### [{timestamp_str}] Issue Report
> **Context**: {entry.context}{page_info}

{entry.message}

---
"""


class IssueLoggerService:
    """
    Service for logging user-reported issues to a markdown file.
    """

    def __init__(self, output_path: Optional[Path] = None):
        if output_path is None:
            # Default to project root ISSUES.md
            self.output_path = Path(__file__).parent.parent.parent.parent / "ISSUES.md"
        else:
            self.output_path = output_path

    def _ensure_file_header(self) -> None:
        """Create file with header if it doesn't exist."""
        if not self.output_path.exists():
            header = """# Issue Log

This file contains user-reported issues from the Mission Control interface.

---

"""
            self.output_path.write_text(header, encoding="utf-8")
            logger.info(f"Created issue log file: {self.output_path}")

    def log_issue(self, entry: IssueEntry) -> bool:
        """
        Append an issue to the log file.

        Returns:
            True if successful, False otherwise.
        """
        try:
            self._ensure_file_header()

            formatted = format_issue_entry(entry)

            with open(self.output_path, "a", encoding="utf-8") as f:
                f.write(formatted)

            logger.info(f"Logged issue: {entry.message[:50]}...")
            return True

        except Exception as e:
            logger.error(f"Failed to log issue: {e}")
            return False

    async def log_issue_async(self, entry: IssueEntry) -> bool:
        """
        Async version of log_issue.

        Falls back to sync if aiofiles not available.
        """
        try:
            import aiofiles

            self._ensure_file_header()
            formatted = format_issue_entry(entry)

            async with aiofiles.open(self.output_path, "a", encoding="utf-8") as f:
                await f.write(formatted)

            logger.info(f"Logged issue (async): {entry.message[:50]}...")
            return True

        except ImportError:
            # Fallback to sync
            return await asyncio.to_thread(self.log_issue, entry)
        except Exception as e:
            logger.error(f"Failed to log issue (async): {e}")
            return False

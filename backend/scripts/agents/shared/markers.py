#!/usr/bin/env python3
"""
Shared Marker Utilities for Agent Scripts
==========================================
Provides completion marker functions for the orchestration system.

Context7 Best Practices:
- Type hints on all functions
- Proper error handling
- JSON-formatted markers for debugging
"""

import json
import time
from pathlib import Path


def get_marker_dir() -> Path:
    """Get the marker directory, creating it if needed."""
    # Marker dir is at backend/.markers/
    marker_dir = Path(__file__).parent.parent.parent.parent / ".markers"
    marker_dir.mkdir(exist_ok=True)
    return marker_dir


def mark_complete(output_id: str, metadata: dict | None = None) -> Path:
    """
    Mark an output as complete by writing a .done marker file.

    Args:
        output_id: Unique identifier for the output
        metadata: Optional additional metadata to include

    Returns:
        Path to the created marker file
    """
    marker_dir = get_marker_dir()
    marker_path = marker_dir / f"{output_id}.done"

    marker_data = {
        "output_id": output_id,
        "timestamp": time.time(),
        "completed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    if metadata:
        marker_data["metadata"] = metadata

    marker_path.write_text(json.dumps(marker_data, indent=2))
    print(f"✅ Marked complete: {output_id}")

    return marker_path


def is_complete(output_id: str) -> bool:
    """Check if an output has been marked complete."""
    marker_dir = get_marker_dir()
    marker_path = marker_dir / f"{output_id}.done"
    return marker_path.exists()


def clear_markers() -> int:
    """Clear all completion markers. Returns count of cleared markers."""
    marker_dir = get_marker_dir()
    count = 0
    for marker in marker_dir.glob("*.done"):
        marker.unlink()
        count += 1
    return count
